import xml.etree.ElementTree as ET
import time

from FirstSample.XMLConversion.Components import Feature,Story,TestCase,Step


def _init():
    start = time.time()
    tree = ET.parse('XMLFiles/2016-09-01_161608_output_4.3_Rerun.xml')
    root = tree.getroot()
    for suites in root.iter('suite'):
        print(suites.tag, suites.attrib)
        for tests in suites.iter('test'):
            print("\t", tests.tag, tests.attrib)
    end = time.time()
    print(end - start)


feature_list = []


def _process_keyword(suite_elem):
    for elem in suite_elem.iter():
        if elem.tag == 'test':
            print(elem.tag, elem.attrib)


def _another():
    source = 'XMLFiles/2016-09-01_161608_output_4.3_Rerun.xml'
    for event, elem in ET.iterparse(source=source, events=('start', 'end')):
        if event == 'start':
            print("start: ", elem.tag, elem.attrib)
        if event == 'end':
            print("End: ", elem.tag, elem.attrib)
            if elem.tag == 'kw':
                current_step = _prepare_step(elem)
                print("====>")
                print(current_step)
                print("<====>")
                elem.clear()


def _prepare_step(keyword_elem):
    # Todo: Need to append Logging later on
    step_status_details = keyword_elem.find('status')
    step_name = keyword_elem.get('name')
    step_status = step_status_details.get('status')
    step_start_time = step_status_details.get('starttime')
    step_end_time = step_status_details.get('endtime')

    new_step = Step(step_name, step_status, step_start_time, step_end_time)
    return new_step


_another()

# test=TestCase("First Test")
# test.add_step("step 1")
# test.add_step("step 2")
# test.add_step("step 3")
# print(test)
#
# story1=Story("First Sotry")
# story1.add_test_case(test)
#
# feature=Feature("First Feature")
# feature.add_story(story1)
#
# print(feature)
