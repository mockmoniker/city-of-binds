from typing import Set, Dict, List, Type, Union


VALID_PREFIXES: Set[str] = {"--", "++", "-", "+"}

VALID_BIND_MANAGEMENT_COMMANDS: Dict[str, List[Type]] = {
    "bind": [str, str],  # key, command
    "showbind": [str],  # key
    "showbindall": [],
    "unbind": [str],  # key
    "unbindall": [],
    "keybindreset": [],
}

VALID_BIND_LOAD_FILE_COMMANDS: Dict[str, List[Type]] = {
    "bindload": [],
    "bindloadfile": [str],  # filename
    "bindloadfilesilent": [str],  # filename
}

VALID_BIND_SAVE_FILE_COMMANDS: Dict[str, List[Type]] = {
    "bindsave": [],
    "bindsavefile": [str],  # filename
    "bindsavefilesilent": [str],  # filename
    "showbindallfile": [str],  # filename
}

VALID_POWEXEC_COMMANDS: Dict[str, List[Type]] = {
    "powexecname": [str],  # power
    "powexecauto": [str],  # power
    "powexeclocation": [str, str],  # loc, power
    "powexectoggleoff": [str],  # power
    "powexectoggleon": [str],  # power
    "powerstogglealloff": [],
    "powexecslot": [int],  # slot
    "powexecaltslot": [int],  # slot
    "powexecalt2slot": [int],  # slot
    "powexecserverslot": [int],  # slot
    "powexectray": [int, int],  # slot tray
    "powexecabort": [],
    "powexecunqueue": [],
}


VALID_CHAT_COMMANDS: Dict[str, List[Type]] = {
    "s": [str],  # message
    "say": [str],  # message
    "l": [str],  # message
    "local": [str],  # message
    "b": [str],  # message
    "broadcast": [str],
    "b": [str],  # message
    "y": [str],  # message
    "yell": [str],  # message
    "g": [str],  # message
    "team": [str],  # message
    "g": [str],  # message
    "group": [str],  # message
    "lc": [str],  # message
    "league": [str],  # message
    "leaguechat": [str],  # message
    "lc": [str],  # message
    "general": [str],  # message
    "gen": [str],  # message
    "z": [str],  # message
    "lfg": [str],  # message
    "lookingforgroup": [str],  # message
    "help": [str],  # message
    "h": [str],  # message
    "helpchat": [str],  # message
    "hc": [str],  # message
    "guide": [str],  # message
    "request": [str],  # message
    "req": [str],  # message
    "auction": [str],  # message
    "sell": [str],  # message
    "tell": [str, str],  # name, message
    "t": [str, str],  # name, message
    "p": [str, str],  # name, message
    "private": [str, str],  # name, message
    "whisper": [str, str],  # name, message
    "telllast": [str],  # message
    "tl": [str],  # message
    "tll": [str, str],  # name, message
    "ttl": [str, str],  # name, message
    "reply": [str],  # message
    "r": [str],  # message
    "autoreply": [],
    "supergroup": [str],  # message
    "sg": [str],  # message
    "coalition": [str],  # message
    "c": [str],  # message
    "f": [str],  # message
    "arena": [str],  # message
    "ac": [str],  # message
    "arenalocal": [str],  # message
}


VALID_COSTUME_CHANGE_COMMANDS: Dict[str, List[Type]] = {
    "cc": [int],  # slot
    "costumechange": [int],
    "cce": [int, str],  # slot ccemote
    "ccemote": [int, str],  # slot ccemote
}


VALID_EMOTE_COMMANDS: Dict[str, List[Type]] = {
    "e": [str],  # emote
    "em": [str],
    "emote": [str],
    "me": [],  # alias for emote
}


# ===== TARGETING COMMANDS =====
VALID_TARGETING_COMMANDS: Dict[str, List[Type]] = {
    # Basic targeting
    "target": [],
    "targetname": [str],  # name
    "assist": [],
    "assistname": [str],  # name
    "unselect": [],
    # Enemy targeting
    "targetenemynear": [],
    "targetenemyfar": [],
    "targetenemynext": [],
    "targetenemyprev": [],
    # Friend targeting
    "targetfriendnear": [],
    "targetfriendfar": [],
    "targetfriendnext": [],
    "targetfriendprev": [],
    # Custom targeting
    "targetcustomnear": [str],  # params
    "targetcustomfar": [str],  # params
    "targetcustomnext": [str],  # params
    "targetcustomprev": [str],  # params
    # Toggle targeting
    "toggleenemy": [],
    "toggleenemyprev": [],
    # Target distance
    "targetdistance": [int],  # 0-1 (boolean)
}


