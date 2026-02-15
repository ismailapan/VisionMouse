import os
import subprocess

path = '"C:/Windows/WinSxS/amd64_microsoft-windows-osk_31bf3856ad364e35_10.0.26100.7824_none_465523d50a146704/osk.exe"'

def open_osk():
    try:
        subprocess.Popen(path, shell=True)
    except Exception as e:
        print(f"Klavye açılmadı.", {e})

def close_osk():
    os.system("taskkill /f /im osk.exe")
