import xml.etree.ElementTree as etree

new_feed=etree.Element("{newNameSpace}feed",attrib={'xml:lang':'en'})
print(etree.tostring(new_feed))