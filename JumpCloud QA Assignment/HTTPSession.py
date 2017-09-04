import requests

class HTTPSession(object):
    """
    Class that holds the requests session for all api calls.
    """

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.rs = requests.Session()
        self.baseurl = 'http://radiant-gorge-83016.herokuapp.com'

    def print_res_info(self, res):
        """
        Function to print useful info when something goes wrong.

        Prints:
            -URL that was hit.
            -Response body.
            -HTTP response code.

        Args:
            res (obj): Response object from a request.

        Returns:
        """
        print('INFO: USED URL: {url}'.format(url=res.url))
        print('INFO: RESPONSE BODY: {res_body}'.format(res_body=res.text))
        print('INFO: RESPONSE STATUS: {status_code}'.format(status_code=res.status_code))
