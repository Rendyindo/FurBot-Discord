import aiohttp
from cogs.utils.mod import Mod

class InvalidHTTPResponse(Exception):
    pass

class NoMapID(Exception):
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
    get_user.count300 = int(user['count300'])
    get_user.count100 = int(user['count100'])
    get_user.count50 = int(user['count50'])
    get_user.playcount = int(user['playcount'])
    get_user.ranked_score = int(user['ranked_score'])
    get_user.total_score = int(user['total_score'])
    get_user.pp_rank = int(user['pp_rank'])
    get_user.level = float(user['level'])
    get_user.pp = float(user['pp_raw'])
    get_user.accuracy = float(user['accuracy'])
    get_user.count_rank_ss = int(user['count_rank_ss'])
    get_user.count_rank_ssh = int(user['count_rank_ssh'])
    get_user.count_rank_s = int(user['count_rank_s'])
    get_user.count_rank_sh = int(user['count_rank_sh'])
    get_user.count_rank_a = int(user['count_rank_a'])
    get_user.country = user['country']
    get_user.pp_country_rank = int(user['pp_country_rank'])
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
    get_beatmaps.set_id = int(map['beatmapset_id'])
    get_beatmaps.statusid = int(map['approved'])
    get_beatmaps.total_length = map['total_length']
    get_beatmaps.hit_length = map['hit_length']
    get_beatmaps.approved_date = map['approved_date']
    get_beatmaps.last_update = map['last_update']
    get_beatmaps.artist = map['artist']
    get_beatmaps.title = map['title']
    get_beatmaps.creator = map['creator']
    get_beatmaps.bpm = int(map['bpm'])
    get_beatmaps.source = map['source']
    get_beatmaps.tags = map['tags']
    get_beatmaps.genre_id = int(map['genre_id']) # Will implement string output soon
    get_beatmaps.language_id = int(map['language_id']) # Same
    get_beatmaps.favourite_count = int(map['favourite_count'])

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
        get_beatmaps.isranked = "True"
    else:
        get_beatmaps.isranked = "False"

    # Difficulty spesific info
    if get_beatmaps.diffs == 1:
        get_beatmaps.version = map['version']
        get_beatmaps.file_md5 = map['file_md5']
        get_beatmaps.diff_size = float(map['diff_size'])
        get_beatmaps.diff_overall = float(map['diff_overall'])
        get_beatmaps.diff_approach = float(map['diff_approach'])
        get_beatmaps.diff_drain = map['diff_drain']
        get_beatmaps.mode = map['mode']
        get_beatmaps.playcount = int(map['playcount'])
        get_beatmaps.passcount = int(map['passcount'])
        get_beatmaps.max_combo = int(map['max_combo'])
        get_beatmaps.difficultyrating = float(map['difficultyrating'])
        get_beatmaps.id = int(map['beatmap_id'])

def parse_mods(int):
    ModList = Mod.unpack(int)
    EnabledModsDict = {key: value for key, value in ModList.items() 
                 if value is not False}
    EnabledModsKeys = EnabledModsDict.keys()
    parse_mods.EnabledMods = []
    for mod in EnabledModsKeys:
        parse_mods.EnabledMods.append(mod)

def calculate_acc(count300, count100, count50, countgeki, countkatu, countmiss, mode=0):
    if mode == 0:
        hitvalue = 50 * count50 + 100 * count100 + 300 * count300
        allvalue = 300 * (countmiss + count50 + count100 + count300)
    if mode == 2:
        hitvalue = count50 + count100 + count300
        allvalue = hitvalue + countmiss + countkatu
    if mode == 1:
        hitvalue = 0.5 * count100 + count300
        allvalue = countmiss + count100 + count300
    if mode == 3:
        hitvalue = 50 * count50 + 100 * count100 + 200 * countkatu + 300 * (count300 + countgeki)
        allvalue = 300 * (countmiss + count50 + count100 + count300 + countgeki + countkatu)
    return round((hitvalue / allvalue) * 100, 2)

async def get_user_recent(token, username, mode=0):
    apilink = "https://osu.ppy.sh/api/get_user_recent?k={}&u={}&m={}".format(token, username, mode)
    async with aiohttp.ClientSession() as session:
        async with session.get(apilink) as r:
            if r.status == 200:
                datajson = await r.json()
            else:
                print("Invalid HTTP Response:" + str(r.status))
                raise InvalidHTTPResponse()
    play = datajson[0]
    get_user_recent.beatmap_id = int(play['beatmap_id'])
    get_user_recent.score = int(play['score'])
    get_user_recent.maxcombo = int(play['maxcombo'])
    get_user_recent.count50 = int(play['count50'])
    get_user_recent.count100 = int(play['count100'])
    get_user_recent.count300 = int(play['count300'])
    get_user_recent.countmiss = int(play['countmiss'])
    get_user_recent.countkatu = int(play['countkatu'])
    get_user_recent.countgeki = int(play['countgeki'])
    get_user_recent.perfect = int(play['perfect'])
    get_user_recent.enabled_mods_bitmask = int(play['enabled_mods'])
    get_user_recent.user_id = int(play['user_id'])
    get_user_recent.date = play['date']
    get_user_recent.rank = play['rank']
    if get_user_recent.perfect == 0:
        get_user_recent.FC = False
    if get_user_recent.perfect == 1:
        get_user_recent.FC = True
    parse_mods(get_user_recent.enabled_mods_bitmask)
    get_user_recent.enabled_mods = parse_mods.EnabledMods
    gamemode = mode
    get_user_recent.accuracy = calculate_acc(get_user_recent.count300, get_user_recent.count100, get_user_recent.count50, get_user_recent.countgeki, get_user_recent.countkatu, get_user_recent.countmiss, mode=mode)