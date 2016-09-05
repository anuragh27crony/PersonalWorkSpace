import xml.etree.ElementTree as ET
import time


def _init():
    start = time.time()
    tree = ET.parse('XMLFiles/2016-09-01_161608_output_4.3_Rerun.xml')
    # tree = ET.parse('XMLFiles/2016-09-02_010331_2.36732.0.0_output_TTX.xml')
    root = tree.getroot()
    for suites in root.iter('suite'):
        print(suites.tag, suites.attrib)
        for tests in suites.iter('test'):
            print("\t", tests.tag, tests.attrib)
    end = time.time()
    print(end - start)


feature_list=[]

class feature(object):
    def __init__(self,feature_name):
        self.name=feature_name
        self.stories=[]

    def add_story(self,story):
        self.stories.append(story)

    def __str__(self):
        final_string="Feature %s \n" % self.name
        for story in self.stories:
            final_string += story.__str__()
        return final_string


class story(object):
    def __init__(self,story_name):
        self.name=story_name
        self.testcases=[]

    def add_test_case(self,test_case):
        self.testcases.append(test_case)

    def __str__(self):

        final_string="\t Story %s \n" % self.name
        for testcase in self.testcases:
            final_string += testcase.__str__()
        return final_string


class testcase(object):
    def __init__(self, test_name):
        self.name=test_name
        self.steps=[]

    def add_step(self,step):
        self.steps.append(step)

    def __str__(self):
        final_string="\t \t Test Case %s \n" % self.name
        for step in self.steps:
            final_string += "\t\t\t %s \n" % step
        return final_string


def _another():
    source = 'XMLFiles/2016-09-01_161608_output_4.3_Rerun.xml'
    suite_nest = 0
    for event, elem in ET.iterparse(source=source, events=('start', 'end')):
        if event == 'start':
            print("start: ",elem.tag,elem.attrib)
            # if elem.tag == 'suite':
            #     suite_nest += 1
        if event == 'end':
            print("End: ",elem.tag,elem.attrib)
            if elem.tag == 'kw':
                step = _prepare_step(elem)
                elem.clear()
        # elem.clear()
            # if elem.tag == 'kw':
            #     if suite_nest > 1:
            #         _process_keyword(elem)
            #         elem.clear()
            #         suite_nest -= 1


def _prepare_step(keyword_elem):
    step_data=''
    step_data += keyword_elem.attrib['name']
    print("====>")
    for elem in keyword_elem.iter():
        print(elem.tag, elem.attrib,elem.keys())
    print(''.join(keyword_elem.itertext()))
    # for text in keyword_elem.itertext():
    #     print(text)
    print("<====>")
    return step_data


def _process_keyword(suite_elem):
    for elem in suite_elem.iter():
        if elem.tag == 'test':
            print(elem.tag, elem.attrib)


_another()

# test=testcase("First Test")
# test.add_step("step 1")
# test.add_step("step 2")
# test.add_step("step 3")
# print(test)
#
# story1=story("First Sotry")
# story1.add_test_case(test)
#
# feature=feature("First Feature")
# feature.add_story(story1)
#
# print(feature)