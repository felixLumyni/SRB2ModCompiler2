# SRB2ModCompiler v2
A python script that enhances your [SRB2](https://www.srb2.org/) modding workflow!

<details><summary><b>Why is this helpful?</b></summary>

- Most importantly, it automates the process of saving your mod's assets into a <span title=" The file type SRB2 expects for loading mods. It's just a renamed zip file." style="border-bottom:1px dotted; cursor: help;">pk3</span>, opening the game and loading your mod every time you want to test it
- While <span title="ZIP, WAD, or PK3's" style="border-bottom:1px dotted; cursor: help;">compressed files</span> can be uploaded to <span title="Version control platforms. GitHub, GitLab, Codeberg, you name it." style="border-bottom:1px dotted; cursor: help;">git</span>, you can't <span title="like seeing exactly which lines of which files were modified in each version" style="border-bottom:1px dotted; cursor: help;">keep track of development</span> reliably
- Having your mod outside of a compressed file also allows mods to be edited more comfortably with apps other than [SLADE](https://github.com/sirjuddington/SLADE). I personally recommend [VS Code](https://code.visualstudio.com/), since it can run this script *and* edit your lua files.
### TL;DR: 
```
This is tool is meant to make writing and testing code more convenient. With that said, you'll still probably rely on SLADE for graphics/sprite editing.
```
</details>

---

<details><summary><b>How do I download the script from GitHub?</b></summary>
View -> Raw -> Right Click -> Save as file

</details>

---

<details><summary><b>I ran the script, but I'm lost. How do I set this up?</b></summary>

- Run the script with [Python](https://www.python.org/) or [Visual Studio Code](https://code.visualstudio.com/), a terminal should open
- **(Skip if your mod's assets are not zipped)** Use the ``unzip`` command
- **(Skip if you use the ``mod`` command)** Move the script to the mod's assets, it should look something like [this](https://github.com/user-attachments/assets/b7f05909-e80d-4d2e-a339-4baa9795f128)
- **(Skip if your SRB2 is in flatpak)** If you haven't yet, tell it where your SRB2.exe is with the ``set`` command

You're done! Now, every time you simply <span title="without any commands" style="border-bottom:1px dotted; cursor: help;">press enter</span> on the script's terminal (or when you run the simple version), this script will automatically "compile" your mod and launch your game with it
</details>

---

<details><summary><b>What do you mean it "compiles" my mod? Is it customizable?</b></summary>

- It makes a pk3 file containing the contents (excluding some files, such as git files and itself) of the directory the script is located at (it will also use that to determine the name of the file).

By default, this newly made pk3 is made in <span title="(exe's dir)/DOWNLOAD/_srb2compiled" style="border-bottom:1px dotted; cursor: help;">DOWNLOAD</span>, but it can be changed with the ``downloads`` command
- Opens your SRB2 executable
- Skips the intro
- Loads your mod (with custom parameters if you've used the ``args`` command)
- And wishes you a happy testing session!

</details>

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.