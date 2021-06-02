from lexer import Lexer
from parser import Parser
from file_writer import FileWriter
import parser_objects
from tkinter import messagebox
import error


class Interpreter:
    def __init__(self, file1, file2, resolve_mode, merge_destination, root):
        self.file1_path = "test_files/3 - one class with one attribute.emx"
        self.file2_path = "test_files/3,5 - one class with one attribute with conflicts.emx"
        self.resolve_conflicts_mode = resolve_mode
        self.merge_destination = 1
        self.merged_tree = None
        self.root_window = root
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
            self.log_messages.append(f'Files\' model names are different.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 name is {tree1.name}, but file 2 name is {tree2.name}.\nDo you want to change file 1 name?', parent=self.root_window)
                if answer == True:
                    tree1.name = tree2.name
                self.log_messages.append(f'Name conflict resolved, name changed to {tree1.name}.')
        self.merged_tree = parser_objects.Model(file_description, package_imports, packaged_elements, profiles, tree1.id, tree1.name)
        self.write_to_file()

    def compare_file_descriptions(self, tree1, tree2):
        # graphics description copied from file 1
        graphic = tree1.file_description.graphic
        id = tree1.file_description.id
        source = tree1.file_description.source
        if tree1.file_description.source != tree2.file_description.source:
            self.log_messages.append(f'Files\' description sources are different.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 description source is {source}, but file 2 description source is {tree2.file_description.source}.\nDo you want to change file 1 description source?', parent=self.root_window)
                if answer == True:
                    source = tree2.file_description.source
                self.log_messages.append(f'Description source conflict resolved, description source changed to {source}.')
        file_description = parser_objects.FileDescription(graphic, id, source)
        return file_description

    def compare_package_imports(self, tree1, tree2):
        package_imports = tree1.package_imports
        for p in tree2.package_imports:
            for r in tree1.package_imports:
                if p.type == r.type and p.href == r.href:
                    break
            else:
                self.log_messages.append(f'New package import added with type: {p.type} and href: {p.href}.')
                package_imports.append(p)
                continue
        return package_imports

    # TODO: Implement compare_packages_elements
    def compare_packaged_elements(self, tree1, tree2):
        packaged_elements = tree1.packaged_elements
        for p in tree2.packaged_elements:
            for r in range(len(packaged_elements)):
                if type(p) is parser_objects.Class and type(packaged_elements[r]) is parser_objects.Class and p.name == packaged_elements[r].name:
                    new_class, flag = self.compare_classes(packaged_elements[r], p, packaged_elements)
                    if flag is True:
                        packaged_elements[r] = new_class
                    else:
                        break
                elif type(p) is parser_objects.Association and type(packaged_elements[r]) is parser_objects.Association:
                    new_association, flag = self.compare_associations(packaged_elements[r], p, packaged_elements)
                    if flag is True:
                        packaged_elements[r] = new_association
                    else:
                        break
            else:
                if type(p) is parser_objects.Class:
                    # rename ids
                    packaged_elements.append(p)
                elif type(p) is parser_objects.Association:
                    # rename ids
                    packaged_elements.append(p)

        return packaged_elements

    # TODO: Implement compare_classes
    def compare_classes(self, class1, class2, packaged_elements):
        flag = False
        merged_class = class1
        if class1.visibility != class2.visibility:
            self.log_messages.append(f'Visibility conflict in class {class1.name}.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 visibility is {class1.visibility}, but file 2 visibility is {class2.visibility}.\nDo you want to change file 1 visibility?', parent=self.root_window)
                if answer == True:
                    merged_class.visibility = class2.visibility
                self.log_messages.append(f'Visibility conflict resolved in class {class1.name}, visibility changed to {merged_class.visibility}.')
        if class1.isLeaf != class2.isLeaf:
            self.log_messages.append(f'IsLeaf parameter conflict in class {class1.name}.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 isLaf is {class1.isLeaf}, but file 2 isLeaf is {class2.isLeaf}.\nDo you want to change file 1 isLeaf parameter?', parent=self.root_window)
                if answer == True:
                    merged_class.isLeaf = class2.isLeaf
                self.log_messages.append(f'IsLeaf parameter conflict resolved in class {class1.name}, isLeaf changed to {merged_class.isLeaf}.')
        if class1.isAbstract != class2.isAbstract:
            pass
        for attr in class2.attributes:
            pass


        return merged_class, flag

    # TODO: Implement compare_associations
    def compare_associations(self, association1, association2, packaged_elements):
        if association1.id == association2.id:
            return 1, False
        id = association2.member_end
        self.search_for_string(id, packaged_elements)
        return 1, False

    def search_for_string(self, str, packaged_elements):
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
                self.log_messages.append(f'New profile added with href: {p.href}.')
                profiles.append(p)
                continue
        return profiles

    def write_to_file(self):
        file_destination = "output_files/new_emx_merged.emx"
        if self.merge_destination == 0:
            file_destination = self.file1_path
        file_writer = FileWriter(file_destination, self.merged_tree)
        file_writer.write_to_file()
        if self.merge_destination == 0:
            self.log_messages.append(f'Application result was written into file 1, path: {file_destination}.')
        else:
            self.log_messages.append(f'Application result was written into new file: {file_destination}.')
        for mes in self.log_messages:
            print(mes)
