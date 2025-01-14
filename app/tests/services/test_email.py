import unittest
from unittest.mock import patch
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from src.services.email import send_email_alert

###########
#  Tests  #
###########

class TestSendEmailAlert(unittest.TestCase):

    @patch("src.services.email.ses_client")
    def test_send_email_alert_success(self, mock_ses):
        mock_ses.send_email.return_value = {"MessageId": "test-id"}
        response = send_email_alert("Justification text", "Bitcoin")
        self.assertIsNotNone(response)
        self.assertIn("MessageId", response)

    @patch("src.services.email.ses_client")
    def test_send_email_alert_no_credentials(self, mock_ses):
        mock_ses.send_email.side_effect = NoCredentialsError()
        response = send_email_alert("Justification text", "Ethereum")
        self.assertIsNone(response)

    @patch("src.services.email.ses_client")
    def test_send_email_alert_partial_credentials(self, mock_ses):
        mock_ses.send_email.side_effect = PartialCredentialsError(
            provider="test",
            cred_var="test_var",
        )
        response = send_email_alert("Justification text", "Litecoin")
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
