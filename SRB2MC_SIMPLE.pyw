'''
# SRB2ModCompiler-Simple v1 by Lumyni (felixlumyni on discord)
# Requires https://www.python.org/
# Messes w/ files, only edit this if you know what you're doing!
'''

def attempt(func, arg, messagebox):
    try:
        func(arg)
    except Exception as e:
        messagebox.showerror(
            title="Error",
            message=f"{str(e)}"
        )


def main():
    import sys
    from tkinter import messagebox
    sys.dont_write_bytecode = True  
    import SRB2C

    srb2_loc = SRB2C.get_environment_variable("SRB2C_LOC")
    
    if srb2_loc and SRB2C.sanitized_exe_filepath(srb2_loc):
        attempt(SRB2C.run, True, messagebox)
    else:
        message = "SRB2 executable not found.\nClick OK to locate it and run."
        if messagebox.askokcancel("SRB2ModCompiler", message):
            srb2_path = SRB2C.choose_srb2_executable()
            if srb2_path:
                attempt(SRB2C.run, True, messagebox)

if __name__ == "__main__":
    main()