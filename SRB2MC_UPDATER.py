'''
# SRB2ModCompiler-Updater v1.2 by Lumyni (felixlumyni on discord)
# Requires https://www.python.org/
# Messes w/ files, only edit this if you know what you're doing!
'''

import os
import re
import shutil
import sys
try:
    import requests
except ModuleNotFoundError:
    response = input("The 'requests' module is not installed. Would you like to install it now? (y/n)")

    if response == 'y':
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        input("Installation complete. Press enter to restart the script.")
        subprocess.run([sys.executable] + sys.argv)
        sys.exit()
    else:
        print("Cannot continue without 'requests'. Please install it by using 'pip install requests'.")
        sys.exit(1)

class ScriptUpdater:
    def __init__(self, scripts):
        """
        Initialize the updater with a list of scripts to check and update.

        :param scripts: List of dictionaries, each containing:
            - "name": Script display name (for user prompts)
            - "local_path": Path to the local script file
            - "remote_url": Raw GitHub URL of the script
        """
        self.scripts = scripts

    def extract_version(self, text):
        """Extract version number from script header using regex."""
        match = re.search(r'v(\d+)(?:\.(\d+))?', text)  # Matches vX or vX.Y
        if match:
            major = int(match.group(1))
            minor = int(match.group(2)) if match.group(2) else 0  # Default to 0 if missing
            return major, minor
        return None

    def get_local_version(self, script_path):
        """Read the local script and extract its version, or return None if missing."""
        if not os.path.exists(script_path):
            print(f"☑️ {script_path} is missing. It will be downloaded.")
            return None  # Triggers auto-download

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                first_lines = "".join([f.readline() for _ in range(5)])  # Read first few lines
            return self.extract_version(first_lines)
        except Exception as e:
            print(f"⚠️ Error reading {script_path}: {e}")
            return None

    def get_remote_version(self, remote_url):
        """Fetch the latest script from GitHub and extract its version."""
        try:
            response = requests.get(remote_url, timeout=5)
            if response.status_code == 200:
                return self.extract_version(response.text)
        except requests.RequestException as e:
            #print(f"⚠️ Error fetching {remote_url.rsplit("/",1)[-1]}: {e}")
            print(f"⚠️  Error fetching {remote_url.rsplit("/",1)[-1]}. Check internet connection?")
        return None

    def update_script(self, script):
        """Download and replace the local script, handling backups properly."""
        remote_url = script["remote_url"]
        local_path = script["local_path"]
        backup_path = local_path + ".bak"

        print(f"🔄 Downloading update for {script['name']}...")

        try:
            response = requests.get(remote_url, timeout=5)
            if response.status_code == 200:
                # Backup existing file before updating
                if os.path.exists(local_path):
                    shutil.copy(local_path, backup_path)

                # Write new script, ensuring proper line endings
                with open(local_path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(response.text.replace("\r\n", "\n"))

                print(f"✅ {script['name']} updated successfully!")

                # If update succeeded, delete the backup
                if os.path.exists(backup_path):
                    os.remove(backup_path)

                return True

        except requests.RequestException as e:
            print(f"❌ Update failed: {e}")

            # Restore from backup if something went wrong
            if os.path.exists(backup_path):
                print(f"🔄 Restoring {script['name']} from backup...")
                shutil.copy(backup_path, local_path)
                print(f"✅ {script['name']} restored from backup.")
            else:
                print(f"⚠️ No backup available. {script['name']} was not updated.")

        return False

    def check_for_updates(self):
        """Check all scripts for updates OR install missing ones."""
        updates_needed = []
        failed = False

        for script in self.scripts:
            print(f"🔎 Checking {script['name']}...")

            local_version = self.get_local_version(script["local_path"])
            remote_version = self.get_remote_version(script["remote_url"])

            if not remote_version:
                print(f"❌ Could not fetch remote version for {script['name']}.\n")
                failed = True
                continue

            if local_version is None or remote_version > local_version:
                if os.path.basename(script["local_path"]) == os.path.basename(sys.argv[0]):
                    print(f"⚠️  I am outdated! Please replace me with: {script['remote_url']}\n")
                    input("Press Enter to continue...")
                else:
                    print(f"🚀 {script['name']} is missing or outdated! New version: v{remote_version[0]}.{remote_version[1]}\n")
                    updates_needed.append(script)

        if not updates_needed:
            if not failed:
                print("✅ All scripts are up to date.")
            return

        choice = input("Would you like to install/update these scripts? (y/n): ").strip().lower()
        if choice != 'y':
            print("❌ Update canceled.")
            return

        for script in updates_needed:
            self.update_script(script)


# Example usage
if __name__ == "__main__":
    scripts_to_check = [
        {
            "name": "SRB2 Mod Compiler",
            "local_path": "SRB2C.py",
            "remote_url": "https://raw.githubusercontent.com/felixLumyni/SRB2ModCompiler2/refs/heads/main/SRB2C.py"
        },
        {
            "name": "SRB2 Mod Compiler (Simple)",
            "local_path": "SRB2MC_SIMPLE.pyw",
            "remote_url": "https://raw.githubusercontent.com/felixLumyni/SRB2ModCompiler2/refs/heads/main/SRB2MC_SIMPLE.pyw"
        },
        {
            "name": "SRB2 Mod Compiler Updater",
            "local_path": sys.argv[0],
            "remote_url": "https://raw.githubusercontent.com/felixLumyni/SRB2ModCompiler2/refs/heads/main/SRB2MC_UPDATER.py"
        }
    ]

    updater = ScriptUpdater(scripts_to_check)
    updater.check_for_updates()
    import time
    time.sleep(2)
