class Feature(object):
    def __init__(self, feature_name):
        self.name = feature_name
        self.stories = []

    def add_story(self, story):
        self.stories.append(story)

    def __str__(self):
        final_string = "Feature %s \n" % self.name
        for story in self.stories:
            final_string += story.__str__()
        return final_string


class Story(object):
    def __init__(self, story_name):
        self.name = story_name
        self.testcases = []

    def add_test_case(self, test_case):
        self.testcases.append(test_case)

    def __str__(self):
        final_string = "\t Story %s \n" % self.name
        for testcase in self.testcases:
            final_string += testcase.__str__()
        return final_string


class TestCase(object):
    def __init__(self, test_name):
        self.name = test_name
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def __str__(self):
        final_string = "\t \t Test Case %s \n" % self.name
        for step in self.steps:
            final_string += "\t\t\t %s \n" % step
        return final_string


class Step(object):
    def __init__(self, name, status, start_time, end_time):
        self.name = name
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return "Step:%s , Status:%s" % (self.name, self.status)
