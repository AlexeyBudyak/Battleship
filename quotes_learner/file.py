from os import listdir

class Dir:
    def __init__(self):
        self.txt_files = list(filter(lambda f_name: f_name[-4:] == '.txt', listdir('.')))
    def __str__(self):
        return "\n".join([f"{i+1}. {f}" for i,f in enumerate(self.txt_files)])

def input_filename(files):
    filename = ''
    while filename not in files:
        filename = input('Enter file name or file number (0 - for exit) ').lower()
        if filename == '0':
            return -1
        if filename.isdigit() and int(filename) - 1 in range(len(files)):
            filename = files[int(filename) - 1]
        if '.' not in filename:
            filename+= '.txt'
    return filename

class File:
    def __init__(self):
        self.dir = Dir()
        self.name = ''
        self.text = ''
    def pick_file(self):
        print(self.dir)
        print()
        self.name = input_filename(self.dir.txt_files)
    def load(self):
        file = open(self.name, "r")
        self.text = file.read()
        file.close()
        return self.text
    def __str__(self):
        return "\n".join(self.text.split('\n')[::2])
