from bs4 import BeautifulSoup
import aiohttp, random, os
from random import randint
try:
    import config
    fa_a = config.fa_a
    fa_b = config.fa_b
    fa_cfuid = config.fa_cfuid
except:
    pass

try:
    fa_a = os.environ['A_FA']
    fa_b = os.environ['B_FA']
    fa_cfuid = os.environ['CFUID_FA']
except KeyError:
    pass

cookie = { 'b' : fa_b, 'a' : fa_a, '__cfuid' : fa_cfuid}

def shuffle(arr):
    random.shuffle(arr)
    return arr

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

class FurAffinity():
    async def show(self, link):
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(link) as r:
                if r.status == 200:
                    data = await r.text()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        return FASubmission(data)
    
    async def search(self, queries):
        link = "https://www.furaffinity.net/search/?q={}".format(queries)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(link) as r:
                if r.status == 200:
                    data = await r.text()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        s = BeautifulSoup(data, 'html.parser')
        post = randint(0, 47)
        shuffled = s.find(attrs={'id' : 'gallery-search-results'}).findAll("figure")[post].findAll("a")[0]['href']
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get("https://www.furaffinity.net/{}".format(shuffled)) as r:
                if r.status == 200:
                    result = await r.text()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        return FASubmission(result)   

class FASubmission(object):
    def __init__(self, data):
        self.data = data
        self.s = BeautifulSoup(self.data, 'html.parser')
    
    @property
    def imglink(self):
        return self.s.find(attrs={'class' : 'alt1 actions aligncenter'}).findAll('b')[1].a.get('href')
    
    @property
    def title(self):
        return self.s.find(attrs={'class' : 'cat'}).string.strip()

    @property
    def artist(self):
        return self.s.findAll(attrs={'class' : 'cat'})[1].find('a').string
    
    @property
    def keywords(self):
        keywords = []
        try:
            for kw in self.s.find(attrs={'id' : 'keywords'}).findAll('a'):
                keywords.append(kw.string)
        except:
            keywords.append("Unspecified")
        return keywords