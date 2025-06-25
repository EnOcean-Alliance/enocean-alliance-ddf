import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

#List die productID aus den im path angegebenen DDF aus
def getProductID(path):
    tree = ET.parse(path)
    root = tree.getroot()
    device = root.find('Device')
    productID = device.get('Product_ID')

    return(productID)


def createXML(paths, IDs):
    root = minidom.Document()
    xml = root.createElement('index')
    root.appendChild(xml)

#Durchlaueft alle Pfade und die passenden IDs
#Fuegt diese in einen xml string('xml_str') zusammen
    for id in range(len(IDs)):
        productChild = root.createElement('Product')

        productChild.setAttribute('Path', str(paths[id]))
        productChild.setAttribute('Product_ID', str(IDs[id]))
        xml.appendChild(productChild)

    xml_str = root.toprettyxml(indent = "\t")
    #Entfernt die letzte Zeile
    xml_str = xml_str[:xml_str.rfind('\n')]
    xml_str = xml_str.strip()

    #Wenn der aktuell generierte Index mit dem Index aus index.xml uebereinstimmt => Test gueltig
    #Wenn nicht => Aktuell generierten Index in index.xml schreiben
    with open('index.xml') as oldIndex:
        if xml_str == oldIndex.read():
            print('Index.xml is up to date!')
            sys.exit(0)
        else:        
            with open('index.xml', 'w') as text_file:
                text_file.write(xml_str)
                print('Index.xml is updated!');
                sys.exit(0)


rootDir = '../'
exclude = set(['.github', '.git', '.'])
paths = []
productIDs = []

#Durchlaueft alle Ordner außer .github und .git
#Ignoriert alle Dateien, die nicht .xml sind und 'index.xml'
for subdir, dirs, files in os.walk(rootDir, topdown=True):
    [dirs.remove(d) for d in list(dirs) if d in exclude]

    for file in files:
       filepath = subdir + os.sep + file
       if filepath.endswith('.xml') and not filepath.endswith('index.xml'):
        productID = getProductID(filepath)

        #Alle Pfade und productIDs werden gesammelt, um sie spaeter in den Index zu schreiben
        #paths[0] = productIDs[0] usw. (Zugehoerige Werte)
        #'../test_xml/' wird nicht mit in die index.xml geschrieben 
        paths.append(os.path.relpath(filepath, '../enocean-alliance-ddf/'))
        productIDs.append(productID)
        
createXML(paths, productIDs)
