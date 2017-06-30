import untangle


def _init_():
    obj = untangle.parse('C:/Users/amala/Downloads/RobotReports/2016-09-01_161608_output_4.3_Rerun.xml')
    print(type(obj.robot.children))
    print_name(obj.robot, 0)


def print_name(element, counter):
    if len(element.children) is not 0:
        print(final_string(element._name, counter))
        for child_items in element.children:
            print_name(child_items, counter + 1)
    else:
        print(final_string(element._name,counter))


def final_string(element_name,counter):
    finalstring = ""
    for i in range(0, counter):
        finalstring += "-> "
    finalstring += element_name
    return finalstring


_init_()
