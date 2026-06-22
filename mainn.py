import hashlib
import json
import os
from datetime import datetime

HASH_STORAGE_FILE = "saved_hashes.json"

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()

def load_saved_hashes():
    if os.path.exists(HASH_STORAGE_FILE):
        with open(HASH_STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_hashes(hashes):
    with open(HASH_STORAGE_FILE, "w") as file:
        json.dump(hashes, file, indent=4)

def monitor_file(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File does not exist: {file_path}")
        return
    current_hash = calculate_hash(file_path)
    saved_hashes = load_saved_hashes()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n========================================")
    print("       FILE INTEGRITY MONITOR")
    print("========================================")
    print(f"File      : {file_path}")
    print(f"Hash      : {current_hash}")
    print(f"Timestamp : {timestamp}")
    print("========================================")
    if file_path not in saved_hashes:
        saved_hashes[file_path] = current_hash
        save_hashes(saved_hashes)
        print("[INFO] First scan. Hash saved successfully. ✅")
        print("[INFO] Run again after modifying the file to detect changes.")
    elif saved_hashes[file_path] == current_hash:
        print("[SAFE] No changes detected. File integrity is intact. ✅")
    else:
        print("[WARNING] FILE INTEGRITY COMPROMISED! Hash mismatch detected. 🚨")
        print(f"[ALERT] Expected hash : {saved_hashes[file_path]}")
        print(f"[ALERT] Found hash    : {current_hash}")
        print("[ALERT] File has been modified since the last scan.")
        saved_hashes[file_path] = current_hash
        save_hashes(saved_hashes)
        print("[INFO] Current hash updated for future monitoring.")
    print("========================================\n")

while True:
    file_path = input("Enter the file path to monitor (or 'exit' to quit): ")
    if file_path.lower() == "exit":
        print("Exiting the file integrity monitor.")
        break
    monitor_file(file_path)