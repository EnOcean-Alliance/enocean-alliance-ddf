import os
import sys
import re
from lxml import etree

CHANGED_FILES = os.environ.get("CHANGED_FILES")

def validate(xml_path: str, xsd_path: str) -> bool:
    try:
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        xml_doc = etree.parse(xml_path)
        result = xmlschema.validate(xml_doc)

        if not result:
            # Print all validation errors
            for error in xmlschema.error_log:
                print(f"Validation error at line {error.line}: {error.message}")
        return result
    except Exception as e:
        print(f"Exception during validation: {e}")
        return False


#Wenn keine Aenderungen erkannt werden, bzw. eine Aenderung 1:1 rueckgaengig gemacht wurde, 
#ist der Test gueltig
if CHANGED_FILES == "":
    print("No changes detected.")
    sys.exit(0)

#Setzt den rootdir auf den aktuellen Firmenordner
rootdir = './' + CHANGED_FILES.split()[0].split('/')[0]

#Checkt, ob Dateinamen gueltig sind
#Gueltig ist nur wenn: Nur kleine Buchstaben, nur Zahlen, nur Bindestriche, muss mit '.xml' enden
for file in CHANGED_FILES.splitlines():
    file_name = os.path.basename(file)
    if not re.match(r'^[A-Za-z0-9_-]+\.xml$', file_name):
        print('::error::' + file_name + ' invalid file name!')
        sys.exit(1)

#Durchlaueft den aktuellen Firmenordner und checkt alle .xml Dateien
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith('.xml'):
            if validate(filepath, ".github/schema.xsd"):
                print(filepath + " valid!")
            else:
                print('::error::' + filepath + ' not vaild!')
                sys.exit(1)

sys.exit(0)
