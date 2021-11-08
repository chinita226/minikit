import unittest
import unittest.mock
from context import app



class BasicTestSuite(unittest.TestCase):
    """Application test class."""

    @unittest.mock.patch("builtins.print", autospec=True, side_effect=print)
    def test_auth_api_back_wrong(self, mock_print):
        """Test auth_api function returns 401 status code when API key is wrong."""
        app.auth_api_back("wrong", "wrong")
        mock_print.assert_called_with("Wrong authentication: response code", 401)
    
    @unittest.mock.patch("builtins.print", autospec=True, side_effect=print)
    def test_auth_api_back_right(self, mock_print):
        """Test auth_api function returns 200 status code when API key is right."""
        app.auth_api_back("9PLVHsF#aYYI!VC5snz0tBml5lBVNZ7Z", "9PLVHsF#aYYI!VC5snz0tBml5lBVNZ7Z")
        mock_print.assert_called_with("Authentication completed.")




if __name__ == '__main__':
    unittest.main()