import os

from modules.OreIdApi import OreIdApi
from modules.GoogleAuth import googleOauth


def main():
    # google_token = googleOauth()
    # print(google_token)

    #
    # Fail at calling an API endpoint
    #
    OreIdApi().raw_action(
        ["DELETE"],
        {
            "endpoint": "/test",
            "data": {
                "test": "test"
            }
        }
    )

    #
    # Succeed getting an App Access Token
    #
    OreIdApi().get_access_token()

    #
    # Succeed getting an App Access Token w/ password
    #
    OreIdApi().get_access_token({
        "newAccountPassword": "1234"
    })

    #
    # Succeed getting all the supported chain info
    #
    OreIdApi().get_chains()

    #
    # Succeed getting the EOS chain info
    #
    OreIdApi().get_chains("eos_main")

    #
    # Succeed getting the info of the test user
    #
    OreIdApi().get_user(os.getenv("TEST_USER_OREID"))

    #
    # Fail creating a new custodial account
    #
    OreIdApi().new_custodial_account({
        "name": "John Q Test",
        "user_name": "jqtest",
        "email": "email@example.com",
        "picture": "https://example.com/media/user.1234.jpg",
        "user_password": "Password123!",
        "phone": "+12223334444",
        "account_type": "native"
    })


main()
