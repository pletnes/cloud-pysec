import jwt
import json
from sap.xssec.config import USE_SAP_PY_JWT

if USE_SAP_PY_JWT:
    from sapjwt import jwtValidation

ALGORITHMS = ['RS256']
OPTIONS = {
    'verify_aud': False
}


class JwtValidationFacade(object):
    """
    Hides if either sapjwt or pyjwt library is used for the validation.
    """
    def __init__(self):
        if USE_SAP_PY_JWT:
            self._validator = jwtValidation()
        self._pem = None
        self._payload = None
        self._error_desc = None
        self._error_code = 0

    def decode(self, token, verify=True):
        try:
            return jwt.decode(token, verify=verify)
        except jwt.exceptions.DecodeError as e:
            raise DecodeError(e)

    def get_unverified_header(self, token):
        try:
            return jwt.get_unverified_header(token)
        except jwt.exceptions.DecodeError as e:
            raise DecodeError(e)

    def loadPEM(self, verification_key):
        self._pem = verification_key
        if USE_SAP_PY_JWT:
            return self._validator.loadPEM(verification_key)
        else:
            return 0

    def checkToken(self, token):
        if USE_SAP_PY_JWT:
            self._validator.checkToken(token)
        else:
            try:
                self._payload = jwt.decode(token, self._pem, algorithms=ALGORITHMS, options=OPTIONS)
                self._error_desc = ''
                self._error_code = 0
            except jwt.exceptions.InvalidTokenError as e:
                self._error_desc = str(e)
                self._error_code = 1

    def getErrorDescription(self):
        if USE_SAP_PY_JWT:
            return self._validator.getErrorDescription()
        else:
            return self._error_desc

    def getErrorRC(self):
        if USE_SAP_PY_JWT:
            return self._validator.getErrorRC()
        else:
            return self._error_code

    def getJWPayload(self):
        if USE_SAP_PY_JWT:
            return json.loads(self._validator.getJWPayload())
        else:
            return self._payload


class DecodeError(Exception):
    pass