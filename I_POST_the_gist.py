import getpass
import requests


def main():
    username = input('github username: ')
    pw = getpass.getpass('password: ')

    # -------------- #
    resp = requests.post(
        url = "https://api.github.com/gists",
        json = {
            "description": "look at this one, dan and kodie",
            "public": True,
            "files": {
                "I_GET_the_gist.txt": {
                    "content": "when i gist, u gist, just like that"
                }
            }
        },
        auth = (username,pw)
    )
    # -------------- #

    assert ((resp.status_code == 201)
            or (resp.status_code == 401
                and resp.json()['message'] == 'Must specify two-factor authentication OTP code.'))

    # don't need to return anything, after you've posted just exit


if __name__ == '__main__':
    main()