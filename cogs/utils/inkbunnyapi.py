import urllib, json, random, aiohttp

def shuffle(arr):
    random.shuffle(arr)
    return arr

class LoginError(Exception): 
	""" Could not login to IB """
	pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class Inkbunny(object):
    def __init__(self, username, password):
        loginUrl = 'https://inkbunny.net/api_login.php?username=%s&password=%s' \
            % (username, password)
        http = urllib.request.urlopen(loginUrl)
        result = json.loads(http.read())
        
        if ('error_code' in result):
            raise LoginError("Error! Error code %s: %s" % (result['error_code'], result['error_message']))
        self.sid = result['sid']

    async def search(self, args):
        apilink = "https://inkbunny.net/api_search.php?&sid={}&text={}&random=yes&type=1,2,3,4,14".format(self.sid, args)
        async with aiohttp.ClientSession() as session:
            async with session.get(apilink) as r:
                if r.status == 200:
                    datajson = await r.json()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        if not datajson['submissions']:
            print("Result Not Found")
            raise ResultNotFound()
        return InkSubmission(datajson['submissions'][0])
        
class InkSubmission(object):
    def __init__(self, submission):
        self.submission = submission

    @property
    def last_update(self):
        return self.submission['last_file_update_datetime_usertime']
        
    @property
    def submission_title(self):
        return self.submission['title']
        
    @property
    def rating(self):
        return self.submission['rating_name']
        
    @property
    def file_url(self):
        return self.submission['file_url_full']