import re
from typing import NamedTuple

__all__ = ["version", "version_info"]


version = "3.0.0b2"

_re_version = re.compile(r"(\d+)\.(\d+)\.(\d+)(\D*)(\d*)")


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int

    @classmethod
    def from_str(cls, v: str) -> "VersionInfo":
        groups = _re_version.match(v).groups()  # type: ignore
        major, minor, micro = map(int, groups[:3])
        level = (groups[3] or "")[:1]
        if level == "a":
            level = "alpha"
        elif level == "b":
            level = "beta"
        elif level in ("c", "r"):
            level = "candidate"
        else:
            level = "final"
        serial = groups[4]
        serial = int(serial) if serial else 0
        return cls(major, minor, micro, level, serial)

    def __str__(self) -> str:
        v = f"{self.major}.{self.minor}.{self.micro}"
        level = self.releaselevel
        if level and level != "final":
            v = f"{v}{level[:1]}{self.serial}"
        return v


version_info = VersionInfo.from_str(version)
