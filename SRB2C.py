'''
# SRB2ModCompiler v2.1 by Lumyni (felixlumyni on discord)
# Requires https://www.python.org/
# Messes w/ files, only edit this if you know what you're doing!
'''

import os
import platform
import subprocess
if platform.system() == "Windows": import winreg
import datetime
#for zipping:
import io
import zipfile

runcount = 0

def main():
    vscode = 'TERM_PROGRAM' if 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode' else ''
    RED = '\033[31m' if vscode else ''
    GREEN = '\033[32m' if vscode else ''
    BLUE = '\033[36m' if vscode else ''
    RESETCOLOR = '\033[0m' if vscode else ''
    set = GREEN+"set" if get_environment_variable("SRB2C_LOC") else RED+"unset"
    print(BLUE, end="")
    print(f"Welcome to SRB2ModCompiler v2! Your system variable is {set}{BLUE}.")
    print(f"Type '{GREEN}help{BLUE}' to see available commands.")
    
    while True:
        command = input(RESETCOLOR+"> ").lower()
        print(BLUE, end="")

        if command == "help":
            print("Available commands:")
            print(f"  {GREEN}<literally nothing>{BLUE} - Compile this script's directory into a mod and run it in your exe from the system variable!")
            print(f"  {GREEN}set{BLUE} - Update the system variable that (necessary so this script knows where your SRB2 is)")
            print(f"  {GREEN}path{BLUE} - Show the paths for both system variables")
            print(f"  {GREEN}downloads{BLUE} - Update the secondary and optional system variable that determines where your files will be saved")
            print(f"  {GREEN}args{BLUE} - Update your launch parameters as a file! (also optional)")
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
            set_environment_variable("SRB2C_DL", None)
            print("Unset SRB2C_LOC and SRB2C_DL variables.")
        elif command == "args":
            print("- Used to launch the game with special settings. DEFAULT: -skipintro")
            print("- NOTE: Regardless of what parameters you type in here, the script will always use the -file <MOD> parameter to run your mod")
            print('- Example: -skipintro -server +skin Tails +color Rosy +wait 1 -warp tutorial +downloading off')
            print("- (If you're still confused, refer to the 'command line parameters' page from the SRB2 Wiki)")
            print("- If you wish to cancel, simply press enter without typing anything")
            command = input(RESETCOLOR+">> ").lower()
            print(BLUE, end="")
            if command == "":
                print("Operation cancelled by user.")
            else:
                params = []
                params.extend(command.split())
                script_dir = os.path.dirname(os.path.abspath(__file__))
                filename = ".SRB2C_ARGS"
                filepath = os.path.join(script_dir, filename)
                with open(filepath, "w") as file:
                    for i, param in enumerate(params):
                        file.write(param)
                        if i != len(params) - 1:
                            file.write(" ")
                print(filename,"file was created/updated (in the same directory as this script)!")
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
            BLACK = '\033[30m' if vscode else ''
            print(BLACK+"Who are you running from?"+BLUE)
        elif command == "cls":
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
        else:
            print(f"Invalid command. Type '{GREEN}help{BLUE}' to see available commands.")

def run():
    """
    I'm adding this comment because this function does a lot of things:
    - Requires the enviroment variable ``SRB2C_LOC``, which points to the user's SRB2 executable (if not provided, will return a warning)
    - Tries to read the ``.SRB2C_ARGS`` file (in the same directory as this script) and store its contents as launch parameters.
        - If the file is not found, it will default to ``-skipintro``
    - It will zip the current directory in the ``SRB2C_DL`` enviroment variable
        - If the variable is not found, the zip file will be stored in the same place as ``SRB2C_LOC``
    - After the zip file has been created/updated, it will then run the SRB2 executable in ``SRB2C_LOC``, with the ``-file`` parameter to run it
    - Aditionally, this will print useful information such as runcount and datetime
    """
    global runcount
    srb2_loc = get_environment_variable("SRB2C_LOC")
    srb2_dl = get_environment_variable("SRB2C_DL") if get_environment_variable("SRB2C_DL") else os.path.dirname(srb2_loc)
    vscode = 'TERM_PROGRAM' if 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode' else ''
    if srb2_loc:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # NOW! *thunder*
        gonnarun = True
        currentdir = os.path.dirname(__file__)
        basedirname = os.path.basename(currentdir)
        pk3name = "_"+basedirname+".pk3"
        try:
            with open(os.path.join(currentdir, ".SRB2C_ARGS"), "r") as file:
                extraargs = file.read().split()
                if runcount == 0:
                    BLUE = '\033[36m' if vscode else ''
                    GREEN = '\033[32m' if vscode else ''
                    print(f"[{now}] Found {GREEN}.SRB2C_ARGS{BLUE} file")
        except FileNotFoundError:
            if runcount == 0:
                BLUE = '\033[36m' if vscode else ''
                GREEN = '\033[32m' if vscode else ''
                print(f"[{now}] {GREEN}.SRB2C_ARGS{BLUE} file not found, so we will be using the default parameter: {GREEN}-skipintro{BLUE}")
            extraargs = ["-skipintro"]
        args = [srb2_loc, "-file", pk3name]
        args.extend(extraargs)
        if runcount == 0:
            print(f"- Zipping '{GREEN}{basedirname}{BLUE}', please wait a moment...")
        create_or_update_zip(currentdir, srb2_dl, pk3name)
        if os.path.exists(os.path.join(srb2_dl, pk3name)):
            if runcount == 0:
                specified = "specified" if get_environment_variable("SRB2C_DL") else "SRB2"
                print(f"- '{GREEN}"+pk3name+f"{BLUE}' (This script's directory) was created/updated in your {specified} directory")
                print("- Running SRB2 with that mod. Happy testing!")
            else:
                print(f"[{now}] Running test #{runcount+1}...")
        else:
            RED = '\033[31m' if vscode else ''
            BLUE = '\033[36m' if vscode else ''
            print(f"{RED}ERROR:{BLUE} Pk3 not detected, maybe I don't have file writing permissions?")
            gonnarun = False
        if gonnarun:
            subprocess.run(args, cwd=os.path.dirname(srb2_loc))
            runcount = runcount + 1
    else:
        GREEN = '\033[32m' if vscode else ''
        RESETCOLOR = '\033[0m' if vscode else ''
        print(f"SRB2C_LOC system variable not set. Please run '{GREEN}set{RESETCOLOR}' to set it.")

def get_environment_variable(variable: str):
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
        return os.environ.get(variable)

    return sysvar

def set_environment_variable(variable: str|None, value: str|None):
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

def file_explorer(file_types: list):
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename(filetypes=file_types)

    root.destroy()

    return file_path

def directory_explorer():
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    directory_path = filedialog.askdirectory()

    root.destroy()

    return directory_path

def create_or_update_zip(source_path: str, destination_path: str, zip_name: str):
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
                        if rel_path in existing_zip.namelist():
                            # Read the existing file from the zip archive
                            with existing_zip.open(rel_path) as existing_file:
                                existing_file_data = existing_file.read()
                            # Read the source file data
                            with open(source_file_path, 'rb') as source_file:
                                source_file_data = source_file.read()

                            # Compare files and update if needed
                            if existing_file_data != source_file_data:
                                temp_zip.writestr(rel_path, source_file_data)
                        else:
                            # If the file is not in the existing zip, add it
                            with open(source_file_path, 'rb') as source_file:
                                temp_zip.writestr(rel_path, source_file.read())

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