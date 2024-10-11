# SRB2ModCompiler v2
A python script that enhances your [SRB2](https://www.srb2.org/) modding workflow!

## How do I download just the script?
View it here in github -> Raw -> Right Click -> Save as file

## Why is this helpful?
- Most importantly, it automates the process of saving your mod to a PK3, opening the game and loading your mod every time you want to test it
- While compressed files - such as ZIP/WAD/PK3 - can be uploaded with git, you can't keep track of development (like which files were added, removed or modified in each commit/version)
- Having your mod outside of a compressed file also allows mods to be edited more comfortably with apps other than [SLADE](https://github.com/sirjuddington/SLADE), I personally recommend [VS Code](https://code.visualstudio.com/), since it can run this script AND edit your mods like SLADE.

## How to use this to test your mod
- If your mod is in a compressed file, extract it to a folder with the ``unzip`` command
- Drag and drop the .py file inside of the mod files, it should look something like [this](https://github.com/user-attachments/assets/b7f05909-e80d-4d2e-a339-4baa9795f128)
- Run the .py file with [Python](https://www.python.org/) or [Visual Studio Code](https://code.visualstudio.com/), a terminal should open
- If you haven't yet, tell it where your SRB2.exe is with the ``set`` command
- Afterwards, everytime you simply press enter on the terminal (without a command), this script will automatically compile your mod and launch your game with it

<details><summary><b>What do you mean it "compiles" my mod?</b></summary>

- It makes a pk3 file containing the contents (excluding some files, such as git files and itself) of the directory the script is located at (it will also use that to determine the name of the file). By default, this newly made pk3 will be located in (exe's dir)/DOWNLOAD/_srb2compiled, but it can be changed with the ``downloads`` command
- Opens your SRB2 executable
- Skips the intro
- Loads your mod (with custom parameters if you've used the ``args`` command)
- And wishes you a happy testing session!

</details>
