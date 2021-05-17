from tokens.token import TokenType
from error import SyntaxError
import parser_objects


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = -1
        self.tree = self.create_tree()

    def get_token(self):
        self.current_token += 1
        return self.tokens[self.current_token]

    def compare_tokens(self, token, type, msg=""):
        if token.token_type != type:
            raise SyntaxError(token, msg)

    def create_tree(self):
        model_description, model_content = self.parse_model()
        model = parser_objects.Model(model_content[0], model_content[1], model_content[2],
                                     model_content[3], model_description[0], model_description[1])
        return model

    def parse_model(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET, "Model does not start with '<'")
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_UML_MODEL, "Model not defined")

        model_description = self.parse_model_description()  # [id, name]

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET, "Model description does not end with '>'")

        model_content = self.parse_model_content()  # [file_description, imports, elements, profiles]

        self.parse_model_end()
        return model_description, model_content

    # parse model description
    # model description = 'xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI"
    # xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore"
    # xmlns:uml="http://www.eclipse.org/uml2/3.0.0/UML" xmlns:umlnotation="http://www.ibm.com/xtools/1.5.3/Umlnotation"
    # xmi:id=', id, ' name=', id;
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
        file_description = self.parse_file_description()
        imports = []
        pckg_import = self.parse_package_import()
        while pckg_import != None:
            imports.append(pckg_import)
            pckg_import = self.parse_package_import()

        elements = []
        pckg_element = self.parse_packaged_element()
        while pckg_element != None:
            elements.append(pckg_element)
            pckg_element = self.parse_packaged_element()

        profiles = []
        profile_application = self.parse_profile_application()
        while profile_application != None:
            profiles.append(profile_application)
            profile_application = self.parse_profile_application()

        return [file_description, imports, elements, profiles]

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
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SOURCE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        source = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        graphics = self.parse_file_name()

        file_description = parser_objects.FileDescription(graphics.graphic, id, source)
        return file_description

    # file name = "<contents xmi:type="umlnotation:UMLDiagram" xmi:id=", string value, ' type="Class" name=',
    # string value, ">", graphic description, "</contents>";
    def parse_file_name(self):
        token = self.get_token()
        graphics = parser_objects.GraphicDescription()
        while token.token_type != TokenType.T_EANNOTATIONS:
            # skip graphic description
            # append all tokens to GraphicDescription class
            graphics.graphic.append(token)
            token = self.get_token()
        graphics.graphic.append(token)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        graphics.graphic.append(token)
        return graphics

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
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        type, href = self.parse_package()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_PACKAGE_IMPORT)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        package = parser_objects.ImportedPackage(id, type, href)
        return package

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
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        href = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return type, href

    # packaged element = "<packagedElement xmi:type=", ( class | association ), "</packagedElement>";
    def parse_packaged_element(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()

        if token.token_type != TokenType.T_PACKAGED_ELEMENT:
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
            return self.parse_class()
        elif token.value == '"uml:Association"':
            return self.parse_association()
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
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        name = token.value

        visibility = self.parse_visibility()

        optional_attributes = []
        token = self.get_token()
        if token.token_type != TokenType.T_RIGHT_BRACKET:
            while token.token_type == TokenType.T_IS_LEAF or token.token_type == TokenType.T_IS_ABSTRACT:
                option_type = token.token_type
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_EQUALS)
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_STRING_VALUE)
                if token.value != '"true"' and token.value != '"false"':
                    raise SyntaxError(token, "Unexpected value, expected true or false value")
                else:
                    option_value = token.value
                    optional_attributes.append((option_type, option_value))
            token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        stereotype = self.parse_stereotype()
        generalization = self.parse_generalization()
        attributes = []
        attribute = self.parse_attribute()
        while attribute != None:
            attributes.append(attribute)
            attribute = self.parse_attribute()
        operations = []
        operation = self.parse_operation()
        while operation != None:
            operations.append(operation)
            operation = self.parse_operation()
        self.parse_packaged_element_end()
        is_abstract = '"false"'
        is_leaf = '"false"'
        for a in optional_attributes:
            if a[0] == TokenType.T_IS_LEAF:
                is_leaf = a[1]
            if a[0] == TokenType.T_IS_ABSTRACT:
                is_abstract = a[1]
        parsed_class = parser_objects.Class(id, name, visibility, is_leaf, is_abstract, stereotype, generalization, attributes, operations)
        return parsed_class

    # visibility = " visibility=", visibility type;
    # visibility type = "public" | "private" | "protected" | "package";
    def parse_visibility(self):
        token = self.get_token()
        if token.token_type != TokenType.T_VISIBILITY:
            self.current_token -= 1
            return None
        self.compare_tokens(token, TokenType.T_VISIBILITY)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        if token.value == '"public"' or token.value == '"private"' or token.value == '"protected"' \
                or token.value == '"package"':
            return token.value
        else:
            raise SyntaxError(token, "Unexpected visibility")

    # stereotype = "<eAnnotations xmi:id=", string value, " source=", string value, ">", stereotype description,
    #               {stereotype description}, "</eAnnotations>";
    def parse_stereotype(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_EANNOTATIONS:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SOURCE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        source = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        stereotypes = []
        stereotype = self.parse_stereotype_description()
        while stereotype != None:
            stereotypes.append(stereotype)
            stereotype = self.parse_stereotype_description()
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        stereotypes_obj = parser_objects.Stereotype(id, source, stereotypes)
        return stereotypes_obj

    # stereotype description = "<details xmi:id=", string value, " key=", string value, "/>";
    def parse_stereotype_description(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_DETAILS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_KEY)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        key = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return [id, key]

    # generalization = "<generalization xmi:id=", string value, " general=", string value, "/>";
    def parse_generalization(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_GENERALIZATION:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_GENERALIZATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_GENERAL)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        general = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        generalization = parser_objects.Generalization(id, general)
        return generalization

    # attribute = "<ownedAttribute xmi:id=", string value, " name=", string value, attribute parameters,
    #           ( "/>" | attribute description );
    # attribute description = ">", [type], [limit], [default value], "</ownedAttribute>";
    def parse_attribute(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_OWNED_ATTRIBUTE:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_OWNED_ATTRIBUTE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        name = token.value
        parameters = self.parse_attribute_parameters()
        token = self.get_token()
        if token.token_type == TokenType.T_SLASH:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            attribute = parser_objects.Attribute(id, name, parameters, None, None, None, None)
            return attribute
        elif token.token_type == TokenType.T_RIGHT_BRACKET:
            type = self.parse_type()
            upper_limit = self.parse_upper_limit()
            lower_limit = self.parse_lower_limit()
            default_value = self.parse_default_value()
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_SLASH)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_OWNED_ATTRIBUTE)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            attribute = parser_objects.Attribute(id, name, parameters, type, upper_limit, lower_limit, default_value)
            return attribute
        else:
            raise SyntaxError(token, "Unexpected OwnedAttribute ending, expected '/' or '>'")

    # type = "<type xmi:type=", string value, "href=", string value,"/>";
    def parse_type(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_TYPE:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        href = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return type, href

    # default value = "<defaultValue xmi:type=", string value, " xmi:id=", string value, " value=", string value,
    # ( default value type | "/>" );
    # default value type = type, "</defaultValue>";
    def parse_default_value(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_DEFAULT_VALUE:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_DEFAULT_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        value = token.value
        token = self.get_token()
        if token.token_type != TokenType.T_SLASH:
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            default_type = self.parse_type()
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_SLASH)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_DEFAULT_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        default_value = parser_objects.Limit(type, id, value)
        return default_value

    # attribute parameters = visibility, ['isLeaf="true"'], ['isStatic="true"'], ['isOrdered="true"'],
    # ['isReadOnly="true"'], ['isDerived="true"'], ['isDerivedUnion="true"'], [short type], [association type];
    # association type = [ 'aggregation="composite"' | 'aggregation="shared"' ], "association=", string value;
    def parse_attribute_parameters(self):
        visibility = self.parse_visibility()
        token = self.get_token()
        if token.token_type != TokenType.T_RIGHT_BRACKET and token.token_type != TokenType.T_SLASH:
            while token.token_type == TokenType.T_IS_LEAF or token.token_type == TokenType.T_IS_STATIC \
                    or token.token_type == TokenType.T_IS_ORDERED or token.token_type == TokenType.T_IS_READ_ONLY \
                    or token.token_type == TokenType.T_IS_DERIVED or token.token_type == TokenType.T_IS_DERIVED_UNION:
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_EQUALS)
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_STRING_VALUE)
                token = self.get_token()
            if token.token_type == TokenType.T_TYPE:
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_EQUALS)
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_STRING_VALUE)
                token = self.get_token()
            if token.token_type == TokenType.T_AGGREGATION:
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_EQUALS)
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_STRING_VALUE)
                token = self.get_token()
            if token.token_type == TokenType.T_ASSOCIATION:
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_EQUALS)
                token = self.get_token()
                self.compare_tokens(token, TokenType.T_STRING_VALUE)
                token = self.get_token()

        self.current_token -= 1
        parameters = parser_objects.AttributeParameters(visibility, None, None, None, None, None, None, None, None)
        return parameters

    # operation = "<ownedOperation xmi:id=", string value, " name=", string value, [ operation parameters ],
    #           ("/>" | parameter );
    def parse_operation(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_OWNED_OPERATION:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_OWNED_OPERATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        name = token.value
        parameters = self.parse_operation_parameters()
        token = self.get_token()
        owned_parameters = []
        if token.token_type != TokenType.T_SLASH:
            owned_parameter = self.parse_owned_parameter()
            while owned_parameter != None:
                owned_parameters.append(owned_parameter)
                owned_parameter = self.parse_owned_parameter()
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_SLASH)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_OWNED_OPERATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        operation = parser_objects.Operation(id, name, None, None, None, None, owned_parameters)
        return operation

    # operation parameters = visibility, ['isLeaf="true"'], ['isStatic="true"'], ['isQuery="true"'];
    def parse_operation_parameters(self):
        visibility = self.parse_visibility()
        token = self.get_token()
        while token.token_type == TokenType.T_IS_LEAF or token.token_type == TokenType.T_IS_STATIC \
                or token.token_type == TokenType.T_IS_QUERY:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_EQUALS)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_STRING_VALUE)
            token = self.get_token()
        self.current_token -= 1
        return visibility

    # parameter = owned parameter, {owned parameter}, "</ownedOperation>";
    # owned parameter = "<ownedParameter xmi:id=", string value, " name=", string value, [owned parameter parameters],
    #                   ("/>" | owned parameter description);
    # owned parameter parameters = short type, ['isOrdered="true"'], ['isUnique="false"'], [parameter direction];
    def parse_owned_parameter(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_OWNED_PARAMETER:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_OWNED_PARAMETER)
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
        type = self.parse_short_type()
        token = self.get_token()
        while token.token_type == TokenType.T_IS_ORDERED or token.token_type == TokenType.T_IS_UNIQUE:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_EQUALS)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_STRING_VALUE)
            token = self.get_token()
        direction = self.parse_parameter_direction(token)
        token = self.get_token()
        if token.token_type != TokenType.T_SLASH:
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            description = self.parse_owned_parameter_description()
            return description
        else:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            return 0

    # owned parameter description = ">", [type], [upper limit], [lower limit], [default value], "</ownedParameter>";
    def parse_owned_parameter_description(self):
        type = self.parse_type()
        upper_limit = self.parse_upper_limit()
        lower_limit = self.parse_lower_limit()
        default_value = self.parse_default_value()
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_OWNED_PARAMETER)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return type, upper_limit, lower_limit, default_value

    # parameter direction = " direction=", direction type;
    # direction type = "return" | "out" | "inout";
    def parse_parameter_direction(self, tok):
        if tok.token_type != TokenType.T_DIRECTION:
            self.current_token -= 1
            return None
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        return token.value

    # association = '"uml:Association"', " xmi:id=", string value, " memberEnd=", double string value, ">", owned end;
    def parse_association(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_MEMBER_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_DOUBLE_STRING_VALUE)
        member_end = token.value
        token = self.get_token()
        if token.token_type == TokenType.T_SLASH:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
            association = parser_objects.Association(id, member_end, None)
            return association
        elif token.token_type == TokenType.T_RIGHT_BRACKET:
            owned_end = self.parse_owned_end()
            association = parser_objects.Association(id, member_end, owned_end)
            return association
        else:
            raise SyntaxError(token, "Invalid association ending, expected '/' or '>'")

    # owned end = "<ownedEnd xmi:id=", string value, " name=", string value, visibility, short type, "association=",
    #           string value, ">", upper limit, lower limit, "</ownedEnd>";
    def parse_owned_end(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_OWNED_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_NAME)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        name = token.value

        visibility = self.parse_visibility()
        type = self.parse_short_type()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_ASSOCIATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        association = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        upper_limit = self.parse_upper_limit()
        lower_limit = self.parse_lower_limit()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_OWNED_END)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        self.parse_packaged_element_end()
        owned_end = parser_objects.OwnedEnd(id, name, visibility, type, association, upper_limit, lower_limit)
        return owned_end

    # upper limit = "<upperValue xmi:type=", string value, " xmi:id=", string value, [" value=", ("1" | "*")] ,"/>";
    def parse_upper_limit(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_UPPER_VALUE:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_UPPER_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        value = None
        if token.token_type == TokenType.T_VALUE:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_EQUALS)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_STRING_VALUE)
            value = token.value
            token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        upper_limit = parser_objects.Limit(type, id, value)
        return upper_limit

    # lower limit = "<lowerValue xmi:type=", string value, " xmi:id=", string value, [" value=", ("1" | "*")] ,"/>";
    def parse_lower_limit(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        if token.token_type != TokenType.T_LOWER_VALUE:
            self.current_token -= 2
            return None
        self.compare_tokens(token, TokenType.T_LOWER_VALUE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        value = None
        if token.token_type == TokenType.T_VALUE:
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_EQUALS)
            token = self.get_token()
            self.compare_tokens(token, TokenType.T_STRING_VALUE)
            value = token.value
            token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        lower_limit = parser_objects.Limit(type, id, value)
        return lower_limit

    # short type = " type=", string value;
    def parse_short_type(self):
        token = self.get_token()
        if token.token_type != TokenType.T_TYPE:
            self.current_token -= 1
            return None
        self.compare_tokens(token, TokenType.T_TYPE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        return token.value

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

    # profile application = "<profileApplication xmi:id=", id, ">", eannotation,
    #                       applied profile, "</profileApplication>";
    def parse_profile_application(self):
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()

        if token.token_type != TokenType.T_PROFILE_APPLICATION:
            self.current_token -= 2
            return None

        self.compare_tokens(token, TokenType.T_PROFILE_APPLICATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_XMI_ID)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        eannotation = self.parse_eannotation()
        href = self.parse_applied_profile()
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_PROFILE_APPLICATION)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        profile_application = parser_objects.ProfileApplication(eannotation, id, href)
        return profile_application

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
        id = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SOURCE)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        source = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)

        type, href = self.parse_references()

        token = self.get_token()
        self.compare_tokens(token, TokenType.T_LEFT_BRACKET)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EANNOTATIONS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        eannotation = parser_objects.EAnnotation(id, source, type, href)
        return eannotation

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
        type = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_HREF)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EQUALS)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_STRING_VALUE)
        href = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return type, href

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
        href = token.value
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_SLASH)
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_RIGHT_BRACKET)
        return href

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
        token = self.get_token()
        self.compare_tokens(token, TokenType.T_EOF, msg)
