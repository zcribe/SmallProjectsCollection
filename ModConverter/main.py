import os
import zipfile
import tempfile

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


mod_folder = "F:\\Steam\\steamapps\\workshop\\content\\281990"


with cd(mod_folder):
    mods = os.listdir()
    for folder in mods:
        specific_mod_dir = "\\".join([mod_folder, folder])
        with cd(specific_mod_dir):
            current_files = os.listdir()
            try:
                with zipfile.ZipFile(current_files[0], "r")as myzip:
                    myzip.extract("descriptor.mod", path=)
            except IndexError:
                pass
