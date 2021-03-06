"""Functions useful for temporary bans, for any chat bot."""


from datetime import datetime
import json
import os
from .errors import NoTempBansForGuild
from .ext import parse_times
from .types import TempbanEnd, TempbanState

# If this whole extension looks familiar, it is: I basically just copy-pasted mute.py
# and edited it to fit with temp-bans instead of mutes.


def get_temp_bans_file():
    """Returns any temp bans."""
    try:
        with open("data/temp_bans.json", "r", encoding="utf-8", newline="\n") as file:
            return json.load(file)
    except FileNotFoundError:
        if not os.path.exists("data/"):
            os.makedirs("data/")
        with open("data/temp_bans.json", "w+", encoding="utf-8", newline="\n") as file:
            json.dump({}, file)
            return {}


def check_bans(clear_bans=True):
    """
        Returns any temp bans that should end by now.
        Ideally run this command every minute or so, for maximum efficiency.
        """
    unban_list = []
    to_clear = []
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    unbans = get_temp_bans_file()
    if dt_string in unbans:
        # we have people to unban for now
        for to_unban in unbans.get(dt_string):
            guild_id = to_unban[1]
            user_id = to_unban[0]
            unban_list.append(TempbanEnd().from_dict({
                "guild_id": guild_id,
                "user_id": user_id
            }))
            if clear_bans:
                to_clear.append([guild_id, user_id])
        if clear_bans:
            unbans = json.load(open("data/temp_bans.json", "r", encoding="utf-8", newline="\n"))
            unbans.pop(dt_string)
            for to_remove in to_clear:
                guild = to_remove[0]
                user = to_remove[1]
                unbans[str(guild)].pop(str(user))
                if not unbans.get(str(guild)):
                    unbans.pop(str(guild))
            json.dump(unbans, open("data/temp_bans.json", "w+", encoding="utf-8", newline="\n"))
    return unban_list


def add_bans(guild_id: int, user_id: int, author_id: int, datetime_to_parse: str):
    """
    Add a temporary ban to a user.
    NOTE: datetime_to_parse should be a string like: "1 hour 30 minutes"
    """
    bans = get_temp_bans_file()
    new_ban_data = (user_id, guild_id)
    str_dt_obj = parse_times(datetime_to_parse)

    # if the script made it this far, this is real we have to store temp-ban data
    if str_dt_obj not in bans:
        bans[str_dt_obj] = []
    bans[str_dt_obj].append(new_ban_data)
    temp_ban_index = len(bans[str_dt_obj]) - 1  # how the hell does that work
    if str(guild_id) not in bans:
        bans[str(guild_id)] = {}
    if str(user_id) in bans[str(guild_id)]:
        bans[str(guild_id)].pop(str(user_id))
    if not str(user_id) in bans[str(guild_id)]:
        bans[str(guild_id)][str(user_id)] = []
    bans[str(guild_id)][str(user_id)] = [str_dt_obj, author_id, temp_ban_index]
    json.dump(bans, open("data/temp_bans.json", "w+", newline='\n', encoding='utf-8'))
    return str_dt_obj
    # Don't worry I can't read this mess either.


def get_ban_status(guild_id: int, user_id: int):
    """
    Return data of the user's temp ban.
    """
    with open("data/temp_bans.json", "r", newline='\n', encoding='utf-8') as temp_file:
        bans = json.load(temp_file)
    guild_temp_bans = bans.get(str(guild_id))
    if guild_temp_bans is None:
        raise NoTempBansForGuild(f"Guild {guild_id} does not have any current temp-bans.")
    user_bans = guild_temp_bans.get(str(user_id))
    if not user_bans:
        return None
    # user has been muted.
    ban_index = user_bans[2]
    ban_data = bans.get(user_bans[0])[ban_index]
    return TempbanState().from_dict({
        "unban_time": user_bans[0],
        "ban_author_id": user_bans[1],
        "ban_index": ban_index,
        "ban_data": ban_data
    })


def unban_user(guild_id: int, user_id: int):
    """
    Removes the temporary ban from a user.
    """
    bans = get_temp_bans_file()
    try:
        guild_bans = bans.get(str(guild_id))
    except KeyError as exception:
        raise NoTempBansForGuild(f"Guild {guild_id} does not have any current temp-bans.") from \
            exception
    user_bans = get_ban_status(guild_id, user_id)
    unban_time = user_bans["unban_time"]
    ban_index = user_bans["ban_index"]
    bans.get(unban_time).pop(ban_index)
    if not bans.get(unban_time):
        bans.pop(unban_time)
    guild_bans.pop(str(user_id))
    if not guild_bans:
        bans.pop(str(guild_id))
    else:
        for value in bans[str(guild_id)].items():
            value[2] = value[2] - 1
    json.dump(bans, open("data/temp_bans.json", "w+", newline='\n', encoding='utf-8'))
