'''
# SRB2Compiler v2-PRERELEASE by Lumyni (felixlumyni on discord)
# Requires https://www.python.org/ and https://www.7-zip.org/
# Messes w/ files, only edit this if you know what you're doing!
'''

import os
import platform
import subprocess
if platform.system() == "Windows": import winreg
#for zipping:
import io
import zipfile
import filecmp

def main():
    vscode = 'TERM_PROGRAM' if 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode' else ''
    RED = '\033[31m' if vscode else ''
    GREEN = '\033[32m' if vscode else ''
    BLUE = '\033[36m' if vscode else ''
    RESETCOLOR = '\033[0m' if vscode else ''
    set = GREEN+"set" if get_environment_variable("SRB2C_LOC") else RED+"unset"
    print(BLUE, end="")
    print(f"Welcome to SRB2Compiler v2! Your system variable is {set}{BLUE}.")
    print(f"Type '{GREEN}help{BLUE}' to see available commands.")
    
    while True:
        command = input(RESETCOLOR+"> ").lower()
        print(BLUE, end="")

        if command == "help":
            print("Available commands:")
            print(f"  {GREEN}<literally nothing>{BLUE} - Compile this script's directory into a mod and run it in your exe from the system variable!")
            print(f"  {GREEN}path{BLUE} - Show the paths for the system variables")
            print(f"  {GREEN}set{BLUE} - Update the system variable")
            print(f"  {GREEN}downloads{BLUE} - Update the secondary and optional system variable that determines where your files will be saved")
            print(f"  {GREEN}quit{BLUE} - Exit the program")
        elif command == "path":
            srb2_loc = get_environment_variable("SRB2C_LOC")
            srb2_dl = get_environment_variable("SRB2C_DL")
            print(f"SRB2C_LOC system variable path: {srb2_loc}")
            print(f"SRB2C_DL system variable path: {srb2_dl}")
        elif command == "set":
            choose_srb2_executable()
        elif command == "downloads":
            choose_srb2_downloads()
        elif command == "unset":
            set_environment_variable("SRB2C_LOC", None)
            print("Unset SRB2C_LOC variable.")
        elif command == "quit":
            break
        elif command == "":
            run()
        elif command == "nothing":
            print("stop it.")
        elif command == "<literally nothing>":
            print("BRUH LOL")
            print("You know what I meant.")
        elif command == "run":
            print("\033[30m"+"Who are you running from?"+BLUE)
        elif command == "cls":
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
        else:
            print(f"Invalid command. Type '{GREEN}help{BLUE}' to see available commands.")

def run():
    srb2_loc = get_environment_variable("SRB2C_LOC")
    srb2_dl = get_environment_variable("SRB2C_DL") if get_environment_variable("SRB2C_DL") else os.path.dirname(srb2_dl)
    if srb2_loc:
        currentdir = os.path.dirname(__file__)
        basedirname = os.path.basename(currentdir)
        pk3name = "_"+basedirname+".pk3"
        create_or_update_zip(currentdir, srb2_dl, pk3name)
        if os.path.exists(os.path.join(srb2_dl, pk3name)):
            print(pk3name+" (This script's directory) was created/updated in your SRB2 directory!")
            print("Running SRB2 with that mod. Happy testing!")
            args = [srb2_loc,"-skipintro","-file",pk3name]
            subprocess.Popen(args, cwd=os.path.dirname(srb2_loc))
        else:
            print("Hm... I couldn't detect a pk3 file, maybe I don't have file writing permissions?")
            print("Running SRB2 anyway.")
            args = [srb2_loc, "-skipintro", "-file", pk3name]
            subprocess.Popen(args, cwd=os.path.dirname(srb2_loc))
    else:
        print("SRB2C_LOC system variable not set. Please run 'set' to set it.")

def get_environment_variable(variable):
    sysvar = os.getenv(variable)

    if platform.system() == "Windows":
        # On Windows, manually refresh os.environ after modifying the registry
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_READ)
        try:
            sysvar, _ = winreg.QueryValueEx(key, variable)
        except FileNotFoundError:
            pass
        finally:
            winreg.CloseKey(key)
    else:
        os.environ[variable] = sysvar

    return sysvar

def set_environment_variable(variable, value):
    if platform.system() == "Windows":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, variable, 0, winreg.REG_EXPAND_SZ, value)
        winreg.CloseKey(key)
    else:
        os.environ[variable] = value

def choose_srb2_executable():
    ext = "Do keep in mind your current path will be overwritten!" if get_environment_variable("SRB2C_LOC") else ""

    print(f"Please select the SRB2.exe file. {ext}")
    file_types = [("Executable files", "*.exe")]
    srb2_path = file_explorer(file_types)

    if srb2_path:
        set_environment_variable("SRB2C_LOC", srb2_path)
        print("SRB2C_LOC system variable updated! Now just press enter to run it.")
    else:
        print("Operation cancelled by user.")

    return srb2_path

def choose_srb2_downloads():
    ext = "Do keep in mind your current path will be overwritten!" if get_environment_variable("SRB2C_DL") else ""

    print(f"Please select the directory for SRB2 downloads. {ext}")
    srb2_downloads_path = directory_explorer()

    if srb2_downloads_path:
        set_environment_variable("SRB2C_DL", srb2_downloads_path)
        print("SRB2C_DL system variable updated! Now this is where your pk3's will be saved.")
    else:
        print("Operation cancelled by user.")

    return srb2_downloads_path

def file_explorer(file_types):
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=file_types)

    root.destroy()

    return file_path

def directory_explorer():
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()

    directory_path = filedialog.askdirectory()

    root.destroy()

    return directory_path

def create_or_update_zip(source_path, destination_path, zip_name):
    zip_full_path = os.path.join(destination_path, zip_name)

    # Check if the destination zip file already exists
    if os.path.exists(zip_full_path):
        # Read the existing zip file into memory
        with open(zip_full_path, 'rb') as existing_zip_file:
            existing_zip_data = io.BytesIO(existing_zip_file.read())

        # Create a temporary in-memory zip file
        temp_zip_data = io.BytesIO()

        # Compare source files with existing zip contents
        with zipfile.ZipFile(existing_zip_data, 'r') as existing_zip, zipfile.ZipFile(temp_zip_data, 'a') as temp_zip:
            for root, _, files in os.walk(source_path):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(source_file_path, source_path)

                    # Exclude this script and git files
                    if not (file.endswith('.py') or file.endswith('.md') or file.endswith('LICENSE') or file.startswith('.') or '.git' in rel_path):
                        # Compare files and update if needed
                        if rel_path in existing_zip.namelist() and not filecmp.cmp(source_file_path, existing_zip.extract(rel_path)):
                            temp_zip.write(source_file_path, rel_path)
                        elif rel_path not in existing_zip.namelist():
                            temp_zip.write(source_file_path, rel_path)

        # Update the destination zip file with the modified contents
        with open(zip_full_path, 'wb') as updated_zip_file:
            updated_zip_file.write(temp_zip_data.getvalue())

    else:
        # If the destination zip file doesn't exist, create a new one
        with zipfile.ZipFile(zip_full_path, 'w') as new_zip:
            for root, _, files in os.walk(source_path):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(source_file_path, source_path)

                    # Exclude this script and git files
                    if not (file.endswith('.py') or file.endswith('.md') or file.endswith('LICENSE') or file.startswith('.') or '.git' in rel_path):
                        new_zip.write(source_file_path, rel_path)

if __name__ == "__main__":
    main()