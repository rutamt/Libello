"""
Misc utilities for use throughout the app.
"""

import schoolopy


def check_if_duplicates(list_of_elems):
    """Check if given list contains any duplicates

    Credit: https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
    """
    print("check_if_duplicates()")
    set_of_elems = set()
    for elem in list_of_elems:
        if elem in set_of_elems:
            return True
        else:
            set_of_elems.add(elem)
    return False


def get_assignments(key, secret, classes=None):
    """Use the Schoology API to return the user's assignments"""
    print("get_assignments()")
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))

    if classes == ["default"] or classes == "default":
        return "NONE"
    else:
        cl_list = []
        cl_num = 0
        new_cl = []
        classes_length = len(classes)
        class_int = 0
        for i in range(0, classes_length):
            current_class_assignemnts = []
            current_class_assignemnts.append(sc.get_assignments(classes[class_int]))
            cl_list += current_class_assignemnts
            class_int += 1

        # print(cl_list)
        # print(f"CLASSES LENGTH: {classes_length}")
        # for i in classes:
        #     new_cl.append(sc.get_assignments(i))
        #     # cl_list.append(new_cl)
        #     # cl_list += sc.get_assignments(i)
        # cl_list.append(new_cl)
        # # print(cl_list)
        return cl_list
