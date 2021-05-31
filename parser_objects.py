class Model:
    def __init__(self, file_desc, packages, elements, profiles, id="", name=""):
        self.file_description = file_desc
        self.package_imports = packages
        self.packaged_elements = elements
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
    def __init__(self, id, name, visibility, isLeaf, isAbstract, stereotypes, generalizations, attributes, operations):
        self.id = id
        self.name = name
        self.visibility = visibility
        self.isLeaf = isLeaf
        self.isAbstract = isAbstract
        self.stereotypes = stereotypes
        self.generalizations = generalizations
        self.attributes = attributes
        self.operations = operations


class Stereotype:
    def __init__(self, id, source, stereotypes):  # stereotypes[(id, key)]
        self.id = id
        self.source = source
        self.stereotypes = stereotypes


class Generalization:
    def __init__(self, id, general):
        self.id = id
        self.general = general


class Attribute:
    def __init__(self, id, name, parameters, type, upper_limit, lower_limit, default_value):
        self.id = id
        self.name = name
        self.parameters = parameters
        self.type = type
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.default_value = default_value


class AttributeParameters:
    def __init__(self, visibility, isLeaf, isStatic, isOrdered, isUnique, isReadOnly, isDerived, isDerivedUnion, aggregation,
                 association, type):
        self.visibility = visibility
        self.isLeaf = isLeaf
        self.isStatic = isStatic
        self.isOrdered = isOrdered
        self.isUnique = isUnique
        self.isReadOnly = isReadOnly
        self.isDerived = isDerived
        self.isDerivedUnion = isDerivedUnion
        self.aggregation = aggregation
        self.association = association
        self.short_type = type


class Limit:
    def __init__(self, type, id, value):
        self.type = type
        self.id = id
        self.value = value


class Operation:
    def __init__(self, id, name, visibility, isLeaf, isStatic, isAbstract, isQuery, ownedParameters):
        self.id = id
        self.name = name
        self.visibility = visibility
        self.isLeaf = isLeaf
        self.isStatic = isStatic
        self.isAbstract = isAbstract
        self.isQuery = isQuery
        self.ownedParameters = ownedParameters


class OwnedParameter:
    def __init__(self, id, name, type, isOrdered, isUnique, direction, upper, lower, default_value):
        self.id = id
        self.name = name
        self.type = type
        self.isOrdered = isOrdered
        self.isUnique = isUnique
        self.direction = direction
        self.upper_limit = upper
        self.lower_limit = lower
        self.default_value = default_value


class Association:
    def __init__(self, id, member_end, owned_end=None):
        self.id = id
        self.member_end = member_end
        self.owned_end = owned_end


class OwnedEnd:
    def __init__(self, id, name, visibility, type, association, upper_limit, lower_limit):
        self.id = id
        self.name = name
        self.visibility = visibility
        self.type = type
        self.association = association
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit


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
