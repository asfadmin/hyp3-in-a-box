import os
import subprocess


def install_all_requirements_txts(root_dir):
    for path, dirs, files in os.walk(root_dir):
        for name in files:
            if "requirements" in name and name.endswith('.txt'):
                subprocess.check_call(
                    ["pip", "install", "-U", "-r", name],
                    cwd=path
                )


if __name__ == "__main__":
    install_all_requirements_txts(os.getcwd())
