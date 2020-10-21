import os
from pathlib import Path
import google.auth._default


class AuthenticationError(Exception):
    pass


def gcp_initailize():
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') and os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') != '':
        return
    try:
        print('Trying Google default authentication.')
        google.auth._default.default()
        print('Google default authentication passed.')
    except:  # pylint: disable=bare-except # We are not raising anything here.
        print('Google default authentication failed.')
        print('Getting environment GOOGLE_APPLICATION_CREDENTIALS.')
        os.environ.setdefault(
            'GOOGLE_APPLICATION_CREDENTIALS',
            os.path.join(
                Path(__file__).resolve().parent.parent.parent,
                '.secret/credential.json')
        )
        try:
            google.auth._default.default()
            print('Google authentication passed.')
        except:
            raise AuthenticationError(
                'Google authentication failed.') from None
