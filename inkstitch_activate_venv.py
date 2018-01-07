import os

if __name__ == "__main__":
    if os.path.isdir("inkstitch-venv"):
        activate = os.path.join("inkstitch-venv", "bin", "activate_this.py")
        execfile(activate, dict(__file__=activate))