# ===== MOVEMENT COMMANDS =====
VALID_MOVEMENT_COMMANDS: Dict[str, List[Type]] = {
    "forward": [],
    "backward": [],
    "left": [],
    "right": [],
    "up": [],
    "down": [],
    "turnleft": [],
    "turnright": [],
    "autorun": [],
    "follow": [],
    "face": [],
    "playerturn": [],
    "speedturn": [float],  # number
}


# ===== TRAY COMMANDS =====
VALID_TRAY_COMMANDS: Dict[str, List[Type]] = {
    # Tray navigation
    "nexttray": [],
    "prevtray": [],
    "nexttrayalt": [],
    "prevtrayalt": [],
    "nexttrayalt2": [],
    "prevtrayalt2": [],
    "nexttraystray": [],
    "prevtraystray": [],
    # Tray selection
    "gototray": [int],  # number
    "gototrayalt": [int],  # number
    "gototrayalt2": [int],  # number
    "gototraystray": [int, int],  # row tray
    # Tray display
    "alttray": [int],  # 0-1
    "alt2tray": [int],  # 0-1
    "alttraysticky": [],
    "traysticky": [int, int],  # tray 0-1
    "traystickyalt2": [],
    # Tray options
    "tray": [],
    "cleartray": [],
    "shownewtray": [],
    "trayalwaysshrink": [],
    "trayanimations": [],
    "traylabels": [],
}


# ===== TEAM/LEAGUE COMMANDS =====
VALID_TEAM_LEAGUE_COMMANDS: Dict[str, List[Type]] = {
    # Team management
    "invite": [str],  # character
    "i": [str],  # alias for invite
    "kick": [str],  # character
    "k": [str],  # alias for kick
    "leaveteam": [],
    "makeleader": [str],  # character
    "ml": [str],  # alias for makeleader
    "teamselect": [int],  # number
    "teamquitinternal": [],
    # League management
    "leagueinvite": [str],  # name
    "li": [str],  # alias for league_invite
    "leaguekick": [str],  # name
    "lk": [str],  # alias for league_kick
    "leaguemakeleader": [str],  # name
    "lml": [str],  # alias for league_make_leader
    "leaveLeague": [],
    "leagueToggleTeamLock": [],
    "leagueWithdrawTeam": [],
    "teamMoveToLeague": [str],  # LeaderName
    "tmtl": [str],  # alias for teamMoveToLeague
    # Invites by global name
    "getlocalinvite": [str],  # globalname
    "getlocalleagueinvite": [str],  # globalname
}


# ===== INSPIRATION COMMANDS =====
VALID_INSPIRATION_COMMANDS: Dict[str, List[Type]] = {
    "inspexecname": [str],  # inspiration
    "inspexecslot": [int],  # 1-5
    "inspirationslot": [int],  # alias for inspexec_slot
    "inspexectray": [int, int],  # row column
    "inspexecpetname": [str, str],  # insp_name petname
    "inspexecpettarget": [str],  # insp_name
    "inspdelete": [str],  # inspiration
    "inspcombine": [str, str],  # inspName inspName
    "mergeInsp": [str, str],  # alias for insp_combine
}


# ===== PET COMMANDS =====
VALID_PET_COMMANDS: Dict[str, List[Type]] = {
    "petcom": [str],  # commands
    "petcomall": [str],  # commands
    "petcomname": [str, str],  # pet_name commands
    "petcompow": [str, str],  # power_name commands
    "petsay": [str],  # message
    "petsayall": [str],  # message
    "petsayname": [str, str],  # pet_name message
    "petsaypow": [str, str],  # power_name message
    "petselect": [int],  # integer
    "petselectname": [str],  # pet_name
    "petrename": [str],  # name
    "petrenamename": [str],  # name
    "releasepets": [],
    "clearpetnames": [],
    "showpetnames": [],
    "petoptions": [],
}


