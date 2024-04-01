# SRB2ModCompiler v2
A python script that enhances your [SRB2](https://www.srb2.org/) modding workflow!

## How do I download just the script?
View it here in github -> Raw -> Right Click -> Save as file

## Why is this helpful?
- Most importantly, it automates the process of saving your mod to a PK3, opening the game and loading your mod every time you want to test it
- While compressed files - such as ZIP/WAD/PK3 - can be uploaded with git, you can't keep track of development (like which files were added, removed or modified in each commit/version)
- Having your mod outside of a compressed file also allows mods to be edited more comfortably with apps other than [SLADE](https://github.com/sirjuddington/SLADE), I personally recommend [VS Code](https://code.visualstudio.com/), since it can run this script AND edit your mods like SLADE.

## How to use this to test your mod
- Drag and drop the .py file inside of the mod files
- Run the .py file with [Python](https://www.python.org/) or [Visual Studio Code](https://code.visualstudio.com/), a terminal should open
- If you haven't yet, tell it where your SRB2.exe is with the 'set' command
- Afterwards, everytime you simply press enter, it will:
  - Make a pk3 file containing the contents (excluding some files, such as git files and itself) of the directory the script is located at (it will also use that to determine the name of the file). By default, this newly made pk3 will be located in your SRB2 directory, but it can be changed with the command 'downloads'
  - Open your SRB2
  - Skip the intro
  - Load your mod
  - And wish you a happy testing session!
