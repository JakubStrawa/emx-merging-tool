
class FileReader:
    def __init__(self, filepath, line=1, position=0):
        self.filepath = filepath
        self.file = open(filepath, 'r', encoding='utf-8', errors='replace')
        self.line = line
        self.position = position
        self.eof = False

    def get_char(self):
        self.file.seek(self.position)
        c = self.file.read(1)
        self.position += 1
        return c

    def peek(self):
        temp_position = self.file.tell()
        c = self.file.read(1)
        tmp = c
        while c != '"':
            c = self.file.read(1)
            tmp += c
        self.file.seek(temp_position)
        return tmp

    def is_eof(self):
        if not self.file.readline():
            self.eof = True
            return True
        else:
            return False