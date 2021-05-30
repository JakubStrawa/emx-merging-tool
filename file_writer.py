import tokens.token


class FileWriter:
    def __init__(self, filepath, tree):
        self.filepath = filepath
        self.tree = tree
        self.file = open(filepath, 'w', encoding='utf-8', errors='replace')

    def write_to_file(self):
        self.write_emx_header()
        self.file.write("Costam testowego\n")
        self.close_file()

    def write_emx_header(self):
        self.file.write('<?xml version="1.0" encoding="UTF-8"?>\n<!--xtools2_universal_type_manager-->\n<!--Rational Software Architect Designer 9.7.0-->\n<?com.ibm.xtools.emf.core.signature <signature id="com.ibm.xtools.mmi.ui.signatures.diagram" version="7.0.0"><feature description="" name="Rational Modeling Platform (com.ibm.xtools.rmp)" url="" version="7.0.0"/></signature>?>\n<?com.ibm.xtools.emf.core.signature <signature id="com.ibm.xtools.uml.msl.model" version="7.0.0"><feature description="" name="com.ibm.xtools.ruml.feature" url="" version="7.0.0"/></signature>?>\n')

    def close_file(self):
        self.file.close()
