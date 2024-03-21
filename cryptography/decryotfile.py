from cryptography.fernet import Fernet
key =  "TXVJkGQ50pJpSB25aQmUk7paTyVGYbYMIW_Y4udzl7Q="


keys_information_e = "enc_key_log.txt"
system_information_e = "enc_systeminfo.txt"
clipboard_information_e = "enc_clipboard.txt"

encrypted_files = [system_information_e,clipboard_information_e,keys_information_e]
count = 0

for decrypting_files in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)
    count += 1