# ===== SUPERGROUP COMMANDS =====
VALID_SUPERGROUP_COMMANDS: Dict[str, List[Type]] = {
    # Basic SG management
    "sginvite": [str],  # character
    "sgi": [str],  # alias for sginvite
    "sgkick": [str],  # character
    "sgk": [str],  # alias for sgkick
    "sgkickyes": [str],  # name (no confirmation)
    "sgleave": [],
    "sgmode": [],
    "sgmodeset": [int],  # mode (0-1)
    "sgwho": [],
    "altinvite": [str],  # name
    # SG settings
    "sgsetmotd": [str],  # message
    "sgsetmotto": [str],  # motto
    "sgsetdescription": [str],  # description
    "sgsetdemotetimeout": [int],  # seconds
    "sgpasscode": [str],  # text
    # Rank naming
    "nameleader": [str],  # name
    "nameoverlord": [str],  # name
    "nameringleader": [str],  # name
    "nameenforcer": [str],  # name
    "nametaskmaster": [str],  # name
    "namecommander": [str],  # name
    "namelieutenant": [str],  # name
    "namecaptain": [str],  # name
    "namemember": [str],  # name
    "nameflunky": [str],  # name
    # Promote/demote
    "promote": [str],  # character
    "demote": [str],  # character
    # Base access
    "enterbasefrompasscode": [str],  # passcode
    "enterbasefromsgid": [int],  # SGID number
    "sgenterpasscode": [],
}


# ===== WINDOW/UI COMMANDS =====
VALID_WINDOW_UI_COMMANDS: Dict[str, List[Type]] = {
    # Window management
    "windowshow": [str],  # window_name
    "show": [str],  # alias for window_show
    "windowhide": [str],  # window_name
    "windowtoggle": [str],  # window_name
    "toggle": [str],  # alias for window_toggle
    "windowresetall": [],
    "windownames": [],
    "windowscale": [str, float],  # window scale
    "windowcolor": [],
    "windowcloseextra": [],
    "gamereturn": [],  # alias for window_close_extra
    # Custom windows
    "customwindow": [str],  # name
    "customwindowtoggle": [str],  # name
    # Chat windows
    "chat": [],
    "chatcycle": [],
    "clearchat": [],
    "copychat": [str],  # tab
    "beginchat": [str],  # string
    "startchat": [],
    "slashchat": [],
    # Specific windows
    "map": [],
    "nav": [],
    "powers": [],
    "info": [],
    "infoself": [],
    "infotab": [int],  # tab_number
    "infoselftab": [int],  # tab_number
    "menu": [],
    "helpwindow": [],
    # UI scaling
    "uiscale": [float],  # number
}


# ===== MACRO COMMANDS =====
VALID_MACRO_COMMANDS: Dict[str, List[Type]] = {
    "macro": [str, str],  # name command
    "macroimage": [str, str, str],  # icon tooltip command
    "macroslot": [int, str, str],  # macro-slot# name command
}


# ===== CAMERA COMMANDS =====
VALID_CAMERA_COMMANDS: Dict[str, List[Type]] = {
    "camdist": [float],  # distance
    "camdistadjust": [float],  # adjustment
    "camreset": [],
    "camrotate": [],
    "camturn": [],
    "mouselook": [],
    "canlook": [],  # alias for mouse_look
    "mouseinvert": [],
    "mousespeed": [float],  # scale factor
    "mousedrag": [],
    "first": [],
    "third": [],
    "lookdown": [],
    "lookup": [],
    "zoomin": [Union[str, int]],  # +, ++, or 0-1
    "zoomout": [Union[str, int]],  # +, ++, or 0-1
}


