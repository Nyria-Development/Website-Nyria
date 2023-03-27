import json
from database.query import Query

query = Query(
    pool_name="level_setting",
    pool_size=3
)
__level_settings = {}


def get_leveling_server(server_id: int):
    if server_id not in __level_settings:
        return False
    return __level_settings[server_id]


def load_leveling_servers() -> print:
    data = query.execute(
        query="SELECT * FROM leveling",
        data=[]
    )

    if not data:
        return print("No leveling Server to load")

    for guilds in data:
        __level_settings[guilds[0]] = guilds[1]

    return print("leveling Server loaded")
