import os
import sys
import re
from lxml import etree

CHANGED_FILES = os.environ.get("CHANGED_FILES", "")

# Separate changed files and exclude the generated index.xml
changed_files = [
    file
    for file in CHANGED_FILES.split("|")
    if file and file != "index.xml"
]


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

def validate_with_fallback(xml_path: str, primary_xsd: str, fallback_xsd: str) -> bool:
    if validate(xml_path, primary_xsd):
        return True
    return validate(xml_path, fallback_xsd)

# Wenn keine relevanten Änderungen erkannt werden, ist der Test gültig.
# Die automatisch generierte index.xml wird ignoriert.
if not changed_files:
    print("No changes detected.")
    sys.exit(0)

# Setzt den rootdir auf den aktuellen Firmenordner
rootdir = './' + changed_files[0].split('/')[0]

# Checkt, ob Dateinamen gültig sind
# Gültig ist nur wenn: Buchstaben, Zahlen, Bindestriche,
# Unterstriche und die Endung '.xml'
for file in changed_files:
    file_name = os.path.basename(file)
    if not re.match(r'^[A-Za-z0-9_-]+\.xml$', file_name):
        print('::error::' + file_name + ' invalid file name!')
        sys.exit(1)

PRIMARY_XSD = ".github/schema.xsd"
FALLBACK_XSD = ".github/schemaV2.0.xsd"

# Durchläuft den aktuellen Firmenordner und prüft alle XML-Dateien
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith('.xml'):
            if validate_with_fallback(
                filepath,
                PRIMARY_XSD,
                FALLBACK_XSD
            ):
                print(filepath + " valid!")
            else:
                print('::error::' + filepath + ' not vaild!')
                sys.exit(1)

sys.exit(0)
