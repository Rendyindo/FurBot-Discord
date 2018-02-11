import aiohttp

class InvalidHTTPResponse(Exception):
    pass

async def get_user(token, username, mode=0):
    apilink = "https://osu.ppy.sh/api/get_user?k={}&m={}&u={}".format(token, mode, username)
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    user = datajson[0]
    get_user.id = user['user_id']
    get_user.name = user['username']
    get_user.count300 = user['count300']
    get_user.count100 = user['count100']
    get_user.count50 = user['count50']
    get_user.playcount = user['playcount']
    get_user.ranked_score = user['ranked_score']
    get_user.total_score = user['total_score']
    get_user.pp_rank = user['pp_rank']
    get_user.level = user['level']
    get_user.pp = user['pp_raw']
    get_user.accuracy = user['accuracy']
    get_user.count_rank_ss = user['count_rank_ss']
    get_user.count_rank_ssh = user['count_rank_ssh']
    get_user.count_rank_s = user['count_rank_s']
    get_user.count_rank_sh = user['count_rank_sh']
    get_user.count_rank_a = user['count_rank_a']
    get_user.country = user['country']
    get_user.pp_country_rank = user['pp_country_rank']
    get_user.events = user['events']

async def get_beatmaps(token, beatmapid=0, beatmapsetid=0, mode=0):
    if not beatmapid:
        if not beatmapsetid:
            raise NoMapID
        apilink = "https://osu.ppy.sh/api/get_beatmaps?k={}&m={}&s={}".format(token, mode, beatmapsetid)
    else:
        apilink = "https://osu.ppy.sh/api/get_beatmaps?k={}&m={}&b={}".format(token, mode, beatmapid)
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    map = datajson[0]
    get_beatmaps.diffs = len(datajson)
    get_beatmaps.set_id = map['beatmapset_id']
    get_beatmaps.statusid = map['approved']
    get_beatmaps.total_length = map['total_length']
    get_beatmaps.hit_length = map['hit_length']
    get_beatmaps.approved_date = map['approved_date']
    get_beatmaps.last_update = map['last_update']
    get_beatmaps.artist = map['artist']
    get_beatmaps.title = map['title']
    get_beatmaps.creator = map['creator']
    get_beatmaps.bpm = map['bpm']
    get_beatmaps.source = map['source']
    get_beatmaps.tags = map['tags']
    get_beatmaps.genre_id = map['genre_id'] # Will implement string output soon
    get_beatmaps.language_id = map['language_id'] # Same
    get_beatmaps.favourite_count = map['favourite_count']

    # Beatmap statuses
    if get_beatmaps.statusid == "-2":
        get_beatmaps.status = "Graveyard"
    if get_beatmaps.statusid == "-1":
        get_beatmaps.status = "WIP"
    if get_beatmaps.statusid == "0":
        get_beatmaps.status = "Pending"
    if get_beatmaps.statusid == "1":
        get_beatmaps.status = "Ranked"
    if get_beatmaps.statusid == "2":
        get_beatmaps.status = "Approved"
    if get_beatmaps.statusid == "3":
        get_beatmaps.status = "Qualified"
    if get_beatmaps.statusid == "4":
        get_beatmaps.status = "Loved"
    if get_beatmaps.statusid > 0:
        get_beatmaps.isranked == "True"
    else:
        get_beatmaps.isranked == "False"

    # Difficulty spesific info
    if get_beatmaps.diffs == 1:
        get_beatmaps.version = map['version']
        get_beatmaps.file_md5 = map['file_md5']
        get_beatmaps.diff_size = map['diff_size']
        get_beatmaps.diff_overall = map['diff_overall']
        get_beatmaps.diff_approach = map['diff_approach']
        get_beatmaps.diff_drain = map['diff_drain']
        get_beatmaps.mode = map['mode']
        get_beatmaps.playcount = map['playcount']
        get_beatmaps.passcount = map['passcount']
        get_beatmaps.max_combo = map['max_combo']
        get_beatmaps.difficultyrating = map['difficultyrating']
        get_beatmaps.id = map['beatmap_id']
    