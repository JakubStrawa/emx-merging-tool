
class FileReader:
    def __init__(self, filepath, line=1, position=1):
        self.filepath = filepath
        self.file = open(filepath, 'r')
        self.line = line
        self.position = position
        self.eof = False

    def get_char(self):
        return self.file.read(1)

    def peek(self):
        pass

    def is_eof(self):
        if not self.file.readline():
            self.eof = True
            return True
        else:
            return False