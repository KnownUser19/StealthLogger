from cryptography.fernet import Fernet

key = " DdV1rNJ0ujTkZK00Xfd60Sq0Qa5T3-z8EEErhE425kI= "

system_information_e = "e_system.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_keys.txt"
audio_information_e = "e_audio.txt"
screenshot_e = "e_screenshot.txt"


encrypted_files = [ system_information_e, clipboard_information_e, keys_information_e, audio_information_e, screenshot_e]
count = 0


for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()
            
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
        
        with open(encrypted_files[count], 'wb') as f:
            f.write(decrypted)
            
        count += 1
        

