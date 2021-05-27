import enum


# class Token represents simple token without value
# class ValueToken represents token with value
# class TokenType with all needed tokens for lexer
# dictionary token_names with token corresponding literals

class Token:
    def __init__(self, type, line=0, position=0):
        self.token_type = type
        self.line = line
        self.position = position


class ValueToken(Token):
    def __init__(self, type, value, line=0, position=0):
        super().__init__(type, line, position)
        self.value = value


class TokenType(enum.Enum):
    def to_string(self):
        return token_names.get(self)

    # basic symbols <,>,/,=
    T_LEFT_BRACKET = enum.auto()
    T_RIGHT_BRACKET = enum.auto()
    T_SLASH = enum.auto()
    T_EQUALS = enum.auto()

    #emx file tokens
    T_UML_MODEL = enum.auto()
    T_XMI_ID = enum.auto()
    T_NAME = enum.auto()
    T_EANNOTATIONS = enum.auto()
    T_SOURCE = enum.auto()
    T_CONTENTS = enum.auto()
    T_XMI_TYPE = enum.auto()
    T_TYPE = enum.auto()
    T_ELEMENT = enum.auto()
    T_XSI_NIL = enum.auto()
    T_PACKAGE_IMPORT = enum.auto()
    T_IMPORTED_PACKAGE = enum.auto()
    T_HREF = enum.auto()
    T_PACKAGED_ELEMENT = enum.auto()
    T_GENERALIZATION = enum.auto()
    T_GENERAL = enum.auto()
    T_OWNED_ATTRIBUTE = enum.auto()
    T_VISIBILITY = enum.auto()
    T_VALUE = enum.auto()
    T_UPPER_VALUE = enum.auto()
    T_LOWER_VALUE = enum.auto()
    T_DEFAULT_VALUE = enum.auto()
    T_AGGREGATION = enum.auto()
    T_ASSOCIATION = enum.auto()
    T_OWNED_OPERATION = enum.auto()
    T_OWNED_PARAMETER = enum.auto()
    T_IS_STATIC = enum.auto()
    T_MEMBER_END = enum.auto()
    T_OWNED_END = enum.auto()
    T_PROFILE_APPLICATION = enum.auto()
    T_REFERENCES = enum.auto()
    T_APPLIED_PROFILE = enum.auto()
    T_XMLNS_NOTATION = enum.auto()
    T_CHILDREN = enum.auto()
    T_TARGET = enum.auto()
    T_DETAILS = enum.auto()
    T_KEY = enum.auto()
    T_IS_LEAF = enum.auto()
    T_IS_ORDERED = enum.auto()
    T_IS_READ_ONLY = enum.auto()
    T_IS_DERIVED = enum.auto()
    T_IS_DERIVED_UNION = enum.auto()
    T_IS_QUERY = enum.auto()
    T_DIRECTION = enum.auto()
    T_IS_UNIQUE = enum.auto()
    T_IS_ABSTRACT = enum.auto()
    T_EOF = enum.auto()
    T_XMI_VERSION = enum.auto()
    T_XMLNS_XMI = enum.auto()
    T_XMLNS_XSI = enum.auto()
    T_XMLNS_ECORE = enum.auto()
    T_XMLNS_UML = enum.auto()
    T_XMLNS_UML_NOTATION = enum.auto()

    # string value tokens
    T_STRING_VALUE = enum.auto()
    T_DOUBLE_STRING_VALUE = enum.auto()


token_names = {
    TokenType.T_LEFT_BRACKET: "<",
    TokenType.T_RIGHT_BRACKET: ">",
    TokenType.T_SLASH: "/",
    TokenType.T_EQUALS: "=",
    TokenType.T_UML_MODEL: "uml:Model",
    TokenType.T_XMI_ID: "xmi:id",
    TokenType.T_NAME: "name",
    TokenType.T_EANNOTATIONS: "eAnnotations",
    TokenType.T_SOURCE: "source",
    TokenType.T_CONTENTS: "contents",
    TokenType.T_XMI_TYPE: "xmi:type",
    TokenType.T_TYPE: "type",
    TokenType.T_ELEMENT: "element",
    TokenType.T_XSI_NIL: "xsi:nil",
    TokenType.T_PACKAGE_IMPORT: "packageImport",
    TokenType.T_IMPORTED_PACKAGE: "importedPackage",
    TokenType.T_HREF: "href",
    TokenType.T_PACKAGED_ELEMENT: "packagedElement",
    TokenType.T_GENERALIZATION: "generalization",
    TokenType.T_GENERAL: "general",
    TokenType.T_OWNED_ATTRIBUTE: "ownedAttribute",
    TokenType.T_VISIBILITY: "visibility",
    TokenType.T_VALUE: "value",
    TokenType.T_UPPER_VALUE: "upperValue",
    TokenType.T_LOWER_VALUE: "lowerValue",
    TokenType.T_DEFAULT_VALUE: "defaultValue",
    TokenType.T_AGGREGATION: "aggregation",
    TokenType.T_ASSOCIATION: "association",
    TokenType.T_OWNED_OPERATION: "ownedOperation",
    TokenType.T_OWNED_PARAMETER: "ownedParameter",
    TokenType.T_IS_STATIC: "isStatic",
    TokenType.T_MEMBER_END: "memberEnd",
    TokenType.T_OWNED_END: "ownedEnd",
    TokenType.T_PROFILE_APPLICATION: "profileApplication",
    TokenType.T_REFERENCES: "references",
    TokenType.T_APPLIED_PROFILE: "appliedProfile",
    TokenType.T_XMLNS_NOTATION: "xmlns:notation",
    TokenType.T_CHILDREN: "children",
    TokenType.T_TARGET: "target",
    TokenType.T_DETAILS: "details",
    TokenType.T_KEY: "key",
    TokenType.T_IS_LEAF: "isLeaf",
    TokenType.T_IS_ORDERED: "isOrdered",
    TokenType.T_IS_READ_ONLY: "isReadOnly",
    TokenType.T_IS_DERIVED: "isDerived",
    TokenType.T_IS_DERIVED_UNION: "isDerivedUnion",
    TokenType.T_IS_QUERY: "isQuery",
    TokenType.T_DIRECTION: "direction",
    TokenType.T_IS_UNIQUE: "isUnique",
    TokenType.T_IS_ABSTRACT: "isAbstract",
    TokenType.T_EOF: "EOF",
    TokenType.T_XMI_VERSION: "xmi:version",
    TokenType.T_XMLNS_XMI: "xmlns:xmi",
    TokenType.T_XMLNS_XSI: "xmlns:xsi",
    TokenType.T_XMLNS_ECORE: "xmlns:ecore",
    TokenType.T_XMLNS_UML: "xmlns:uml",
    TokenType.T_XMLNS_UML_NOTATION: "xmlns:umlnotation",
    TokenType.T_STRING_VALUE: '"string_value"',
    TokenType.T_DOUBLE_STRING_VALUE: '"double_string value"'
}

# create new token from TokenType and value is condition is met
def create_new_token(token_type: TokenType, value, line=0, position=0):
    if token_type == TokenType.T_STRING_VALUE or token_type == TokenType.T_DOUBLE_STRING_VALUE:
        return ValueToken(token_type, value, line, position)
    else:
        return Token(token_type, line, position)
