import os
import sys
from lxml import etree


def validate(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result


rootdir = os.getcwd()
#Durchlaueft das gesamte Repo und checkt alle .xml Dateien

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith('.xml'):
            if validate(filepath, "./schema.xsd"):
                print(filepath + " valid!")
            else:
                print(filepath + " not vaild!")
                sys.exit(1)

sys.exit(0)
