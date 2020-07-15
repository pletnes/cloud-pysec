import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


from xssec.jwt_audience_validator import JwtAudienceValidator


class TestJwtAudienceValidator:

    XSUAA_BROKER_XSAPPNAME = "brokerplanmasterapp!b123"

    def test_constructor(self):
        self.jwt_audience_validator = JwtAudienceValidator(clientId="ABC")
        assert (self.jwt_audience_validator.clientIds).__len__() == 1


    def test_tokenAudienceMatchesClientId(self):
        # audiencesfromToken = ["client", "foreignclient", "sb-test4!t1.data"]
        # scopesFromToken = []
        clientIdFromToken = "clientid1"
        self.jwt_audience_validator = JwtAudienceValidator(clientIdFromToken)
        validation_result = self.jwt_audience_validator.validateToken(clientIdFromToken=clientIdFromToken)
        assert  validation_result == True

    def test_tokenAudienceMatchesAppId(self):
        audiencesfromToken=["appId!t1"]
        self.jwt_audience_validator = JwtAudienceValidator("sb-appId!t1")
        self.jwt_audience_validator.configureTrustedClientId('appId!t1')
        validation_result = self.jwt_audience_validator.validateToken(audiencesFromToken=audiencesfromToken)
        assert validation_result == True

    def test_tokenAudienceMatchesForeignClientId(self):
        audiencesfromToken = ["client", "foreignclient", "sb-test4!t1.data"]
        self.jwt_audience_validator = JwtAudienceValidator("any")
        self.jwt_audience_validator.configureTrustedClientId('foreignclient')
        validation_result = self.jwt_audience_validator.validateToken(audiencesFromToken=audiencesfromToken)
        assert validation_result == True

    def test_clientIdMatchesTokenAudienceWithoutDo(self):
        audiencesfromToken = ["client", "sb-test4!t1.data.x"]
        self.jwt_audience_validator = JwtAudienceValidator("sb-test4!t1")
        validation_result = self.jwt_audience_validator.validateToken(audiencesFromToken=audiencesfromToken)
        assert validation_result == True

    # def test_tokenClientIdMatchesTrustedClientId(self):
    #     audiencesfromToken = ["client", "foreignclient", "sb-test4!t1.data"]
    #     self.jwt_audience_validator = JwtAudienceValidator("client")
    #     validation_result = self.jwt_audience_validator.validateToken(audiencesfromToken)
    #     assert validation_result == True

    def test_brokerClientIdMatchesCloneAudience(self):
        audiencesfromToken = ["sb-f7016e93-8665-4b73-9b46-f99d7808fe3c!b446|" + self.XSUAA_BROKER_XSAPPNAME]
        self.jwt_audience_validator = JwtAudienceValidator("sb-" + self.XSUAA_BROKER_XSAPPNAME)
        validation_result = self.jwt_audience_validator.validateToken(audiencesFromToken=audiencesfromToken)
        assert validation_result == True