from cryptography.fernet import Fernet
import json
import os

# Generate a new encryption key or load an existing one
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

# Save account information to encrypted file
def save_accounts(accounts):
    encrypted_data = cipher.encrypt(json.dumps(accounts).encode())
    with open("accounts.db", "wb") as f:
        f.write(encrypted_data)

# Load account information from encrypted file
def load_accounts():
    if not os.path.exists("accounts.db"):
        return {}
    with open("accounts.db", "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

# Add new account
def add_account():
    username = input("Enter the Roblox username: ")
    password = input("Enter the Roblox password: ")

    accounts = load_accounts()
    accounts[username] = password
    save_accounts(accounts)
    print(f"Account for {username} added successfully!")

# Remove an account
def remove_account():
    username = input("Enter the username to remove: ")

    accounts = load_accounts()
    if username in accounts:
        del accounts[username]
        save_accounts(accounts)
        print(f"Account for {username} removed successfully!")
    else:
        print("Account not found.")

# View all accounts
def view_accounts():
    accounts = load_accounts()
    if accounts:
        print("\nStored Accounts:")
        for username in accounts:
            print(f"- {username}")
    else:
        print("No accounts stored.")

# Retrieve password for an account
def retrieve_password():
    username = input("Enter the username to retrieve password for: ")

    accounts = load_accounts()
    if username in accounts:
        print(f"Password for {username}: {accounts[username]}")
    else:
        print("Account not found.")

# Main program loop
def main():
    while True:
        print("\nRoblox Account Manager")
        print("1. Add Account")
        print("2. Remove Account")
        print("3. View Accounts")
        print("4. Retrieve Password")
        print("5. Exit")
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
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
