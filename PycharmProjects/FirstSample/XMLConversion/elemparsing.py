import xml.etree.ElementTree as ET
import time


def _init():
    start = time.time()
    tree = ET.parse('C:/Users/amala/Downloads/RobotReports/2016-09-01_161608_output_4.3_Rerun.xml')
    # tree = ET.parse('C:/Users/amala/Downloads/RobotReports/2016-09-02_010331_2.36732.0.0_output_TTX.xml')
    root = tree.getroot()
    for suites in root.iter('suite'):
        print suites.tag, suites.attrib
        for tests in suites.iter('test'):
            print "\t", tests.tag, tests.attrib
    end = time.time()
    print(end - start)


def _another():
    source = 'C:/Users/amala/Downloads/RobotReports/2016-09-01_161608_output_4.3_Rerun.xml'
    suite_nest = 0
    for event, elem in ET.iterparse(source=source, events=('start', 'end')):
        if event == 'start':
            if elem.tag == 'suite':
                suite_nest += 1
        if event == 'end':
            if elem.tag == 'suite':
                # print (suite_nest,elem.attrib['name'])
                _process_keyword(elem)
                elem.clear()
                suite_nest -= 1


def _process_keyword(suite_elem):
    for elem in suite_elem.iter():
        if elem.tag=='test':
            print elem.tag,elem.attrib

_another()
