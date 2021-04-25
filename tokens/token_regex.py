import re
from tokens.token import TokenType


# dictionary regex_rules with regex rules for each token

def compile_regex_rules():
    compiled_regex = {}
    for r in regex_rules:
        pattern = re.compile(r)
        compiled_regex[pattern] = regex_rules[r]
    return compiled_regex


regex_rules = {
    r'<(?![\S|\s])': TokenType.T_LEFT_BRACKET,
    r'>(?![\S|\s])': TokenType.T_RIGHT_BRACKET,
    r'/(?![\S|\s])': TokenType.T_SLASH,
    r'=': TokenType.T_EQUALS,
    r'uml:Model(?![\S|\s])': TokenType.T_UML_MODEL,
    r'xmi:id': TokenType.T_XMI_ID,
    r'name': TokenType.T_NAME,
    r'eAnnotations(?![\S|\s])': TokenType.T_EANNOTATIONS,
    r'source': TokenType.T_SOURCE,
    r'contents(?![\S|\s])': TokenType.T_CONTENTS,
    r'xmi:type': TokenType.T_XMI_TYPE,
    r'type': TokenType.T_TYPE,
    r'element(?![\S|\s])': TokenType.T_ELEMENT,
    r'xsi:nil': TokenType.T_XSI_NIL,
    r'packageImport(?![\S|\s])': TokenType.T_PACKAGE_IMPORT,
    r'importedPackage(?![\S|\s])': TokenType.T_IMPORTED_PACKAGE,
    r'href': TokenType.T_HREF,
    r'packagedElement(?![\S|\s])': TokenType.T_PACKAGED_ELEMENT,
    r'generalization(?![\S|\s])': TokenType.T_GENERALIZATION,
    r'general': TokenType.T_GENERAL,
    r'ownedAttribute(?![\S|\s])': TokenType.T_OWNED_ATTRIBUTE,
    r'visibility': TokenType.T_VISIBILITY,
    r'value': TokenType.T_VALUE,
    r'upperValue(?![\S|\s])': TokenType.T_UPPER_VALUE,
    r'lowerValue(?![\S|\s])': TokenType.T_LOWER_VALUE,
    r'defaultValue(?![\S|\s])': TokenType.T_DEFAULT_VALUE,
    r'aggregation': TokenType.T_AGGREGATION,
    r'association': TokenType.T_ASSOCIATION,
    r'ownedOperation(?![\S|\s])': TokenType.T_OWNED_OPERATION,
    r'ownedParameter(?![\S|\s])': TokenType.T_OWNED_PARAMETER,
    r'isStatic': TokenType.T_IS_STATIC,
    r'memberEnd': TokenType.T_MEMBER_END,
    r'ownedEnd(?![\S|\s])': TokenType.T_OWNED_END,
    r'profileApplication(?![\S|\s])': TokenType.T_PROFILE_APPLICATION,
    r'references(?![\S|\s])': TokenType.T_REFERENCES,
    r'appliedProfile(?![\S|\s])': TokenType.T_APPLIED_PROFILE,
    r'xmlns:notation': TokenType.T_XMLNS_NOTATION,
    r'children': TokenType.T_CHILDREN,
    r'target': TokenType.T_TARGET,
    r'details': TokenType.T_DETAILS,
    r'key': TokenType.T_KEY,
    r'isLeaf': TokenType.T_IS_LEAF,
    r'isOrdered': TokenType.T_IS_ORDERED,
    r'isReadOnly': TokenType.T_IS_READ_ONLY,
    r'isDerived': TokenType.T_IS_DERIVED,
    r'isDerivedUnion': TokenType.T_IS_DERIVED_UNION,
    r'isQuery': TokenType.T_IS_QUERY,
    r'direction': TokenType.T_DIRECTION,
    r'isUnique': TokenType.T_IS_UNIQUE,
    r'isAbstract': TokenType.T_IS_ABSTRACT,
    r'\Z': TokenType.T_EOF,
    r'xmi:version': TokenType.T_XMI_VERSION,
    r'xmlns:xmi': TokenType.T_XMLNS_XMI,
    r'xmlns:xsi': TokenType.T_XMLNS_XSI,
    r'xmlns:ecore': TokenType.T_XMLNS_ECORE,
    r'xmlns:uml': TokenType.T_XMLNS_UML,
    r'xmlns:umlnotation': TokenType.T_XMLNS_UML_NOTATION,
    r'\"[\S]*\"': TokenType.T_STRING_VALUE,
    r'\"[\w-]*\s[\w-]*\"': TokenType.T_DOUBLE_STRING_VALUE
}
