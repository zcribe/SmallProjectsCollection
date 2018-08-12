import os
import zipfile
import shutil

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
descriptor_folder = "C:\\Users\\Erlend\\Documents\\Paradox Interactive\\Stellaris\\mod"

# TODO: Muuda funktsiooniks
with cd("C:\\Users\\Erlend\\Documents\\Paradox Interactive\\Stellaris\\mod"):
    files = os.listdir()
    for i in files:
        os.remove(i)

with cd(mod_folder): # TODO: Halb stack cd kasutus
    mods = os.listdir()
    for folder in mods:
        specific_mod_dir = "\\".join([mod_folder, folder])
        with cd(specific_mod_dir):
            current_files = os.listdir() # TODO: Puruneb kui mingi muu fail on kohvris
            new_filename = ""
            try:
                new_filename = "".join([folder, ".mod"])
                with zipfile.ZipFile(current_files[0], "r")as myzip:
                        myzip.extract("descriptor.mod")

                mod_path = "\\".join(["workshop\\content\\281990\\LinkedDir", folder, current_files[0]]).replace("\\", "/")

                f = open("descriptor.mod", "r+", encoding="utf-8-sig")
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i == 'archive="{}"\n'.format(current_files[0]):
                        f.write('path="{}"\n'.format(mod_path))
                    else:
                        f.write(i)
                f.truncate()
                f.close()

                os.rename("descriptor.mod", new_filename)
                shutil.move("\\".join([specific_mod_dir, new_filename]), descriptor_folder )
            except IndexError:
                pass
            except zipfile.BadZipFile:
                os.remove(new_filename)
                print("Multiple files in the folder or not a zip file {}".format(folder))
            except shutil.Error:
                with cd(descriptor_folder):
                    files = os.listdir()
                    for i in files:
                        os.remove(i)
