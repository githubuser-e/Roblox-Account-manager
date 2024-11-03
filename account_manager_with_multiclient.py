import os
import subprocess
import time
import json
import winreg
from cryptography.fernet import Fernet

# Path to Roblox Player executable
ROBLOX_PLAYER_PATH = r"C:\Users\YourUsername\AppData\Local\Roblox\Versions\version-xxxxxx\RobloxPlayerBeta.exe"

# Encryption and decryption key setup
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

cipher = load_key()

# Save and load encrypted account data
def save_accounts(accounts):
    encrypted_data = cipher.encrypt(json.dumps(accounts).encode())
    with open("accounts.db", "wb") as f:
        f.write(encrypted_data)

def load_accounts():
    if not os.path.exists("accounts.db"):
        return {}
    with open("accounts.db", "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

# Account management functions
def add_account():
    username = input("Enter the Roblox username: ")
    password = input("Enter the Roblox password: ")
    accounts = load_accounts()
    accounts[username] = password
    save_accounts(accounts)
    print(f"Account for {username} added successfully!")

def remove_account():
    username = input("Enter the username to remove: ")
    accounts = load_accounts()
    if username in accounts:
        del accounts[username]
        save_accounts(accounts)
        print(f"Account for {username} removed successfully!")
    else:
        print("Account not found.")

def view_accounts():
    accounts = load_accounts()
    if accounts:
        print("\nStored Accounts:")
        for username in accounts:
            print(f"- {username}")
    else:
        print("No accounts stored.")

def retrieve_password():
    username = input("Enter the username to retrieve password for: ")
    accounts = load_accounts()
    if username in accounts:
        print(f"Password for {username}: {accounts[username]}")
    else:
        print("Account not found.")

# Registry modification to allow multiple Roblox instances
def set_registry(temp_folder):
    key_path = r"SOFTWARE\Roblox Corporation\Environments\roblox-player"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "LaunchTime", 0, winreg.REG_SZ, temp_folder)

def launch_client(username, temp_folder):
    os.makedirs(temp_folder, exist_ok=True)
    set_registry(temp_folder)
    subprocess.Popen([ROBLOX_PLAYER_PATH])
    print(f"Launched Roblox client for {username}")

def launch_multiple_clients():
    accounts = load_accounts()
    if not accounts:
        print("No accounts available. Add accounts first.")
        return
    
    temp_base_path = r"C:\TempRobloxSessions"
    os.makedirs(temp_base_path, exist_ok=True)

    for i, username in enumerate(accounts):
        temp_folder = os.path.join(temp_base_path, f"session_{i}")
        launch_client(username, temp_folder)
        time.sleep(1)

# Main program loop
def main():
    while True:
        print("\nRoblox Account Manager")
        print("1. Add Account")
        print("2. Remove Account")
        print("3. View Accounts")
        print("4. Retrieve Password")
        print("5. Launch Multiple Clients")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_account()
        elif choice == "2":
            remove_account()
        elif choice == "3":
            view_accounts()
        elif choice == "4":
            retrieve_password()
        elif choice == "5":
            launch_multiple_clients()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
