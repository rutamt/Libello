import schoolopy
import webbrowser as wb
import config
import time
import datetime

def get_assignments():

    config.name = None
    DOMAIN = "https://henrico.schoology.com"
    bl1 = "5167125116"
    bl2 = "5167125194"

    # This key can't really do anything, so it should be fine to leave here.
    key = "1de57784114df33651b1af7ec0d35fdf0625b5cbb"
    secret = "89b44b05a27ebed1dc3a96b8d434627a"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    # Request authorization URL to open in another window.

    url = auth.request_authorization()

    # Open OAuth authorization webpage. Give time to authorize.
    if url is not None:
        wb.open(url, new=2)


    # Wait for user to accept or deny the request.
    time.sleep(10)
    # Authorize the Auth instance as the user has either accepted or not accepted the request.
    # Returns False if failed.

    if not auth.authorize():
        raise SystemExit('Account was not authorized.')

    # Create a Schoology instance with Auth as a parameter.
    sc = schoolopy.Schoology(auth)
    # sc.limit = 10  # Only retrieve 10 objects max

    my_name = str(sc.get_me().name_display).split()[0]
    config.name = my_name
    assignments = sc.get_assignments(bl1) + sc.get_assignments(bl2)



    return assignments