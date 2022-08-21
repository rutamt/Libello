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


admin_key = "1de57784114df33651b1af7ec0d35fdf0625b5cbb"
admin_secret = "89b44b05a27ebed1dc3a96b8d434627a"

# Instantiate with 'three_legged' set to True for three_legged oauth.
# Make sure to replace 'https://www.schoology.com' with your school's domain.
DOMAIN = "https://henrico.schoology.com"


auth = schoolopy.Auth(admin_key, admin_secret, three_legged=True, domain=DOMAIN)
url = auth.request_authorization()

# Open OAuth authorization webpage. Give time to authorize.
def leggedurl():
    if url is not None:
        return url


def leggedurl2():
    test_key = auth.consumer_key
    test_secret = auth.consumer_secret
    print(f"LEGGED URL PT.2 KEY: {test_key}, SECRET: {test_secret}")
