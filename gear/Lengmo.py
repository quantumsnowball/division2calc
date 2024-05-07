from dataclasses import dataclass, field

import gear.attrs as attrs
from gear import Gear


@dataclass(kw_only=True)
class Lengmo(Gear):
    name: str = 'Lengmo'
    core: attrs.CoreAttribute = field(default_factory=attrs.BlueCore)
    attr1: attrs.MinorAttribute = field(default_factory=attrs.ExplosiveResistence)
    attr2: attrs.MinorAttribute = field(default_factory=attrs.CriticalHitChance)
