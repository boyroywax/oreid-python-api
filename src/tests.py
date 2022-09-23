import os

from modules.oreid_api import OreIdApi


oreid_api: OreIdApi = OreIdApi()
color = '\033[96m'
endcolor = '\033[0m'


def color_line(line: str) -> str:
    print(f"{color}{line}{endcolor}")


def main():
    #
    color_line("Fail at calling an API endpoint")
    #
    oreid_api.raw_action(
        ["DELETE"],
        {
            "endpoint": "/test",
            "data": {
                "test": "test"
            }
        }
    )

    #
    color_line("Succeed getting an App Access Token")
    #
    oreid_api.get_access_token()

    #
    color_line("Succeed getting an App Access Token w/ password")
    #
    oreid_api.get_access_token({
        "newAccountPassword": "Password123!"
    })

    #
    color_line("Succeed getting all the supported chain info")
    #
    oreid_api.get_chains()

    #
    color_line("Succees logging in a user with google token")
    #
    oreid_api.new_user_with_token(os.getenv("GOOGLE_ID_TOKEN"))

    #
    color_line("Succeed getting the EOS chain info")
    #
    oreid_api.get_chains("telos_test")

    #
    color_line("Succeed creating a TLOS chain account for the user")
    #
    oreid_api.new_chain_account({
        "account_name": os.getenv("TEST_USER_OREID"),
        "account_type": "native",
        "chain_network": "telos_test",
        "user_password": os.getenv("TEST_USER_PASSWORD")
    })

    #
    color_line("Succeed getting the info of the test user")
    #
    oreid_api.get_user(os.getenv("TEST_USER_OREID"))

    #
    color_line("Fail creating a new custodial account")
    #
    oreid_api.new_custodial_account({
        "name": "John Q Test",
        "user_name": "jqtest",
        "email": "email@example.com",
        "picture": "https://example.com/media/user.1234.jpg",
        "user_password": "Password123!",
        "phone": "+12223334444",
        "account_type": "native"
    })


main()
