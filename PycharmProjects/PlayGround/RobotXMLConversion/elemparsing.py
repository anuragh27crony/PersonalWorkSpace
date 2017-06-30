import xml.etree.ElementTree as ET
from RobotXMLConversion.Components import Feature, Story, TestCase, Step

feature_list = []


def _another():
    source = 'resources/2016-09-01_161608_output_4.3_Rerun.xml'
    for event, elem in ET.iterparse(source=source, events=('start', 'end')):
        has_test_tag = False
        test_case = None
        suite_count=1
        story = None

        # TODO: First suite is feature
        # TODO: Append Name from Second suite till test case for Story
        if event == 'start':
            print("start: ", elem.tag, elem.attrib)
            if elem.tag == 'test':
                has_test_tag = True
                # TODO: Append name from TestCase till last keyword
                test_case = TestCase(elem.key('name'))
        if event == 'end':
            print("End: ", elem.tag, elem.attrib)
            if elem.tag == 'kw':
                current_step = _prepare_step(elem)
                print("====>")
                print(current_step)
                if has_test_tag:
                    test_case.add_step(current_step)
                print("<====>")
                elem.clear()
            if elem.tag == 'test':
                pass

            if elem.tag == 'suite':
                pass


def _prepare_step(keyword_elem):
    # Todo: Need to append Logging later on
    step_status_details = keyword_elem.find('status')
    step_name = keyword_elem.get('name')
    step_status = step_status_details.get('status')
    step_start_time = step_status_details.get('starttime')
    step_end_time = step_status_details.get('endtime')

    new_step = Step(step_name, step_status, step_start_time, step_end_time)
    return new_step


def _prepare_test_case(testcase_elem):
    pass


def _prepare_story(story_elem):
    pass


_another()
