import glob
import os
import sys


class FileRenamer:
    def __init__(self):
        self.this = ""
        self.that = ""
        self.selection = []
        self.file_counter = 0

    def run(self):
        self.read_arguments()
        self.select_files()
        self.rename_files()
        self.report_results()

    def read_arguments(self):
        arguments = sys.argv
        if len(arguments) < 3:
            print("Usage: this that")
        else:
            self.this = arguments[1]
            self.that = arguments[2]

    def select_dir(self, change_to):
        os.chdir(change_to)

    def select_files(self):
        self.selection = glob.glob(f"*.{self.this}")
        if not self.selection:
            print("No suitable files found.")

    def rename_files(self):
        for file in self.selection:
            new_name = file.replace(self.this, self.that)
            os.rename(file, new_name)
            self.file_counter += 1

    def report_results(self):
        if self.file_counter == 0:
            print("No files renamed.")
        elif self.file_counter == 1:
            print(f"{self.file_counter} file renamed.")
        else:
            print(f"{self.file_counter} files renamed.")


if __name__ == "__main__":
    FileRenamer().run()
