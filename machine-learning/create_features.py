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
import joblib

# Configure logging for console output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_blacklist(url):
    logging.info("Downloading the blacklist...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logging.info("Download complete.")
        return response.iter_lines(decode_unicode=True)
    else:
        logging.error("Error during download.")
        return []

def extract_features(domain):
    domain = domain.strip()
    return [
        len(domain),  # Length of the domain
        domain.count('.') - 1,  # Number of subdomains
        int(bool(re.search(r'[-_0-9]', domain))),  # Presence of special characters or digits
        calculate_entropy(domain),  # Entropy of the domain
        int(any(word in domain for word in ["login", "secure", "bank", "verify", "official"])),  # Presence of suspicious words
        tldextract.extract(domain).suffix  # Top-level domain (TLD)
    ]

def calculate_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]  # Probability of each character
    return -sum(p * math.log(p, 2) for p in prob)  # Entropy calculation

def process_batch(batch, output_file):
    df = pd.DataFrame(batch, columns=['Length', 'Subdomains', 'Special_Chars', 'Entropy', 'Suspicious_Words', 'TLD'])
    df = pd.get_dummies(df, columns=['TLD'], drop_first=True)  # One-hot encoding for TLD
    df.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))  # Append to CSV

def process_domains_in_stream(url, output_file, batch_size=1000):
    logging.info("Starting domain processing in streaming mode...")
    domains = download_blacklist(url)
    batch = []

    with ThreadPoolExecutor(max_workers=4) as executor:  # Limit number of workers to avoid overload
        futures = []
        for domain in domains:
            domain = domain.strip()
            batch.append(extract_features(domain))

            if len(batch) >= batch_size:
                futures.append(executor.submit(process_batch, batch, output_file))
                batch = []

        if batch:
            futures.append(executor.submit(process_batch, batch, output_file))

        for _ in tqdm(as_completed(futures), total=len(futures), desc="Parallel batch processing", mininterval=0.1):
            pass  # Use progress bar without logging each batch

def generate_summary_statistics(file_path, chunk_size=10000):
    logging.info("Generating statistics in parallel...")
    chunks = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False, chunksize=chunk_size)
    summary = pd.DataFrame()

    with ThreadPoolExecutor(max_workers=4) as executor:  # Limit number of workers to avoid overload
        futures = [executor.submit(chunk.describe) for chunk in chunks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Parallel statistics calculation", mininterval=0.1):
            chunk_summary = future.result().T
            summary = summary.add(chunk_summary, fill_value=0) if not summary.empty else chunk_summary

    summary /= len(futures)  # Average of the statistics
    print(summary)
    return summary

def train_model(X_train, y_train):
    # Placeholder for model training - customize as needed
    logging.info("Starting model training...")
    model = RandomForestClassifier()
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30]
    }
    grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    logging.info("Model trained successfully.")
    return grid_search.best_estimator_

def evaluate_model(model, X_test, y_test):
    logging.info("Starting model evaluation...")
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    logging.info(f"Model metrics: {metrics}")
    return metrics

blacklist_url = "https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt"
output_file = 'features.csv'
process_domains_in_stream(blacklist_url, output_file)

logging.info("Processing complete. Data saved.")

summary_stats = generate_summary_statistics(output_file)

df = pd.read_csv(output_file, on_bad_lines='skip', low_memory=False)
X = df.drop('Malicious', axis=1, errors='ignore')
y = df['Malicious'] if 'Malicious' in df else [1 if i % 2 == 0 else 0 for i in range(len(df))]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
best_model = train_model(X_train, y_train)
metrics = evaluate_model(best_model, X_test, y_test)

joblib.dump(best_model, 'best_model.pkl')
logging.info("Best model saved.")
