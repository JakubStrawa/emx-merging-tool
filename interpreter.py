from lexer import Lexer
from parser import Parser
from file_writer import FileWriter
import parser_objects
from tkinter import messagebox


class Interpreter:
    def __init__(self, file1, file2, resolve_mode, merge_destination, root, destination_file="output_files/new_emx_merged.emx"):
        self.file1_path = "test_files/3 - one class with one attribute.emx"
        self.file2_path = "test_files/3,5 - one class with one attribute with conflicts.emx"
        self.resolve_conflicts_mode = resolve_mode
        self.merge_destination = 1
        self.destination_file = destination_file
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
                if answer:
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
                if answer:
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
        if class1.visibility != class2.visibility:
            self.log_messages.append(f'Visibility conflict in class {class1.name}.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 visibility is {class1.visibility}, but file 2 visibility is {class2.visibility}.\nDo you want to change file 1 visibility?', parent=self.root_window)
                if answer:
                    class1.visibility = class2.visibility
                    flag = True
                self.log_messages.append(f'Visibility conflict resolved in class {class1.name}, visibility changed to {class1.visibility}.')
        if class1.isLeaf != class2.isLeaf:
            self.log_messages.append(f'IsLeaf parameter conflict in class {class1.name}.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 isLeaf is {class1.isLeaf}, but file 2 isLeaf is {class2.isLeaf}.\nDo you want to change file 1 isLeaf parameter?', parent=self.root_window)
                if answer:
                    class1.isLeaf = class2.isLeaf
                    flag = True
                self.log_messages.append(f'IsLeaf parameter conflict resolved in class {class1.name}, isLeaf changed to {class1.isLeaf}.')
        if class1.isAbstract != class2.isAbstract:
            self.log_messages.append(f'IsAbstract parameter conflict in class {class1.name}.')
            if self.resolve_conflicts_mode == 0:
                answer = messagebox.askyesno("Question", f'File 1 isAbstract is {class1.isAbstract}, but file 2 isAbstract is {class2.isAbstract}.\nDo you want to change file 1 isAbstract parameter?', parent=self.root_window)
                if answer:
                    class1.isAbstract = class2.isAbstract
                    flag = True
                self.log_messages.append(f'IsAbstract parameter conflict resolved in class {class1.name}, isAbstract changed to {class1.isAbstract}.')
        if (class1.stereotypes is None and class2.stereotypes is not None) or (class1.stereotypes is not None and class2.stereotypes is not None):
            if class1.stereotypes is None:
                class1.stereotypes = class2.stereotypes
                flag = True
            else:
                for s in class2.stereotypes.stereotypes:
                    for t in class1.stereotypes.stereotypes:
                        if s[1] == t[1]:
                            break
                    else:
                        class1.stereotypes.stereotypes.append(s)
                        flag = True
                        continue

        for attr2 in class2.attributes:
            for attr1 in class1.attributes:
                if attr1.name == attr2.name:
                    if attr1.type is not None and attr2.type is not None and (attr1.type[1] != attr2.type[1] or attr1.type[0] != attr2.type[0]):
                        self.log_messages.append(f'Type parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 type is {attr1.type[0]}, but in file 2 type is {attr2.type[0]}.\nDo you want to change file 1 type parameter?', parent=self.root_window)
                            if answer:
                                attr1.type = attr2.type
                                flag = True
                            self.log_messages.append(f'Type parameter conflict resolved in class {class1.name}, attribute {attr1.name}, type changed to {attr1.type[0]}.')
                    if attr1.type is None and attr2.type is not None:
                        self.log_messages.append(f'Type parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 type is None, but in file 2 type is {attr2.type[0]}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.type = attr2.type
                                flag = True
                            self.log_messages.append(f'Type parameter conflict resolved in class {class1.name}, attribute {attr1.name}, type changed to {attr1.type[0]}.')
                    if attr1.parameters.visibility != attr2.parameters.visibility:
                        self.log_messages.append(f'Visibility parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 visibility is {attr1.parameters.visibility}, but in file 2 visibility is {attr2.parameters.visibility}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.visibility = attr2.parameters.visibility
                                flag = True
                            self.log_messages.append(f'Visibility parameter conflict resolved in class {class1.name}, attribute {attr1.name}, visibility changed to {attr1.parameters.visibility}.')
                    if attr1.parameters.isLeaf != attr2.parameters.isLeaf:
                        self.log_messages.append(f'IsLeaf parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isLeaf is {attr1.parameters.isLeaf}, but in file 2 isLeaf is {attr2.parameters.isLeaf}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isLeaf = attr2.parameters.isLeaf
                                flag = True
                            self.log_messages.append(f'IsLeaf parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isLeaf changed to {attr1.parameters.isLeaf}.')
                    if attr1.parameters.isStatic != attr2.parameters.isStatic:
                        self.log_messages.append(f'IsStatic parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isStatic is {attr1.parameters.isStatic}, but in file 2 isStatic is {attr2.parameters.isStatic}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isStatic = attr2.parameters.isStatic
                                flag = True
                            self.log_messages.append(f'IsStatic parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isStatic changed to {attr1.parameters.isStatic}.')
                    if attr1.parameters.isOrdered != attr2.parameters.isOrdered:
                        self.log_messages.append(f'IsOrdered parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isOrdered is {attr1.parameters.isOrdered}, but in file 2 isOrdered is {attr2.parameters.isOrdered}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isOrdered = attr2.parameters.isOrdered
                                flag = True
                            self.log_messages.append(f'IsOrdered parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isOrdered changed to {attr1.parameters.isOrdered}.')
                    if attr1.parameters.isUnique != attr2.parameters.isUnique:
                        self.log_messages.append(f'IsUnique parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isUnique is {attr1.parameters.isUnique}, but in file 2 isUnique is {attr2.parameters.isUnique}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isUnique = attr2.parameters.isUnique
                                flag = True
                            self.log_messages.append(f'IsUnique parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isUnique changed to {attr1.parameters.isUnique}.')
                    if attr1.parameters.isReadOnly != attr2.parameters.isReadOnly:
                        self.log_messages.append(f'IsReadOnly parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isReadOnly is {attr1.parameters.isReadOnly}, but in file 2 isReadOnly is {attr2.parameters.isReadOnly}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isReadOnly = attr2.parameters.isReadOnly
                                flag = True
                            self.log_messages.append(f'IsReadOnly parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isReadOnly changed to {attr1.parameters.isReadOnly}.')
                    if attr1.parameters.isDerived != attr2.parameters.isDerived:
                        self.log_messages.append(f'IsDerived parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isDerived is {attr1.parameters.isDerived}, but in file 2 isDerived is {attr2.parameters.isDerived}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isDerived = attr2.parameters.isDerived
                                flag = True
                            self.log_messages.append(f'IsDerived parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isDerived changed to {attr1.parameters.isDerived}.')
                    if attr1.parameters.isDerivedUnion != attr2.parameters.isDerivedUnion:
                        self.log_messages.append(f'IsDerivedUnion parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isDerivedUnion is {attr1.parameters.isDerivedUnion}, but in file 2 isDerivedUnion is {attr2.parameters.isDerivedUnion}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.isDerivedUnion = attr2.parameters.isDerivedUnion
                                flag = True
                            self.log_messages.append(f'IsDerivedUnion parameter conflict resolved in class {class1.name}, attribute {attr1.name}, isDerivedUnion changed to {attr1.parameters.isDerivedUnion}.')
                    if attr1.parameters.aggregation != attr2.parameters.aggregation:
                        self.log_messages.append(f'Aggregation parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 aggregation is {attr1.parameters.aggregation}, but in file 2 aggregation is {attr2.parameters.aggregation}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.aggregation = attr2.parameters.aggregation
                                flag = True
                            self.log_messages.append(f'Aggregation parameter conflict resolved in class {class1.name}, attribute {attr1.name}, aggregation changed to {attr1.parameters.aggregation}.')
                    if attr1.parameters.association != attr2.parameters.association:
                        self.log_messages.append(f'Association parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 association is {attr1.parameters.association}, but in file 2 association is {attr2.parameters.association}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.association = attr2.parameters.association
                                flag = True
                            self.log_messages.append(f'Association parameter conflict resolved in class {class1.name}, attribute {attr1.name}, association changed to {attr1.parameters.association}.')
                    if attr1.parameters.short_type != attr2.parameters.short_type:
                        self.log_messages.append(f'Short type parameter conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 short type is {attr1.parameters.short_type}, but in file 2 short type is {attr2.parameters.short_type}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.parameters.short_type = attr2.parameters.short_type
                                flag = True
                            self.log_messages.append(f'Short type parameter conflict resolved in class {class1.name}, attribute {attr1.name}, short type changed to {attr1.parameters.short_type}.')
                    if attr2.lower_limit is not None:
                        if attr1.lower_limit is not None and attr1.lower_limit.type != attr2.lower_limit.type:
                            self.log_messages.append(f'Lower limit type conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 lower limit type is {attr1.lower_limit.type}, but in file 2 lower limit type is {attr2.lower_limit.type}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.lower_limit.type = attr2.lower_limit.type
                                    flag = True
                                self.log_messages.append(f'Lower limit type conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to {attr1.lower_limit.type}.')
                        if attr1.lower_limit is not None and attr1.lower_limit.value != attr2.lower_limit.value:
                            self.log_messages.append(f'Lower limit value conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 lower limit value is {attr1.lower_limit.value}, but in file 2 lower limit value is {attr2.lower_limit.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.lower_limit.value = attr2.lower_limit.value
                                    flag = True
                                self.log_messages.append(f'Lower limit value conflict resolved in class {class1.name}, attribute {attr1.name}, value changed to {attr1.lower_limit.value}.')
                        if attr1.lower_limit is None:
                            self.log_messages.append(f'Lower limit conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 lower limit is None, but in file 2 lower limit is {attr2.lower_limit.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.lower_limit = attr2.lower_limit
                                    flag = True
                                self.log_messages.append(f'Lower limit conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to {attr1.lower_limit.value}.')

                    if attr2.lower_limit is None and attr1.lower_limit is not None:
                        self.log_messages.append(f'Lower limit conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 lower limit is {attr1.lower_limit.value}, but in file 2 lower limit is None.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.lower_limit = attr2.lower_limit
                                flag = True
                            self.log_messages.append(f'Lower limit conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to None.')

                    if attr2.upper_limit is not None:
                        if attr1.upper_limit is not None and attr1.upper_limit.type != attr2.upper_limit.type:
                            self.log_messages.append(f'Upper limit type conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 upper limit type is {attr1.upper_limit.type}, but in file 2 upper limit type is {attr2.upper_limit.type}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.upper_limit.type = attr2.upper_limit.type
                                    flag = True
                                self.log_messages.append(f'Upper limit type conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to {attr1.upper_limit.type}.')
                        if attr1.upper_limit is not None and attr1.upper_limit.value != attr2.upper_limit.value:
                            self.log_messages.append(f'Upper limit value conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 upper limit value is {attr1.upper_limit.value}, but in file 2 upper limit value is {attr2.upper_limit.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.upper_limit.value = attr2.upper_limit.value
                                    flag = True
                                self.log_messages.append(f'Upper limit value conflict resolved in class {class1.name}, attribute {attr1.name}, value changed to {attr1.upper_limit.value}.')
                        if attr1.upper_limit is None:
                            self.log_messages.append(f'Upper limit conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 upper limit is None, but in file 2 upper limit is {attr2.upper_limit.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.upper_limit = attr2.upper_limit
                                    flag = True
                                self.log_messages.append(f'Upper limit conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to {attr1.upper_limit.value}.')

                    if attr2.upper_limit is None and attr1.upper_limit is not None:
                        self.log_messages.append(f'Upper limit conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 upper limit is {attr1.upper_limit.value}, but in file 2 upper limit is None.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.upper_limit = attr2.upper_limit
                                flag = True
                            self.log_messages.append(f'Upper limit conflict resolved in class {class1.name}, attribute {attr1.name}, limit changed to None.')

                    if attr2.default_value is not None:
                        if attr1.default_value is not None and attr1.default_value.type != attr2.default_value.type:
                            self.log_messages.append(f'Default value type conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 default value is {attr1.default_value.type}, but in file 2 default value is {attr2.default_value.type}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.default_value.type = attr2.default_value.type
                                    flag = True
                                self.log_messages.append(f'Default value type conflict resolved in class {class1.name}, attribute {attr1.name}, default value changed to {attr1.default_value.type}.')
                        if attr1.default_value is not None and attr1.default_value.value != attr2.default_value.value:
                            self.log_messages.append(f'Default value conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 default value is {attr1.default_value.value}, but in file 2 default value is {attr2.default_value.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.default_value.value = attr2.default_value.value
                                    flag = True
                                self.log_messages.append(f'Default value conflict resolved in class {class1.name}, attribute {attr1.name}, value changed to {attr1.default_value.value}.')
                        if attr1.default_value is None:
                            self.log_messages.append(f'Default value conflict in class {class1.name}, attribute {attr1.name}.')
                            if self.resolve_conflicts_mode == 0:
                                answer = messagebox.askyesno("Question", f'In file 1 default value is None, but in file 2 default value is {attr2.default_value.value}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                                if answer:
                                    attr1.default_value = attr2.default_value
                                    flag = True
                                self.log_messages.append(f'Default value conflict resolved in class {class1.name}, attribute {attr1.name}, default value changed to {attr1.default_value.value}.')

                    if attr2.default_value is None and attr1.default_value is not None:
                        self.log_messages.append(f'Default value conflict in class {class1.name}, attribute {attr1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 default value is {attr1.default_value.value}, but in file 2 default value is None.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                attr1.default_value = attr2.default_value
                                flag = True
                            self.log_messages.append(f'Default value conflict resolved in class {class1.name}, attribute {attr1.name}, default value changed to None.')

            # if class 1 does not have any attribute with that name, it is added to attribute list of class 1
            isAlreadyAnAttribute = False
            for tmp in class1.attributes:
                if tmp.name == attr2.name:
                    isAlreadyAnAttribute = True
            if isAlreadyAnAttribute is False:
                class1.attributes.append(attr2)

        for operation2 in class2.operations:
            for operation1 in class1.operations:
                if operation1.name == operation2.name:
                    if operation1.visibility != operation2.visibility:
                        self.log_messages.append(f'Visibility parameter conflict in class {class1.name}, operation {operation1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 visibility is {operation1.visibility}, but in file 2 visibility is {operation2.visibility}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                operation1.visibility = operation2.visibility
                                flag = True
                            self.log_messages.append(f'Visibility parameter conflict resolved in class {class1.name}, operation {operation1.name}, visibility changed to {operation1.visibility}.')
                    if operation1.isLeaf != operation2.isLeaf:
                        self.log_messages.append(f'isLeaf parameter conflict in class {class1.name}, operation {operation1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isLeaf is {operation1.isLeaf}, but in file 2 isLeaf is {operation2.isLeaf}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                operation1.isLeaf = operation2.isLeaf
                                flag = True
                            self.log_messages.append(f'isLeaf parameter conflict resolved in class {class1.name}, operation {operation1.name}, isLeaf changed to {operation1.isLeaf}.')
                    if operation1.isStatic != operation2.isStatic:
                        self.log_messages.append(f'isStatic parameter conflict in class {class1.name}, operation {operation1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isStatic is {operation1.isStatic}, but in file 2 isStatic is {operation2.isStatic}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                operation1.isStatic = operation2.isStatic
                                flag = True
                            self.log_messages.append(f'isStatic parameter conflict resolved in class {class1.name}, operation {operation1.name}, isStatic changed to {operation1.isStatic}.')
                    if operation1.isAbstract != operation2.isAbstract:
                        self.log_messages.append(f'isAbstract parameter conflict in class {class1.name}, operation {operation1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isAbstract is {operation1.isAbstract}, but in file 2 isAbstract is {operation2.isAbstract}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                operation1.isAbstract = operation2.isAbstract
                                flag = True
                            self.log_messages.append(f'isAbstract parameter conflict resolved in class {class1.name}, operation {operation1.name}, isAbstract changed to {operation1.isAbstract}.')
                    if operation1.isQuery != operation2.isQuery:
                        self.log_messages.append(f'isQuery parameter conflict in class {class1.name}, operation {operation1.name}.')
                        if self.resolve_conflicts_mode == 0:
                            answer = messagebox.askyesno("Question", f'In file 1 isQuery is {operation1.isQuery}, but in file 2 isQuery is {operation2.isQuery}.\nDo you want to change file 1 parameter?', parent=self.root_window)
                            if answer:
                                operation1.isQuery = operation2.isQuery
                                flag = True
                            self.log_messages.append(f'isQuery parameter conflict resolved in class {class1.name}, operation {operation1.name}, isQuery changed to {operation1.isQuery}.')

                    for param2 in operation2.ownedParameters:
                        for param1 in operation1.ownedParameters:
                            pass


        for g in class2.generalizations:
            # find g.general id in class and attribute
            # check if that id, class and attribute are in merged_class
            # if no: write log warning
            # if yes: change ids to correct ones, but it can be that this generalization already exists
            pass


        return class1, flag

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
        if self.merge_destination == 0:
            self.destination_file = self.file1_path
        file_writer = FileWriter(self.destination_file, self.merged_tree)
        file_writer.write_to_file()
        if self.merge_destination == 0:
            self.log_messages.append(f'Application result was written into file 1, path: {self.destination_file}.')
        else:
            self.log_messages.append(f'Application result was written into new file: {self.destination_file}.')
        for mes in self.log_messages:
            print(mes)
