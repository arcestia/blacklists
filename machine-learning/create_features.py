import requests
import re
import math
import tldextract
import pandas as pd
import whois
import ipinfo
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.utils import resample
import logging
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import joblib
import socket
import os
import numpy as np

# Configure logging for console output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ACCESS_TOKEN = "your_ipinfo_access_token"
handler = ipinfo.getHandler(ACCESS_TOKEN)

# Improved feature extraction
def download_blacklist(url):
    logging.info("Downloading the blacklist...")
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        logging.info("Download complete.")
        return response.iter_lines(decode_unicode=True)
    except requests.RequestException as e:
        logging.error(f"Error during download: {e}")
        return []

def extract_features(domain):
    domain = domain.strip()
    tld_extract = tldextract.extract(domain)
    try:
        whois_info = whois.whois(domain)
        if isinstance(whois_info.creation_date, list):
            creation_date = whois_info.creation_date[0]
        else:
            creation_date = whois_info.creation_date
        domain_age = (datetime.now() - creation_date).days if creation_date else 0
    except Exception as e:
        logging.warning(f"WHOIS lookup failed for {domain}: {e}")
        domain_age = 0

    try:
        ip = socket.gethostbyname(domain)
        details = handler.getDetails(ip)
        hosting_provider = details.org if details and 'org' in details.all else "Unknown"
    except Exception as e:
        logging.warning(f"IP lookup failed for {domain}: {e}")
        hosting_provider = "Unknown"

    return [
        len(domain),  # Length of the domain
        domain.count('.') - 1,  # Number of subdomains
        int(bool(re.search(r'[-_0-9]', domain))),  # Presence of special characters or digits
        calculate_entropy(domain),  # Entropy of the domain
        int(any(word in domain.lower() for word in ["login", "secure", "bank", "verify", "official"])),  # Suspicious words
        tld_extract.suffix,  # Top-level domain (TLD)
        domain_age,  # Domain age in days
        hosting_provider  # Hosting provider
    ]

def calculate_entropy(domain):
    if len(domain) == 0:
        return 0
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]  # Probability of each character
    return -sum(p * math.log(p, 2) for p in prob)  # Entropy calculation

def process_batch(batch, output_file):
    df = pd.DataFrame(batch, columns=['Length', 'Subdomains', 'Special_Chars', 'Entropy', 'Suspicious_Words', 'TLD', 'Domain_Age', 'Hosting_Provider'])
    df = pd.get_dummies(df, columns=['TLD', 'Hosting_Provider'], drop_first=True)  # One-hot encoding for TLD and hosting provider
    df.to_csv(output_file, mode='a', index=False, header=not os.path.exists(output_file))  # Append to CSV

def process_domains_in_stream(url, output_file, batch_size=1000):
    logging.info("Starting domain processing in streaming mode...")
    domains = download_blacklist(url)
    batch = []

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:  # Multiprocessing with optimal workers
        futures = []
        for domain in domains:
            domain = domain.strip()
            if domain:
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

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(chunk.describe) for chunk in chunks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Parallel statistics calculation", mininterval=0.1):
            chunk_summary = future.result().T
            summary = summary.add(chunk_summary, fill_value=0) if not summary.empty else chunk_summary

    if len(futures) > 0:
        summary /= len(futures)
    print(summary)
    return summary

def train_model(X_train, y_train):
    logging.info("Starting model training...")
    model = GradientBoostingClassifier()
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 10],
        'learning_rate': [0.01, 0.1, 0.2]
    }
    grid_search = RandomizedSearchCV(model, param_grid, cv=5, n_jobs=-1, scoring='f1', n_iter=10, random_state=42)
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
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    logging.info(f"Model metrics: {metrics}")
    return metrics

# Execute script with improved features
blacklist_url = "https://github.com/fabriziosalmi/blacklists/releases/download/latest/blacklist.txt"
output_file = 'enhanced_features.csv'
process_domains_in_stream(blacklist_url, output_file)

logging.info("Processing complete. Data saved.")

summary_stats = generate_summary_statistics(output_file)

df = pd.read_csv(output_file, on_bad_lines='skip', low_memory=False)
X = df.drop('Malicious', axis=1, errors='ignore')
y = df['Malicious'] if 'Malicious' in df else np.random.choice([0, 1], size=len(df), p=[0.5, 0.5])  # Placeholder labels with balanced distribution

# Handling class imbalance
X_resampled, y_resampled = resample(X, y, replace=True, n_samples=len(y), random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)
best_model = train_model(X_train, y_train)
metrics = evaluate_model(best_model, X_test, y_test)

joblib.dump(best_model, 'best_model_enhanced.pkl')
logging.info("Best model saved.")
