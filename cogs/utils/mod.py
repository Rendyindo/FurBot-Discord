from collections import namedtuple

from cogs.utils.bit_enum import BitEnum

class Mod(BitEnum):
    """The mods in osu!
    """
    no_fail = 1
    easy = 1 << 1
    no_video = 1 << 2  # not a mod anymore
    hidden = 1 << 3
    hard_rock = 1 << 4
    sudden_death = 1 << 5
    double_time = 1 << 6
    relax = 1 << 7
    half_time = 1 << 8
    nightcore = 1 << 9  # always used with double_time
    flashlight = 1 << 10
    autoplay = 1 << 11
    spun_out = 1 << 12
    relax2 = 1 << 13  # same as autopilot
    auto_pilot = 1 << 13  # same as relax2
    perfect = 1 << 14
    key4 = 1 << 15
    key5 = 1 << 16
    key6 = 1 << 17
    key7 = 1 << 18
    key8 = 1 << 19
    fade_in = 1 << 20
    random = 1 << 21
    last_mod = 1 << 22  # same as cinema
    cinema = 1 << 22  # same as last_mod
    target_practice = 1 << 23
    key9 = 1 << 24
    coop = 1 << 25
    key1 = 1 << 26
    key3 = 1 << 27
    key2 = 1 << 28
    scoreV2 = 1 << 29

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