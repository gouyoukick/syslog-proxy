import os
import socket
from datetime import datetime, timedelta
import re
import logging

# Configuration du logger (pour enregistrer les erreurs)
logging.basicConfig(filename="/opt/syslog-relay/syslog-relay-error.log", level=logging.ERROR)

# Fonction pour lire le fichier de configuration
def load_config(config_file):
    config = {}
    try:
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore les lignes vides et les commentaires
                    # Supprimer tout commentaire après un '#' et enlever les espaces supplémentaires
                    line = re.sub(r'\s*#.*$', '', line).strip()
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        logging.error(f"[ERROR] Erreur lors de la lecture du fichier de configuration : {e}")
    return config

# Charger la configuration depuis le fichier
config = load_config("/opt/syslog-relay/syslog-relay-config.txt")

# Paramètres extraits du fichier de config
BUFFER_FILE = config.get('log_directory', '/var/log') + "/" + config.get('log_file', 'buffer-relay.log')
RECEIVER_IP = config.get('receiver_ip', '192.168.3.2')  # Adresse IP du récepteur syslog
RECEIVER_PORT = int(config.get('receiver_port', 6666))  # Port du récepteur
TIMEOUT_SECONDS = int(config.get('timeout_seconds', 5))  # Timeout pour l'envoi
MAX_AGE_MINUTES = int(config.get('max_log_age', 2))  # Age maximum des logs avant suppression

def parse_syslog_timestamp(line):
    try:
        # Supprimer le PRI si présent (ex: "<189>")
        line = re.sub(r"^<\d+>", "", line).strip()

        # Vérifier que la ligne commence par une date valide (ex: "Apr  7 16:09:26")
        match = re.match(r"^([A-Za-z]{3} {1,2}\d{1,2} \d{2}:\d{2}:\d{2})", line)
        if not match:
            return None

        # Extraire le timestamp
        timestamp_str = match.group(1)

        # Corrige les espaces (ex: "Apr  7" → "Apr 7")
        timestamp_str = re.sub(r'\s+', ' ', timestamp_str.strip())

        # Ajoute l'année actuelle
        current_year = datetime.now().year
        full_timestamp = f"{current_year} {timestamp_str}"

        # Convertir en datetime
        log_time = datetime.strptime(full_timestamp, "%Y %b %d %H:%M:%S")
        return log_time

    except Exception as e:
        logging.error(f"[ERROR] Erreur dans le parsing de la ligne : {line} ({e})")
        return None

def send_log_to_receiver(log):
    try:
        with socket.create_connection((RECEIVER_IP, RECEIVER_PORT), timeout=TIMEOUT_SECONDS) as sock:
            sock.sendall(log.encode())
        return True
    except (socket.timeout, socket.error) as e:
        logging.error(f"[ERROR] Erreur de connexion : {e}")
        return False

def process_buffer():
    if not os.path.exists(BUFFER_FILE):
        logging.error(f"[ERROR] Fichier buffer non trouvé : {BUFFER_FILE}")
        return

    with open(BUFFER_FILE, 'r') as f:
        lines = f.readlines()

    if not lines:
        return

    new_lines = []
    now = datetime.now()

    # Traitement de chaque ligne dans le buffer
    for line in lines:
        line = line.strip()
        if not line:
            continue

        log_time = parse_syslog_timestamp(line)
        if log_time is None:
            continue

        # Vérification de l'âge du log
        age = now - log_time
        if age > timedelta(minutes=MAX_AGE_MINUTES):
            continue

        if send_log_to_receiver(line):
            # Log envoyé avec succès
            pass
        else:
            # Log non envoyé, le conserver pour un prochain essai
            new_lines.append(line + "\n")

    # Réécrire les lignes restantes dans le buffer
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_buffer()
