# executing this against the blacklist will create a 29GB features.csv file

import requests
import re
import math
import tldextract
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurazione logging per stampa su schermo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_blacklist(url):
    logging.info("Scaricamento della blacklist...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logging.info("Download completato.")
        return response.iter_lines(decode_unicode=True)
    else:
        logging.error("Errore nel download.")
        return []

def extract_features(domain):
    domain = domain.strip()
    return [
        len(domain),
        domain.count('.') - 1,
        int(bool(re.search(r'[-_0-9]', domain))),
        calculate_entropy(domain),
        int(any(word in domain for word in ["login", "secure", "bank", "verify", "official"])),
        tldextract.extract(domain).suffix
    ]

def calculate_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

def process_batch(batch, output_file):
    df = pd.DataFrame(batch, columns=['Length', 'Subdomains', 'Special_Chars', 'Entropy', 'Suspicious_Words', 'TLD'])
    df = pd.get_dummies(df, columns=['TLD'], drop_first=True)
    df.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))

def process_domains_in_stream(url, output_file, batch_size=1000):
    logging.info("Inizio elaborazione domini in streaming...")
    domains = download_blacklist(url)
    batch = []

    with ThreadPoolExecutor(max_workers=4) as executor:  # Limita il numero di worker per evitare sovraccarico
        futures = []
        for i, domain in enumerate(domains):
            domain = domain.decode('utf-8').strip()
            batch.append(extract_features(domain))

            if len(batch) >= batch_size:
                futures.append(executor.submit(process_batch, batch, output_file))
                batch = []

        if batch:
            futures.append(executor.submit(process_batch, batch, output_file))

        for _ in tqdm(as_completed(futures), total=len(futures), desc="Processo parallelo dei batch", mininterval=0.1):
            pass  # Usa la barra di progresso senza log di ogni batch

def generate_summary_statistics(file_path, chunk_size=10000):
    logging.info("Generazione delle statistiche in parallelo...")
    chunks = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False, chunksize=chunk_size)
    summary = pd.DataFrame()

    with ThreadPoolExecutor(max_workers=4) as executor:  # Limita il numero di worker per evitare sovraccarico
        futures = [executor.submit(chunk.describe) for chunk in chunks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Calcolo parallelo delle statistiche", mininterval=0.1):
            chunk_summary = future.result().T
            summary = summary.add(chunk_summary, fill_value=0) if not summary.empty else chunk_summary

    summary /= len(futures)  # Media delle statistiche
    print(summary)
    return summary

blacklist_url = "https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt"
output_file = 'features.csv'
process_domains_in_stream(blacklist_url, output_file)

logging.info("Elaborazione completata. Dati salvati.")

summary_stats = generate_summary_statistics(output_file)

df = pd.read_csv(output_file, on_bad_lines='skip', low_memory=False)
X = df.drop('Malicious', axis=1, errors='ignore')
y = df['Malicious'] if 'Malicious' in df else [1 if i % 2 == 0 else 0 for i in range(len(df))]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
best_model = train_model(X_train, y_train)
metrics = evaluate_model(best_model, X_test, y_test)

joblib.dump(best_model, 'best_model.pkl')
logging.info("Miglior modello salvato.")
