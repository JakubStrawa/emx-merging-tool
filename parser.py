from tokens.token import Token, ValueToken, TokenType
from error import SyntaxError
import parser_objects

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = -1
        self.root = self.create_tree()

    def get_token(self):
        self.current_token += 1
        return self.tokens[self.current_token]

    def compare_tokens(self, token, type, msg = ""):
        if token.token_type != type:
            raise SyntaxError(token, msg)

    def create_tree(self):
        model = self.parse_model()
        return model

    def parse_model(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET, "Model does not start with '<'")
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_UML_MODEL, "Model not defined")

        model_description = self.parse_model_description()
        #print(model_description)

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET, "Model description does not end with '>'")

        self.parse_model_content()

        self.parse_model_end()


    # parse model description
    # model description = 'xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore" xmlns:uml="http://www.eclipse.org/uml2/3.0.0/UML" xmlns:umlnotation="http://www.ibm.com/xtools/1.5.3/Umlnotation" xmi:id=', id, ' name=', id;
    def parse_model_description(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_VERSION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMLNS_XMI)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMLNS_XSI)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMLNS_ECORE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMLNS_UML)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMLNS_UML_NOTATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        # model id
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        # model name
        name = token.value
        return [id, name]

    # parse everything after model description
    # model contents = file description,{ package import },{ packaged element },{ profile application };
    def parse_model_content(self):
        self.parse_file_description()
        pckg_import = self.parse_package_import()
        while pckg_import != None:
            pckg_import = self.parse_package_import()

        pckg_element = self.parse_packaged_element()
        while pckg_element != None:
            pckg_element = self.parse_packaged_element()

        profile_application = self.parse_profile_application()
        while profile_application != None:
            profile_application = self.parse_profile_application()

        return [pckg_import, pckg_element, profile_application]


    # file description = "<eAnnotations xmi:id=", id, ' source="uml2.diagrams">', file name, "</eAnnotations>";
    def parse_file_description(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SOURCE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        self.parse_file_name()


    # file description = "<eAnnotations xmi:id=", string value, ' source="uml2.diagrams">', file name, "</eAnnotations>";
    # file name = "<contents xmi:type="umlnotation:UMLDiagram" xmi:id=", string value, ' type="Class" name=', string value, ">", graphic description, "</contents>";
    def parse_file_name(self):
        token = self.get_token()
        while token.token_type != TokenType.T_EANNOTATIONS:
            # skip graphic description
            token = self.get_token()
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)


    # package import = "<packageImport xmi:id=", id, ">", package, "</packageImport>";
    def parse_package_import(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()

        if token.token_type == TokenType.T_PACKAGED_ELEMENT:
            self.current_token -= 2
            return None

        self.compare_tokens(token, TokenType.T_PACKAGE_IMPORT)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        self.parse_package()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_PACKAGE_IMPORT)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

    # package = '<importedPackage xmi:type="uml:Model" href=', string value, "/>";
    def parse_package(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_IMPORTED_PACKAGE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

    # packaged element = "<packagedElement xmi:type=", ( class | association ), "</packagedElement>";
    def parse_packaged_element(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()

        if token.token_type == TokenType.T_PROFILE_APPLICATION:
            self.current_token -= 2
            return None

        self.compare_tokens(token, TokenType.T_PACKAGED_ELEMENT)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        if token.value == '"uml:Class"':
            self.parse_class()
        elif token.value == '"uml:Association"':
            self.parse_association()
        else:
            raise SyntaxError(token, "Unrecognised packaged element, xmi:type expected: uml:Class or uml:Association")

    # class = '"uml:Class" xmi:id=', string value, " name=", string value, visibility, ['isLeaf="true"'],
    # ['isAbstract="true"'], ">", [ stereotype ], [ generalization ], {attribute}, {operation};
    def parse_class(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        # czy to jest w klasie???
        self.parse_visibility()

        token = self.get_token()
        while token.token_type == TokenType.T_IS_LEAF | token.token_type == TokenType.T_IS_ABSTRACT:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_EQUALS)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_STRING_VALUE)
            if token.value != '"true"' | token.value != '"false"':
                raise SyntaxError(token, "Unexpected value, expected true or false value")
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        stereotype = self.parse_stereotype()
        generalization = self.parse_generalization()
        attribute = self.parse_attribute()
        while attribute != None:
            attribute = self.parse_attribute()
        operation = self.parse_operation()
        while operation != None:
            operation = self.parse_operation()
        self.parse_packaged_element_end()



    # visibility = " visibility=", visibility type;
    # visibility type = "public" | "private" | "protected" | "package";
    def parse_visibility(self):
        token = self.get_token()
        if token.token_type != TokenType.T_VISIBILITY:
            self.current_token -= 1
            return None
        self.compare_tokens(token, TokenType.T_VISIBILITY)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        if token.value == '"public"' | token.value == '"private"' | token.value == '"protected"' | token.value == '"package"':
            pass
        else:
            raise SyntaxError(token, "Unexpected visibility")


    # stereotype = "<eAnnotations xmi:id=", string value, " source=", string value, ">", stereotype description, {stereotype description}, "</eAnnotations>";
    def parse_stereotype(self):
        pass

    # stereotype description = "<details xmi:id=", string value, " key=", string value, "/>";
    def parse_stereotype_description(self):
        pass

    # generalization = "<generalization xmi:id=", string value, " general=", string value, "/>";
    def parse_generalization(self):
        pass

    # attribute = "<ownedAttribute xmi:id=", string value, " name=", string value, attribute parameters, ( "/>" | attribute description );
    # attribute description = ">", [type], [limit], [default value], "</ownedAttribute>";
    # attribute parameters = visibility, ['isLeaf="true"'], ['isStatic="true"'], ['isOrdered="true"'], ['isReadOnly="true"'], ['isDerived="true"'], ['isDerivedUnion="true"'], [short type], [association type];
    def parse_attribute(self):
        pass

    # operation = "<ownedOperation xmi:id=", string value, " name=", string value, [ operation parameters ], ("/>" | parameter );
    def parse_operation(self):
        pass

    # association = '"uml:Association"', " xmi:id=", string value, " memberEnd=", double string value, ">", owned end;
    def parse_association(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_MEMBER_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_DOUBLE_STRING_VALUE)
        token = self.get_token()
        if token.token_type == TokenType.T_SLASH:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            return 0
        elif token.token_type == TokenType.T_RIGHT_BRACKET:
            self.parse_owned_end()
            return 0
        else:
            raise SyntaxError(token, "Invalid association ending, expected '/' or '>'")


    # owned end = "<ownedEnd xmi:id=", string value, " name=", string value, visibility, short type, "association=", string value, ">", upper limit, lower limit, "</ownedEnd>";
    def parse_owned_end(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_OWNED_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)

        self.parse_visibility()
        self.parse_short_type()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_ASSOCIATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        self.parse_upper_limit()
        self.parse_lower_limit()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_OWNED_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        self.parse_packaged_element_end()


    def parse_upper_limit(self):
        pass

    def parse_lower_limit(self):
        pass

    # short type = " type=", string value;
    def parse_short_type(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)

    # "</packagedElement>"
    def parse_packaged_element_end(self):
        msg = "Packaged element ended incorrectly!"
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_PACKAGED_ELEMENT, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET, msg)

    # profile application = "<profileApplication xmi:id=", id, ">", eannotation, applied profile, "</profileApplication>";
    def parse_profile_application(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()

        if token.token_type == TokenType.T_SLASH:
            self.current_token -= 2
            return None

        self.compare_tokens(token, TokenType.T_PROFILE_APPLICATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        self.parse_eannotation()
        self.parse_applied_profile()


    # eannotation = "<eAnnotations xmi:id=", string value, " source=", string value, ">", references, "</eAnnotations>";
    def parse_eannotation(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SOURCE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        self.parse_references()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

    # references = '<references xmi:type="ecore:EPackage" href=', string value, "/>";
    def parse_references(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_REFERENCES)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

    # applied profile = "<appliedProfile href=", path, "/>";
    def parse_applied_profile(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_APPLIED_PROFILE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

    # parse </uml:Model> expression
    def parse_model_end(self):
        msg = "Model ended incorrectly!"
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_UML_MODEL, msg)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET, msg)

