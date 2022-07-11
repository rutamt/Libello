import schoolopy

def get_assignments(key, secret, classes = None ):

    # Create a Schoology instance with Auth as a parameter.

    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))


    if classes == None:
        return "NONE"
    else:
        cl_list = []

        for i in classes:
            cl_list += (sc.get_assignments(i))
        return cl_list
