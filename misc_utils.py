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
    """Use the Schoology API to return the user's assignments
    """
    print("get_assignments()")
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))

    if classes is None or classes == "default":
        return "NONE"
    else:
        cl_list = []
        for i in classes:
            cl_list += (sc.get_assignments(i))
        return cl_list
