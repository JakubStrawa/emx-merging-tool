
# basic file reader with get_char method

class FileReader:
    def __init__(self, filepath, line=1, position=0):
        self.filepath = filepath
        self.file = open(filepath, 'r', encoding='utf-8', errors='replace')
        self.line = line
        self.position = position
        self.skip_file_header()


    def get_char(self):
        self.file.seek(self.position)
        c = self.file.read(1)
        self.position += 1
        if c == '\n':
            self.line += 1
        return c

    def skip_file_header(self):
        for i in range(5):
            line = self.file.readline()
            self.position += len(line)
            self.line += 1

    def close_file(self):
        self.file.close()