import xml.etree.ElementTree as etree


def print_child_elems(root_elem,append_str=""):
    append_str+=str(root_elem.tag)
    for child_elem in root_elem:
        if len(child_elem) > 0:
            print_child_elems(child_elem,append_str+" >> ")
        else:
            print(str(append_str)+" >> "+str(child_elem.tag)+" -- "+ str(child_elem.attrib))


tree=etree.parse('XMLFiles/feed.xml')
root=tree.getroot()

print("print Root: "+str(root))
print("print type of Root: "+str(type(root)))
print("print tag: "+str(root.tag))
print("print len: "+str(len(root)))
print_child_elems(root)

print(etree.tostring(root))

