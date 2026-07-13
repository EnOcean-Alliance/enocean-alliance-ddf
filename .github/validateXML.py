import os
import re
import sys

from lxml import etree


CHANGED_FILES = os.environ.get("CHANGED_FILES", "")

PRIMARY_XSD = ".github/schema.xsd"
FALLBACK_XSD = ".github/schemaV2.0.xsd"


def validate(xml_path: str, xsd_path: str) -> bool:
    try:
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        xml_doc = etree.parse(xml_path)
        result = xmlschema.validate(xml_doc)

        if not result:
            for error in xmlschema.error_log:
                print(
                    f"Validation error in {xml_path} "
                    f"at line {error.line}: {error.message}"
                )

        return result

    except Exception as error:
        print(f"Exception while validating {xml_path}: {error}")
        return False


def validate_with_fallback(
    xml_path: str,
    primary_xsd: str,
    fallback_xsd: str,
) -> bool:
    if validate(xml_path, primary_xsd):
        return True

    print(
        f"{xml_path} is not valid according to {primary_xsd}. "
        f"Trying {fallback_xsd}."
    )

    return validate(xml_path, fallback_xsd)


# The workflow must configure tj-actions/changed-files with:
#
# with:
#   separator: "|"
#
# index.xml is generated automatically and is not a DDF XML document.
changed_files = [
    file_path.strip()
    for file_path in CHANGED_FILES.split("|")
    if file_path.strip() and file_path.strip() != "index.xml"
]


# No relevant DDF files changed.
if not changed_files:
    print("No DDF XML changes detected. index.xml is ignored.")
    sys.exit(0)


# Use the first changed file's top-level directory as the company directory.
rootdir = os.path.join(".", changed_files[0].split("/", 1)[0])

print(f"Changed DDF files: {changed_files}")
print(f"Directory to validate: {os.path.abspath(rootdir)}")


# Validate changed filenames.
for file_path in changed_files:
    file_name = os.path.basename(file_path)

    if not re.fullmatch(r"[A-Za-z0-9_-]+\.xml", file_name):
        print(f"::error::{file_name} invalid file name!")
        sys.exit(1)


if not os.path.isdir(rootdir):
    print(f"::error::Directory does not exist: {rootdir}")
    sys.exit(1)


# Validate every XML file in the affected company directory.
for subdir, dirs, files in os.walk(rootdir):
    dirs.sort()
    files.sort()

    for file_name in files:
        if not file_name.lower().endswith(".xml"):
            continue

        filepath = os.path.join(subdir, file_name)

        if validate_with_fallback(
            filepath,
            PRIMARY_XSD,
            FALLBACK_XSD,
        ):
            print(f"{filepath} valid!")
        else:
            print(f"::error::{filepath} not valid!")
            sys.exit(1)


sys.exit(0)
