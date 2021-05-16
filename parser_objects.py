import tokens.token

class Model:
    def __init__(self, file_desc, packages, classes, relationships, profiles):
        self.file_description = file_desc
        self.packages = packages
        self.classes = classes
        self.relationships = relationships
        self.profiles = profiles
        self.id = ""
        self.name = ""

class FileDescription:
    def __init__(self):
        pass

class GraphicDescription:
    def __init__(self):
        pass

class ImportedPackage:
    def __init__(self):
        pass

class Class:
    def __init__(self):
        pass

class Stereotype:
    def __init__(self):
        pass

class Generalization:
    def __init__(self):
        pass

class Attribute:
    def __init__(self):
        pass

class Operation:
    def __init__(self):
        pass

class Parameter:
    def __init__(self):
        pass

class Relationship:
    def __init__(self):
        pass

class ApplicationProfile:
    def __init__(self):
        pass
