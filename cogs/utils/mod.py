from collections import namedtuple

from cogs.utils.bit_enum import BitEnum

class Mod(BitEnum):
    """The mods in osu!
    """
    NF = 1
    EZ = 1 << 1
    no_video = 1 << 2  # not a mod anymore
    HD = 1 << 3
    HR = 1 << 4
    SD = 1 << 5
    DT = 1 << 6
    RX = 1 << 7
    HT = 1 << 8
    NC = 1 << 9  # always used with double_time
    FL = 1 << 10
    Auto = 1 << 11
    SO = 1 << 12
    AP = 1 << 13  # same as autopilot
    PF = 1 << 14
    FourKeys = 1 << 15
    FiveKeys = 1 << 16
    SixKeys = 1 << 17
    SevenKeys = 1 << 18
    EightKeys = 1 << 19
    FadeIn = 1 << 20
    Random = 1 << 21
    Cinema = 1 << 22  # same as last_mod
    TP = 1 << 23
    NineKeys = 1 << 24
    Coop = 1 << 25
    OneKey = 1 << 26
    ThreeKeys = 1 << 27
    TwoKeys = 1 << 28
    ScoreV2 = 1 << 29

    @classmethod
    def parse(cls, cs):
        """Parse a mod mask out of a list of shortened mod names.

        Parameters
        ----------
        cs : str
            The mod string.

        Returns
        -------
        mod_mask : int
            The mod mask.
        """
        if len(cs) % 2 != 0:
            raise ValueError(f'malformed mods: {cs!r}')

        cs = cs.lower()
        mapping = {
            'ez': cls.easy,
            'hr': cls.hard_rock,
            'ht': cls.half_time,
            'dt': cls.double_time,
            'hd': cls.hidden,
            'fl': cls.flashlight,
            'so': cls.spun_out,
            'nf': cls.no_fail,
        }

        mod = 0
        for n in range(0, len(cs), 2):
            try:
                mod |= mapping[cs[n:n + 2]]
            except KeyError:
                raise ValueError(f'unknown mod: {cs[n:n + 2]!r}')

        return mod