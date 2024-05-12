from dataclasses import dataclass

from division2calc.build.common import Profile
from division2calc.build.stats import Stats
from division2calc.gear import Gears
from division2calc.weapon import Weapon

from division2calc.build.damage.X import X
from division2calc.build.damage.Dydx import Dydx


@dataclass
class Damage:
    _weapon: Weapon
    _gears: Gears
    _stats: Stats

    def __post_init__(self) -> None:
        self.x = X(self._weapon, self._gears, self._stats)
        self.dydx = Dydx(self.x)

    @property
    def basic(self) -> float:
        # base
        dmg = self._weapon.base_damage
        # basic weapon damage
        dmg *= self.x.x1.basic
        # result
        return dmg

    @property
    def min(self) -> float:
        dmg = self.basic
        dmg *= self.x.x2.min
        dmg *= self.x.x3.min
        dmg *= self.x.x4.min
        dmg *= self.x.x5.min
        dmg *= self.x.x6.min
        dmg *= self.x.x7.min
        dmg *= self.x.x8.min
        # result
        return dmg

    @property
    def average(self) -> float:
        dmg = self.basic
        dmg *= self.x.x2.average
        dmg *= self.x.x3.average
        dmg *= self.x.x4.average
        dmg *= self.x.x5.average
        dmg *= self.x.x6.average
        dmg *= self.x.x7.average
        dmg *= self.x.x8.average
        # result
        return dmg

    @property
    def max(self) -> float:
        dmg = self.basic
        dmg *= self.x.x2.max
        dmg *= self.x.x3.max
        dmg *= self.x.x4.max
        dmg *= self.x.x5.max
        dmg *= self.x.x6.max
        dmg *= self.x.x7.max
        dmg *= self.x.x8.max
        # result
        return dmg

    def total_damage(self,
                     profile: Profile,
                     *,
                     critical: bool = False,
                     headshot: bool = False,
                     expcrit: bool = False,
                     armor: bool = False):
        # base
        dmg = self.basic
        if profile == 'basic':
            return dmg
        dmg *= getattr(self.x.x2, profile)
        dmg *= getattr(self.x.x3, profile)
        dmg *= getattr(self.x.x4, profile)
        dmg *= getattr(self.x.x5, profile)
        dmg *= self.x.x6(critical, headshot, expcrit)
        dmg *= self.x.x7(armor)
        dmg *= getattr(self.x.x8, profile)
        # result
        return dmg
