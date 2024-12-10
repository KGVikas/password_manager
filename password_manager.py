from cryptography.fernet import Fernet

# Load the encryption key from file
def load_key():
    try:
        with open('key.key', 'rb') as file:
            key = file.read()
        return key
    except FileNotFoundError:
        print("Key file not found! Please ensure 'key.key' exists.")
        exit()

# Initialize the Fernet encryption object
key = load_key()
fer = Fernet(key)

# Uncomment the below function if you need to create a new key
'''
def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
'''

# Function to view stored passwords
def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, password = data.split('|')
                try:
                    decrypted_password = fer.decrypt(password.encode()).decode()
                    print(f'User: {user} | Password: {decrypted_password}')
                except Exception as e:
                    print(f"Error decrypting password for {user}: {e}")
    except FileNotFoundError:
        print("Password file not found. You haven't stored any passwords yet.")

# Function to add a new password
def add():
    name = input('Account name: ')
    while True:
        pwd = input('Enter your password: ')
        pwdr = input('Re-enter your password: ')
        if pwdr == pwd:
            with open('passwords.txt', 'a') as f:
                encrypted_password = fer.encrypt(pwd.encode()).decode()
                f.write(f'{name}|{encrypted_password}\n')
            print("Password added successfully.")
            break
        else:
            print("The passwords do not match! Please try again.")

# Main loop for user interaction
while True:
    mode = input('Would you like to add a new password or view the existing ones (add/view)? Or press q to quit: ').lower()
    
    if mode == 'q':
        print("Exiting the program. Goodbye!")
        break
    elif mode == 'add':
        add()
    elif mode == 'view':
        view()
    else:
        print('Invalid option! Please enter "add", "view", or "q".')
