import xml.etree.ElementTree as etree


def parse_xml(filepath):
    tree = etree.parse(filepath)
    root = tree.getroot()

    return root


def check_duplicates(listofids):
    if len(listofids) == len(set(listofids)):
        return False
    else:
        return True


def checkids(root):
    component = root.find('{urn:hl7-org:v3}component/{urn:hl7-org:v3}structuredBody')
    output = []
    for i, child in enumerate(component):
        ids = []
        for subchild in child.iter():
            if subchild.tag == '{urn:hl7-org:v3}title':
                title = subchild.text
            if subchild.tag == '{urn:hl7-org:v3}id':
                if 'root' in subchild.attrib:
                    ids.append(subchild.attrib['root'])
                else:
                    print("ERROR", subchild.tag, subchild.attrib)
        try:
            output.append((title, check_duplicates(ids)))
        except:
            print("error with", i)

    return output

def tup_to_dict(tuple, dictionary):
    for (a,b) in tuple:
        dictionary[a] = b
    return dictionary