# ===== OTHER COMMANDS =====
VALID_OTHER_COMMANDS: Dict[str, List[Type]] = {
    # No operation
    "": [],
    "nop": [],
    # System information
    "loc": [],  # alias for getpos
    "getpos": [],
    "whereami": [],
    "citytime": [],
    "localtime": [],
    "servertime": [],
    "showtime": [int],  # 0-1
    "myhandle": [],
    # Status/flags
    "afk": [str],  # message
    "roleplaying": [],
    "watching": [],
    "sethelperstatus": [int],  # 1-4
    "lfgset": [int],  # number
    "lfgtoggle": [],
    # Friends/ignore
    "friend": [str],  # character
    "unfriend": [str],  # character
    "estrange": [str],  # alias for unfriend
    "friendlist": [],
    "fl": [],  # alias for friendlist
    "ignore": [str],  # character
    "unignore": [str],  # character
    "ignorelist": [],
    "ignorespammer": [str],  # character
    # Global friends
    "gfriend": [str],  # name
    "gunfriend": [str],  # name
    "gunfriendplayer": [str],  # alias for gunfriend
    "gfriends": [],
    "gignore": [str],  # username
    "gunignore": [str],  # username
    "gignoring": [],
    # Global names
    "getglobalname": [str],  # localname
    "getlocalname": [str],  # globalname
    # Hide commands
    "hide": [],
    "ghide": [],  # alias for hide
    "gunhide": [],  # alias for hide
    "unhide": [],
    "hideall": [],
    "unhideall": [],
    "hidefriends": [],
    "unhidefriends": [],
    "hidegchannels": [],
    "unhidegchannels": [],
    "hidegfriends": [],
    "unhidegfriends": [],
    "hideinvite": [],
    "unhideinvite": [],
    "hideprimarychat": [],
    "hidesearch": [],
    "unhidesearch": [],
    "hideset": [int],  # number
    "hidesg": [],
    "unhidesg": [],
    "hidetell": [],
    "unhidetell": [],
    # Search
    "search": [str],  # options
    "sea": [str],  # alias for search
    "findmember": [str],  # alias for search
    "who": [str],  # name
    "whoall": [],
    # Game exit
    "quit": [],
    "quittocharacterselect": [],
    "quittologin": [],
    "exitlaunch": [str],  # FilePath
    # Other utilities
    "stuck": [],
    "sync": [],
    "synch": [],  # alias for sync
    "release": [],
    "interact": [],
    "enterdoor": [int, int, int, int],  # coordinates map_ID
    "contextmenu": [int],  # menu_num
    "popmenu": [str],  # name
    "quickchat": [],
    "comment": [str],  # text
    "getcomment": [],  # alias for comment
    "conprint": [str],  # string
    "cmdlist": [],
}


# ===== COMPLETE COMMAND DICTIONARY =====
VALID_COMMANDS_BY_CATEGORY = {
    "bind_file": VALID_BIND_FILE_COMMANDS,
    "powexec": VALID_POWEXEC_COMMANDS,
    "chat": VALID_CHAT_COMMANDS,
    "costume_change": VALID_COSTUME_CHANGE_COMMANDS,
    "emote": VALID_EMOTE_COMMANDS,
    "targeting": VALID_TARGETING_COMMANDS,
    "movement": VALID_MOVEMENT_COMMANDS,
    "tray": VALID_TRAY_COMMANDS,
    "team_league": VALID_TEAM_LEAGUE_COMMANDS,
    "inspiration": VALID_INSPIRATION_COMMANDS,
    "pet": VALID_PET_COMMANDS,
    "supergroup": VALID_SUPERGROUP_COMMANDS,
    "window_ui": VALID_WINDOW_UI_COMMANDS,
    "macro": VALID_MACRO_COMMANDS,
    "camera": VALID_CAMERA_COMMANDS,
    "other": VALID_OTHER_COMMANDS,
}


# Flatten all commands for quick lookup
VALID_COMMANDS: Set[str] = set()
for category_commands in VALID_COMMANDS_BY_CATEGORY.values():
    VALID_COMMANDS.update(category_commands.keys())


# Legacy compatibility - keep existing structure
VALID_BIND_FILE_COMMANDS_LEGACY = VALID_BIND_FILE_COMMANDS
VALID_POWEXEC_COMMANDS_LEGACY = VALID_POWEXEC_COMMANDS
VALID_CHAT_COMMANDS_LEGACY = VALID_CHAT_COMMANDS
VALID_COSTUME_CHANGE_COMMANDS_LEGACY = VALID_COSTUME_CHANGE_COMMANDS
VALID_EMOTE_COMMANDS_LEGACY = VALID_EMOTE_COMMANDS
VALID_OTHER_COMMANDS_LEGACY = VALID_OTHER_COMMANDS
