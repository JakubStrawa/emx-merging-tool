import tokens.token

class Model:
    def __init__(self, file_desc, packages, classes, relationships, profiles, id="", name=""):
        self.file_description = file_desc
        self.packages = packages
        self.classes = classes
        self.relationships = relationships
        self.profiles = profiles
        self.id = id
        self.name = name

class FileDescription:
    def __init__(self, graphic, id="", source=""):
        self.graphic = graphic
        self.id = id
        self.source = source

class GraphicDescription:
    def __init__(self):
        self.graphic = []

class ImportedPackage:
    def __init__(self, id="", type="", href=""):
        self.id = id
        self.type = type
        self.href = href

class Class:
    def __init__(self, id, name, visibility, isleaf, isabstract, stereotypes, generalizations, attributes, operations):
        pass

class Stereotype:
    def __init__(self, id, source, stereotypes):    #stereotypes[(id, key)]
        self.id = id
        self.source = source
        self.stereotypes = stereotypes

class Generalization:
    def __init__(self, id, general):
        self.id = id
        self.general = general

class Attribute:
    def __init__(self, id, name, parameters, type, upper_limit, lower_limit, upper_value):
        self.id = id
        self.name = name
        self.parameters = parameters
        self.type = type
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.upper_value = upper_value

class AttributeParameters:
    def __init__(self, visibility, isLeaf, isStatic, isOrdered, isReadOnly, isDerived, isDerivedUnion, aggregation, association):
        self.visibility = visibility
        self.isLeaf = isLeaf
        self.isStatic = isStatic
        self.isOrdered = isOrdered
        self.isReadOnly = isReadOnly
        self.isDerived = isDerived
        self.isDerivedUnion = isDerivedUnion
        self.aggregation = aggregation
        self.association = association

class Limit:
    def __init__(self, type, id, value):
        pass

class UpperValue:
    def __init__(self, type, id, value):
        pass

class Operation:
    def __init__(self, id, name, visibility, isLeaf, isStatic, isQuery, ownedparameters):
        pass

class OwnedParameter:
    def __init__(self, id, name, type, isOrdered, isUnique, direction, upper, lower, default_value):
        pass

class Relationship:
    def __init__(self):
        pass

class ProfileApplication:
    def __init__(self, eannotation, id="", href=""):
        self.eannotation = eannotation
        self.id = id
        self.href = href

class EAnnotation:
    def __init__(self, id="", source="", type="", href=""):
        self.id = id
        self.source = source
        self.type = type
        self.href = href
