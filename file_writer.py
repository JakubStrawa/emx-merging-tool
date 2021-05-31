import parser_objects
from tokens.token import *


class FileWriter:
    def __init__(self, filepath, tree):
        self.filepath = filepath
        self.tree = tree
        self.file = open(filepath, 'w', encoding='utf-8', errors='replace')

    def write_to_file(self):
        self.file.write('<?xml version="1.0" encoding="UTF-8"?>\n<!--xtools2_universal_type_manager-->\n<!--Rational Software Architect Designer 9.7.0-->\n<?com.ibm.xtools.emf.core.signature <signature id="com.ibm.xtools.mmi.ui.signatures.diagram" version="7.0.0"><feature description="" name="Rational Modeling Platform (com.ibm.xtools.rmp)" url="" version="7.0.0"/></signature>?>\n<?com.ibm.xtools.emf.core.signature <signature id="com.ibm.xtools.uml.msl.model" version="7.0.0"><feature description="" name="com.ibm.xtools.ruml.feature" url="" version="7.0.0"/></signature>?>\n')
        self.write_model_description()
        self.write_file_description()
        self.write_package_imports()
        self.write_packaged_elements()
        self.write_profiles()
        self.file.write("</uml:Model>")
        self.close_file()

    def write_model_description(self):
        self.file.write(f'<uml:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore" xmlns:notation="http://www.eclipse.org/gmf/runtime/1.0.2/notation" xmlns:uml="http://www.eclipse.org/uml2/3.0.0/UML" xmlns:umlnotation="http://www.ibm.com/xtools/1.5.3/Umlnotation" xmi:id={self.tree.id} name={self.tree.name}>\n')

    def write_file_description(self):
        self.file.write(f'<eAnnotations xmi:id={self.tree.file_description.id} source={self.tree.file_description.source}>\n')
        for t in self.tree.file_description.graphic:
            if t.token_type == TokenType.T_RIGHT_BRACKET:
                self.file.write(t.token_type.to_string() + "\n")
            elif t.token_type == TokenType.T_STRING_VALUE:
                self.file.write(t.value + " ")
            elif t.token_type == TokenType.T_CONTENTS or t.token_type == TokenType.T_CHILDREN or t.token_type == TokenType.T_ELEMENT:
                self.file.write(t.token_type.to_string() + " ")
            else:
                self.file.write(t.token_type.to_string())

    def write_package_imports(self):
        for p in  self.tree.package_imports:
            self.file.write(f'  <packageImport xmi:id={p.id}>\n')
            self.file.write(f'    <importedPackage xmi:type={p.type} href={p.href}/>\n')
            self.file.write('  </packageImport>\n')

    def write_packaged_elements(self):
        for p in self.tree.packaged_elements:
            if type(p) == parser_objects.Class:
                self.write_class(p)
            else:
                self.write_association(p)

    def write_class(self, p):
        self.file.write(f'  <packagedElement xmi:type="uml:Class" xmi:id={p.id} name={p.name}')
        if p.visibility is not None:
            self.file.write(f' visibility={p.visibility}')
        if p.isLeaf != "false":
            self.file.write(f' isLeaf={p.isLeaf}')
        if p.isAbstract != "false":
            self.file.write(f' isAbstract={p.isAbstract}')
        self.file.write('>\n')
        # stereotypes
        if p.stereotypes is not None:
            self.file.write(f'    <eAnnotations xmi:id={p.stereotypes.id} source={p.stereotypes.source}>\n')
            for s in p.stereotypes.stereotypes:
                self.file.write(f'      <details xmi:id={s[0]} key={s[1]}/>\n')
            self.file.write('    </eAnnotations>\n')
        # generalizations
        if p.generalizations is not None:
            for g in p.generalizations:
                self.file.write(f'    <generalization xmi:id={g.id} general={g.general}/>\n')
        # attributes
        if p.attributes is not None:
            for a in p.attributes:
                self.file.write(f'    <ownedAttribute xmi:id={a.id} name={a.name} visibility={a.parameters.visibility} isLeaf={a.parameters.isLeaf} isStatic={a.parameters.isStatic} isOrdered={a.parameters.isOrdered} isReadOnly={a.parameters.isReadOnly} isDerived={a.parameters.isDerived} isDerivedUnion={a.parameters.isDerivedUnion} ')
                if a.parameters.short_type is not None:
                    self.file.write(f'type={a.parameters.short_type} ')
                if a.parameters.aggregation is not None:
                    self.file.write(f'aggregation={a.parameters.aggregation} ')
                if a.parameters.association is not None:
                    self.file.write(f'association={a.parameters.association}')
                self.file.write('>\n')
                if a.type is not None:
                    self.file.write(f'      <type xmi:type={a.type[0]} href={a.type[1]}/>\n')
                if a.upper_limit is not None:
                    self.file.write(f'      <upperValue xmi:type={a.upper_limit.type} xmi:id={a.upper_limit.id}')
                    if a.upper_limit.value is not None:
                        self.file.write(f' value={a.upper_limit.value}')
                    self.file.write('/>\n')
                if a.lower_limit is not None:
                    self.file.write(f'      <lowerValue xmi:type={a.lower_limit.type} xmi:id={a.lower_limit.id}')
                    if a.lower_limit.value is not None:
                        self.file.write(f' value={a.lower_limit.value}')
                    self.file.write('/>\n')
                if a.default_value is not None:
                    self.file.write(f'      <defaultValue xmi:type={a.default_value.type} xmi:id={a.default_value.id}')
                    if a.default_value.value is not None:
                        self.file.write(f' value={a.default_value.value}')
                    self.file.write('/>\n')
                self.file.write('    </ownedAttribute>\n')
        # operations
        if p.operations is not None:
            for o in p.operations:
                self.file.write(f'    <ownedOperation xmi:id={o.id} name={o.name} visibility={o.visibility} isLeaf={o.isLeaf} isStatic={o.isStatic} isAbstract={o.isAbstract} isQuery={o.isQuery}>\n')
                if o.ownedParameters is not None:
                    for p in o.ownedParameters:
                        self.file.write(f'      <ownedParameter xmi:id={p.id} name={p.name} isOrdered={p.isOrdered} isUnique={p.isUnique} direction={p.direction}')
                        if p.type is not None:
                            if type(p.type) == str:
                                self.file.write(f' type={p.type}>\n')
                            else:
                                self.file.write(f'>\n')
                                self.file.write(f'        <type xmi:type={p.type[0]} href={p.type[1]}/>\n')
                        else:
                            self.file.write(f'>\n')
                        if p.upper_limit is not None:
                            self.file.write(f'        <upperValue xmi:type={p.upper_limit.type} xmi:id={p.upper_limit.id}')
                            if p.upper_limit.value is not None:
                                self.file.write(f' value={p.upper_limit.value}')
                            self.file.write('/>\n')
                        if p.lower_limit is not None:
                            self.file.write(f'        <lowerValue xmi:type={p.lower_limit.type} xmi:id={p.lower_limit.id}')
                            if p.lower_limit.value is not None:
                                self.file.write(f' value={p.lower_limit.value}')
                            self.file.write('/>\n')
                        if p.default_value is not None:
                            self.file.write(f'        <defaultValue xmi:type={p.default_value.type} xmi:id={p.default_value.id}')
                            if p.default_value.value is not None:
                                self.file.write(f' value={p.default_value.value}')
                            self.file.write('/>\n')
                        self.file.write('      </ownedParameter>\n')
                self.file.write('    </ownedOperation>\n')
        self.file.write('  </packagedElement>\n')



    def write_association(self, p):
        self.file.write(f'  <packagedElement xmi:type="uml:Association" xmi:id={p.id} memberEnd={p.member_end}')
        if p.owned_end is not None:
            self.file.write('>\n')
            self.file.write(f'    <ownedEnd xmi:id={p.owned_end.id} name={p.owned_end.name} visibility={p.owned_end.visibility} type={p.owned_end.type} association={p.owned_end.association}>\n')
            if p.owned_end.upper_limit is not None:
                self.file.write(f'      <upperValue xmi:type={p.owned_end.upper_limit.type} xmi:id={p.owned_end.upper_limit.id}')
                if p.owned_end.upper_limit.value is not None:
                    self.file.write(f' value={p.owned_end.upper_limit.value}')
                self.file.write('/>\n')
            if p.owned_end.lower_limit is not None:
                self.file.write(f'      <lowerValue xmi:type={p.owned_end.lower_limit} xmi:id={p.owned_end.lower_limit.id}')
                if p.owned_end.lower_limit.value is not None:
                    self.file.write(f' value={p.owned_end.lower_limit.value}')
                self.file.write('/>\n')
            self.file.write('    </ownedEnd>')
        else:
            self.file.write('/>\n')
        self.file.write('  </packagedElement>\n')

    def write_profiles(self):
        for p in self.tree.profiles:
            self.file.write(f'''  <profileApplication xmi:id={p.id}>
    <eAnnotations xmi:id={p.eannotation.id} source={p.eannotation.source}>
      <references xmi:type={p.eannotation.type} href={p.eannotation.href}/>
    </eAnnotations>
    <appliedProfile href={p.href}/>
  </profileApplication>\n''')

    def close_file(self):
        self.file.close()
