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

headers = {
    'User-Agent': 'SearchBot/1.0 (by Error- on e621)'
}

async def processapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink, headers=headers) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    if not datajson:
        print("Result Not Found")
        raise ResultNotFound()
    print("Shuffling data from json")
    data = shuffle(datajson)
    print("Parsing data from json")
    imagenum = 0
    while ".swf" in data[imagenum]['file_url']:
        imagenum += 1
    while ".webm" in data[imagenum]['file_url']:
        imagenum += 1
    try:
        dataimage = data[imagenum]
        fileurl = dataimage['file_url']
        imgartists = dataimage['artist']
        imgartist = ', '.join(imgartists)
        imgtag = dataimage['tags']
        imgtag = imgtag.split(" ")
        tags = [imgtag[x:x+25] for x in range(0, len(imgtag), 25)]
        imgtags = tags[0]
        imgrate = dataimage['rating']
        if imgrate == "e":
            processapi.imgrating = "Explicit"
        if imgrate == "s":
            processapi.imgrating = "Safe"
        if imgrate == "q":
            processapi.imgrating = "Mature/Questionable"
        imgsources = dataimage['source']
        imgsource = str(imgsources)
        if imgartist == "None":
            processapi.imgartist = "Unspecified"
        else:
            processapi.imgartist = imgartist
        if imgsource == "None":
            processapi.imgsource = "Unspecified"
        else:
            processapi.imgsource = imgsource
        processapi.imgtags = str(' '.join(imgtags))
        imgid = dataimage['id']
        processapi.imgid = str(imgid)
        processapi.file_link = str(fileurl).replace('None', '')
    except IndexError:
        raise ResultNotFound()

async def processshowapi(apilink):
    print("API Link: " + apilink)
    print("Requesting json from API")
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    if not data:
        print("Result Not Found")
        raise ResultNotFound()
    print("Parsing data from json")
    fileurl = data['file_url']
    imgartists = data['artist']
    imgartist = ', '.join(imgartists)
    imgtag = data['tags']
    imgtag = imgtag.split(" ")
    tags = [imgtag[x:x+25] for x in range(0, len(imgtag), 25)]
    imgtags = tags[0]
    imgrate = data['rating']
    if imgrate == "e":
        processshowapi.imgrating = "Explicit"
    if imgrate == "s":
        processshowapi.imgrating = "Safe"
    if imgrate == "q":
        processshowapi.imgrating = "Mature/Questionable"
    imgsources = data['source']
    imgsource = str(imgsources)
    if imgartist == "None":
        processshowapi.imgartist = "Unspecified"
    else:
        processshowapi.imgartist = imgartist
    if imgsource == "None":
        processshowapi.imgsource = "Unspecified"
    else:
        processshowapi.imgsource = imgsource
    processshowapi.imgtags = str(' '.join(imgtags))
    processshowapi.file_link = str(fileurl).replace('None', '')