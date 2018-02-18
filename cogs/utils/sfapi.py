import random, os, asyncio, aiohttp

class ResultNotFound(Exception):
    """Used if ResultNotFound is triggered by e* API."""
    pass

class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
    pass

def shuffle(arr):
    random.shuffle(arr)
    return arr

async def search(queries, maxlevel):
    apilink = "https://api2.sofurry.com/browse/search?search=" + queries + "&format=json&filter=artwork&maxlevel=" + maxlevel
    print("Requesting json from API")
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    if not datajson:
        print("Result Not Found")
        raise ResultNotFound()
    itemlist = datajson['data']['entries']
    print("Shuffling data from json")
    datashuffle = shuffle(itemlist)
    data = datashuffle[0]
    search.postid = data['id']
    search.title = data['title']
    search.artistID = data['artistID']
    search.artistName = data['artistName']
    search.date = data['date']
    search.tags = data['tags']
    search.contentType = data['contentType']
    search.contentLevel = data['contentLevel']
    search.thumbnail = data['thumbnail'].replace('\/', '/')
    search.preview = data['preview'].replace('\/', '/')
    search.full = data['full'].replace('\/', '/')
    if search.contentLevel == 0:
        search.contentRating = "Safe"
    if search.contentLevel == 1:
        search.contentRating = "Adult"
    if search.contentLevel == 2:
        search.contentRating = "Extreme"