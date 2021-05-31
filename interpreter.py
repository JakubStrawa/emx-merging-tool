from lexer import Lexer
from parser import Parser
from file_writer import FileWriter
import parser_objects
import error


class Interpreter:
    def __init__(self, file1, file2, resolve_mode, merge_destination):
        self.file1_path = "input_files/JavaBlankModel3.emx"
        self.file2_path = "input_files/JavaBlankModel.emx"
        self.resolve_conflicts_mode = resolve_mode
        self.merge_destination = 1
        self.merged_tree = None
        self.log_messages = []
        self.tokenize_input_files()

    def tokenize_input_files(self):
        lexer1 = Lexer(self.file1_path)
        lexer2 = Lexer(self.file2_path)
        print("File tokenizing complete")
        self.parse_input_files(lexer1.tokens_found, lexer2.tokens_found)

    def parse_input_files(self, token_list1, token_list2):
        tree1 = Parser(token_list1)
        tree2 = Parser(token_list2)
        print("Parsing complete")
        self.combine_input_files(tree1.tree, tree2.tree)

    def combine_input_files(self, tree1, tree2):
        file_description = self.compare_file_descriptions(tree1, tree2)
        package_imports = self.compare_package_imports(tree1, tree2)
        packaged_elements = self.compare_packaged_elements(tree1, tree2)
        profiles = self.compare_profiles(tree1, tree2)
        if tree1.name != tree2.name:
            self.log_messages.append(f'Files models name are different, name taken from file 1: {tree1.name}')
        self.merged_tree = parser_objects.Model(file_description, package_imports, packaged_elements, profiles, tree1.name, tree1.id)
        self.write_to_file()

    def compare_file_descriptions(self, tree1, tree2):
        # graphics description copied from file 1
        graphic = tree1.file_description.graphic
        id = tree1.file_description.id
        source = tree1.file_description.source
        if tree1.file_description.source != tree2.file_description.source:
            self.log_messages.append(f'Files description sources are different, source taken from file 1: {tree1.file_description.source}')
        file_description = parser_objects.FileDescription(graphic, id, source)
        return file_description

    def compare_package_imports(self, tree1, tree2):
        package_imports = tree1.package_imports
        for p in tree2.package_imports:
            for r in tree1.package_imports:
                if p.type == r.type and p.href == r.href:
                    break
            else:
                package_imports.append(p)
                continue
        return package_imports

    # TODO: Implement compare_packages_elements
    def compare_packaged_elements(self, tree1, tree2):
        packaged_elements = tree1.packaged_elements
        for p in tree2.packaged_elements:
            for r in packaged_elements:
                if type(p) is parser_objects.Class and type(r) is parser_objects.Class and p.name == r.name:
                    new_class, flag = self.compare_classes(r, p)
                    if flag is True:
                        pass
                    else:
                        break
                elif type(p) is parser_objects.Association and type(r) is parser_objects.Association:
                    self.compare_associations()
                else:
                    break

        return packaged_elements

    # TODO: Implement compare_classes
    def compare_classes(self, class1, class2):
        return 1, False

    # TODO: Implement compare_associations
    def compare_associations(self):
        pass

    def compare_profiles(self, tree1, tree2):
        profiles = tree1.profiles
        for p in tree2.profiles:
            for r in profiles:
                if p.href == r.href:
                    break
                if p.eannotation.source == r.eannotation.source and p.eannotation.type == r.eannotation.type and p.eannotation.href == r.eannotation.href:
                    break
            else:
                profiles.append(p)
                continue
        return profiles

    def write_to_file(self):
        file_destination = "output_files/new_emx_merged.emx"
        if self.merge_destination == 0:
            file_destination = self.file1_path
        file_writer = FileWriter(file_destination, self.merged_tree)
        file_writer.write_to_file()
