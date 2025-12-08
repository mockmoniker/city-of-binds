import re
from typing import Set
from ....configs.constants import GameConstants


class _Command:
    VALID_COMMANDS: Set[str] = set(
        [
            "",
            "ac",
            "afk",
            "ah",
            "ai",
            "alt2tray",
            "altinvite",
            "alttray",
            "alttraysticky",
            "anglesnap",
            "anglesnapcycle",
            "antialiasing",
            "architect",
            "architectclaimtickets",
            "architectcompletemission",
            "architectexit",
            "architectfixerrors",
            "architectinvincible",
            "architectinvisible",
            "architectkilltarget",
            "architectloginupdate",
            "architectnextcritter",
            "architectnextobjective",
            "architectrepublish",
            "architectsaveandexit",
            "architectsaveandtest",
            "architectsavecompressedcostumes",
            "arena",
            "arenainvite",
            "arenalist",
            "arenalocal",
            "arenascore",
            "assist",
            "assistname",
            "attachcycle",
            "aucloginupdate",
            "auction",
            "auctionhouse",
            "autoreply",
            "autorun",
            "b",
            "backward",
            "badgegrant",
            "basedefaultsky",
            "baselightingtype",
            "baseredo",
            "baseselect",
            "baseundo",
            "beginchat",
            "bind",
            "bindload",
            "bindloadfile",
            "bindloadfilesilent",
            "bindsave",
            "bindsavefile",
            "bindsavefilesilent",
            "blackmarket",
            "bloomscale",
            "bloomweight",
            "boostconvert",
            "broadcast",
            "buildsave",
            "buildsavefile",
            "c",
            "camdist",
            "camdistadjust",
            "camreset",
            "camrotate",
            "camturn",
            "canlook",
            "cc",
            "cce",
            "ccemote",
            "center",
            "centersel",
            "chancreate",
            "chandesc",
            "changehandle",
            "chaninvite",
            "chaninvitedeny",
            "chaninvitegf",
            "chaninvitesg",
            "chaninviteteam",
            "chanjoin",
            "chanleave",
            "chanmembers",
            "chanmode",
            "chanmotd",
            "chansend",
            "chantimeout",
            "chanusermode",
            "chat",
            "chatcycle",
            "chatload",
            "chatloadfile",
            "chatoptions",
            "chatsave",
            "chatsavefile",
            "chatset",
            "ci",
            "citytime",
            "clearAttributeView",
            "clearchat",
            "clearpetnames",
            "clearRewardChoice",
            "cleartray",
            "clicktomove",
            "cmdlist",
            "coalition",
            "coalitioncancel",
            "coalitioninvite",
            "coalitionmintalkrank",
            "coalitionnosend",
            "coalitionsgmintalkrank",
            "comment",
            "compatiblecursors",
            "conprint",
            "contactfinderselectcurrent",
            "contactfindershowcurrent",
            "contactfindershownext",
            "contactfindershowprevious",
            "contactfinderteleporttocurrent",
            "contextmenu",
            "controllermodifiers",
            "controllervmouse",
            "cooldownindicator",
            "copychat",
            "costumechange",
            "ctm",
            "ctminvert",
            "ctmtoggle",
            "cursorcache",
            "customwindow",
            "customwindowtoggle",
            "debugdisableautodismiss",
            "demodump",
            "demodumptga",
            "demofps",
            "demoframestats",
            "demohideallentityui",
            "demohidechat",
            "demohidedamage",
            "demohidenames",
            "demoloop",
            "demopause",
            "demorecord",
            "demorecordauto",
            "demospeedscale",
            "demostop",
            "demote",
            "dialoganswer",
            "dialogno",
            "dialogyes",
            "disable2d",
            "dofweight",
            "down",
            "e",
            "editbase",
            "em",
            "emailheaders",
            "emote",
            "enablevbos",
            "enterbasefrompasscode",
            "enterbasefromsgid",
            "enterdoor",
            "estrange",
            "exitlaunch",
            "extramodifiers",
            "f",
            "face",
            "findmember",
            "first",
            "fl",
            "follow",
            "forward",
            "forwardmouse",
            "friend",
            "friendlist",
            "fsaa",
            "fullRelight",
            "fullscreen",
            "g",
            "gamereturn",
            "gen",
            "general",
            "getallarenastats",
            "getarenastats",
            "getcomment",
            "getglobalname",
            "getlocalinvite",
            "getlocalleagueinvite",
            "getlocalname",
            "getpos",
            "getratedarenastats",
            "gfriend",
            "gfriends",
            "ghide",
            "gignore",
            "gignoring",
            "ginvite",
            "ginvitesg",
            "gmotd",
            "gototray",
            "gototrayalt",
            "gototrayalt2",
            "gototraystray",
            "graphfps",
            "gridsnap",
            "gridsnapcycle",
            "group",
            "guide",
            "gunfriend",
            "gunfriendplayer",
            "gunhide",
            "gunignore",
            "h",
            "hardconsts",
            "hc",
            "help",
            "helpchat",
            "helpwindow",
            "hide",
            "hideall",
            "hidefriends",
            "hidegchannels",
            "hidegfriends",
            "hideinvite",
            "hideprimarychat",
            "hidesearch",
            "hideset",
            "hidesg",
            "hidetell",
            "i",
            "ignore",
            "ignorelist",
            "ignorespammer",
            "imageServer",
            "incarnateequip",
            "incarnateunequip",
            "incarnateunequipall",
            "incarnateunequipbyslot",
            "info",
            "infoself",
            "infoselftab",
            "infotab",
            "inspcombine",
            "inspdelete",
            "inspexecname",
            "inspexecpetname",
            "inspexecpettarget",
            "inspexecslot",
            "inspexectray",
            "inspirationslot",
            "interact",
            "invite",
            "k",
            "keybindreset",
            "kick",
            "kiosk",
            "l",
            "lc",
            "league",
            "leaguechat",
            "leagueinvite",
            "leaguekick",
            "leaguemakeleader",
            "leagueToggleTeamLock",
            "leagueWithdrawTeam",
            "leaveLeague",
            "leaveteam",
            "left",
            "lfg",
            "lfgeventresponse",
            "lfgremovefromqueue",
            "lfgrequesteventlist",
            "lfgset",
            "lfgtoggle",
            "li",
            "linkchannel",
            "linkinfo",
            "linkinteract",
            "linkinteractglobal",
            "listenrange",
            "lk",
            "lml",
            "loc",
            "local",
            "localtime",
            "lodbias",
            "logchat",
            "lookdown",
            "lookingforgroup",
            "lookup",
            "loudstacking",
            "ma",
            "macro",
            "macroimage",
            "macroslot",
            "mailview",
            "makeleader",
            "manage",
            "map",
            "maxAniso",
            "maxColorTrackerVerts",
            "maxfps",
            "maximize",
            "maxInactiveFps",
            "maxrtframes",
            "maxtexunits",
            "me",
            "menu",
            "mergeInsp",
            "missionarchitect",
            "missionmake",
            "missionsearch",
            "ml",
            "mmentry",
            "mmscrollsettoggleregion",
            "mmscrollsetviewlist",
            "monitorattribute",
            "mousedrag",
            "mouseinvert",
            "mouselook",
            "mousespeed",
            "myhandle",
            "mypurchases",
            "namecaptain",
            "namecommander",
            "nameenforcer",
            "nameflunky",
            "nameleader",
            "namelieutenant",
            "namemember",
            "nameoverlord",
            "nameringleader",
            "namescale",
            "nametaskmaster",
            "nav",
            "neterrorcorrection",
            "netgraph",
            "nexttray",
            "nexttrayalt",
            "nexttrayalt2",
            "nexttraystray",
            "noBump",
            "nojpg",
            "nojumprepeat",
            "nop",
            "noparticles",
            "nosunflare",
            "notga",
            "optionlist",
            "optionload",
            "optionloadfile",
            "optionsave",
            "optionsavefile",
            "optionset",
            "optiontoggle",
            "p",
            "petcom",
            "petcomall",
            "petcomname",
            "petcompow",
            "petition",
            "petoptions",
            "petrename",
            "petrenamename",
            "petsay",
            "petsayall",
            "petsayname",
            "petsaypow",
            "petselect",
            "petselectname",
            "playernote",
            "playernotelocal",
            "playerturn",
            "popmenu",
            "powers",
            "powerstogglealloff",
            "powexecabort",
            "powexecalt2slot",
            "powexecaltslot",
            "powexecauto",
            "powexeclocation",
            "powexecname",
            "powexecserverslot",
            "powexecslot",
            "powexectoggleoff",
            "powexectoggleon",
            "powexectray",
            "powexecunqueue",
            "prevshaders",
            "prevtray",
            "prevtrayalt",
            "prevtrayalt2",
            "prevtraystray",
            "private",
            "profilerrecord",
            "profilerstop",
            "profilingmemory",
            "promote",
            "quickchat",
            "quit",
            "quittocharacterselect",
            "quittologin",
            "r",
            "rechargeindicator",
            "rechargetimercolor",
            "rechargetimerformat",
            "rechargetimeropacity",
            "rechargetimerthreshold",
            "reducemip",
            "release",
            "releasepets",
            "reloadgfx",
            "renderscale",
            "renderscalex",
            "renderscaley",
            "rendersize",
            "reply",
            "req",
            "request",
            "requestexitmission",
            "respec",
            "respecstatus",
            "right",
            "roleplaying",
            "roll",
            "roomclip",
            "roomclipcycle",
            "rotate",
            "s",
            "salvageopen",
            "say",
            "screen",
            "screenshot",
            "screenshottga",
            "screenshottitle",
            "screenshotui",
            "sea",
            "search",
            "seeeverything",
            "selectbuild",
            "selectlast",
            "selectnext",
            "sell",
            "send",
            "servertime",
            "setdifficultyav",
            "setdifficultyboss",
            "setdifficultylevel",
            "setdifficultyteamsize",
            "sethelperstatus",
            "setpowerinfoclass",
            "settitle",
            "settitleid",
            "sg",
            "sgenterpasscode",
            "sgi",
            "sginvite",
            "sgk",
            "sgkick",
            "sgkickyes",
            "sgleave",
            "sgmode",
            "sgmodeset",
            "sgmusic",
            "sgpasscode",
            "sgsetdemotetimeout",
            "sgsetdescription",
            "sgsetmotd",
            "sgsetmotto",
            "sgwho",
            "shaderCache",
            "sheathe",
            "show",
            "showbind",
            "showbindall",
            "showbindallfile",
            "showfps",
            "shownewtray",
            "showpetnames",
            "showtime",
            "slashchat",
            "speakrange",
            "speedturn",
            "startchat",
            "stopinactivedisplay",
            "stopmonitorattribute",
            "stuck",
            "supergroup",
            "supporthardwarelights",
            "suppressCloseFx",
            "suppressCloseFxDist",
            "sync",
            "synch",
            "t",
            "tabclose",
            "tabcreate",
            "tabglobalnext",
            "tabglobalprev",
            "tabnext",
            "tabprev",
            "tabselect",
            "tabtoggle",
            "tailorstatus",
            "target",
            "targetcustomfar",
            "targetcustomnear",
            "targetcustomnext",
            "targetcustomprev",
            "targetdistance",
            "targetenemyfar",
            "targetenemynear",
            "targetenemynext",
            "targetenemyprev",
            "targetfriendfar",
            "targetfriendnear",
            "targetfriendnext",
            "targetfriendprev",
            "targetname",
            "team",
            "teamMoveToLeague",
            "teamquitinternal",
            "teamselect",
            "tell",
            "telllast",
            "texaniso",
            "texLodBias",
            "third",
            "thumbtack",
            "titlechange",
            "tl",
            "tll",
            "tmtl",
            "toggle",
            "toggleenemy",
            "toggleenemyprev",
            "trade",
            "tradeaccept",
            "tray",
            "trayalwaysshrink",
            "trayanimations",
            "traylabels",
            "traysticky",
            "traystickyalt2",
            "ttl",
            "turnleft",
            "turnright",
            "tutvotekick",
            "tutvotekickopinion",
            "uiscale",
            "unbind",
            "unbindall",
            "unfriend",
            "unhide",
            "unhideall",
            "unhidefriends",
            "unhidegchannels",
            "unhidegfriends",
            "unhideinvite",
            "unhidesearch",
            "unhidesg",
            "unhidetell",
            "unignore",
            "unlevelingpact",
            "unloadgfx",
            "unselect",
            "up",
            "usecelshader",
            "useCubemap",
            "usedof",
            "usefp",
            "usehdr",
            "useHQ",
            "userenderscale",
            "usewater",
            "visscale",
            "watching",
            "wdwload",
            "wdwloadfile",
            "wdwsave",
            "wdwsavefile",
            "wentworths",
            "whereami",
            "whisper",
            "who",
            "whoall",
            "windowcloseextra",
            "windowcolor",
            "windowhide",
            "windownames",
            "windowresetall",
            "windowscale",
            "windowshow",
            "windowtoggle",
            "y",
            "yell",
            "z",
            "zoomin",
            "zoomout",
        ]
    )
    VALID_PREFIXES: Set[str] = set(["--", "++", "-", "+"])

    ### Initialization
    def __init__(self, command: str):
        """Initialize the command with a string."""
        self._prefix = None
        self._slash_command = None
        self._args = None

        command = self._normalize_command_string(command)
        prefix, slash_command, args = self._get_command_parts(command)
        self.prefix = prefix
        self.slash_command = slash_command
        self.args = args

    # region Command Properties
    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, prefix: str):
        self._prefix = self._normalize_and_validate_prefix(prefix)

    @property
    def slash_command(self) -> str:
        return self._slash_command

    @slash_command.setter
    def slash_command(self, slash_command: str):
        self._slash_command = self._normalize_and_validate_slash_command(slash_command)

    @property
    def args(self) -> str:
        return self._args

    @args.setter
    def args(self, args: str):
        self._args = self._normalize_and_validate_args(args)

    # endregion

    # region Helper Functions
    def _get_command_parts(self, command_string: str) -> tuple[str, str, str]:
        """Helper function to extract the command parts from the command string."""
        prefix = self._get_prefix_from_command_string(command_string)
        slash_command = self._get_slash_command_from_command_string(command_string)
        args = self._get_args_from_command_string(command_string)
        return prefix, slash_command, args

    def _get_prefix_from_command_string(self, command_string: str) -> str:
        """Helper function to extract the prefix from the command string."""
        for prefix in sorted(self.VALID_PREFIXES, key=len, reverse=True):
            if command_string.startswith(prefix):
                return prefix
        return ""

    def _get_slash_command_from_command_string(self, command_string: str) -> str:
        """Helper function to extract the command from the command string."""
        slash_command = command_string.split(" ")[0]
        slash_command = self._remove_prefixes(slash_command)
        return slash_command

    def _remove_prefixes(self, slash_command: str) -> str:
        for prefix in sorted(self.VALID_PREFIXES, key=len, reverse=True):
            if slash_command.startswith(prefix):
                return slash_command[len(prefix) :]
        return slash_command

    def _get_args_from_command_string(self, command_string: str) -> str:
        slash_command, space, args = command_string.partition(" ")
        return args if space else ""

    def _normalize_and_validate_prefix(self, prefix: str) -> str:
        prefix = self._normalize_prefix(prefix)
        self._throw_error_if_invalid_prefix(prefix)
        return prefix

    def _normalize_and_validate_slash_command(self, slash_command: str) -> str:
        slash_command = self._normalize_slash_command(slash_command)
        self._throw_error_if_unknown_slash_command(slash_command)
        return slash_command

    def _normalize_and_validate_args(self, args: str) -> str:
        return self._normalize_args(args)

    def _normalize_command_string(self, command_string: str) -> str:
        return command_string.lstrip()

    def _normalize_prefix(self, prefix: str) -> str:
        return prefix.strip()

    def _normalize_slash_command(self, slash_command: str) -> str:
        slash_command = slash_command.strip()
        slash_command = slash_command.replace("_", "")
        slash_command = slash_command.lower()
        return slash_command

    def _normalize_args(self, args: str) -> str:
        return args.lstrip()

    def _build_command_string(self) -> str:
        if self.args:
            return f"{self.prefix}{self.slash_command} {self.args}"
        else:
            return f"{self.prefix}{self.slash_command}"

    # endregion

    # region Error Checking Methods
    def _throw_error_if_invalid_prefix(self, prefix: str):
        """Helper function to validate the prefix portion of the command string."""
        if prefix and prefix not in self.VALID_PREFIXES:
            raise ValueError(
                f"Invalid prefix '{prefix}'. Valid prefixes are: {', '.join(self.VALID_PREFIXES)}"
            )

    def _throw_error_if_unknown_slash_command(self, slash_command: str):
        """Helper function to validate the command portion of the command string."""
        if slash_command not in self.VALID_COMMANDS:
            raise ValueError(
                f"Unknown slash command '{slash_command}'. Please see https://homecoming.wiki/wiki/List_of_Slash_Commands for a list of valid commands."
            )

    # endregion

    # region Dunder Methods
    def __repr__(self):
        if self.args:
            return f"{self.__class__.__name__}(command='{self.slash_command}', args='{self.args}')"
        else:
            return f"{self.__class__.__name__}(command='{self.slash_command}')"

    def __str__(self):
        return self._build_command_string()

    def __eq__(self, other):
        if not isinstance(other, _Command):
            return False
        return str(self) == str(other)

    # endregion
