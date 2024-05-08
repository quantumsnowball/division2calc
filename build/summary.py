from dataclasses import dataclass

from build.damage import Damage
from build.stats import Stats

import pandas as pd


@dataclass
class Summary:
    _stats: Stats
    _damage: Damage

    def stats(self) -> pd.DataFrame:
        # data
        data = {
            'WeaponDamage': f'{self._damage.total_damage(basic=True):,.0f}',
            'CriticalHitChance': f'{self._stats.critical_hit_chance_pct:.1%}',
            'CriticalHitDamage': f'{self._stats.critical_hit_damage_pct:.1%}',
            'HeadshotDamage': f'{self._stats.headshot_damage_pct:.1%}',
            'ArmorDamage': f'{self._stats.damage_to_armor_pct:.1%}',
            'HealthDamage': f'{self._stats.damage_to_health_pct:.1%}',
        }
        df = pd.DataFrame(data, index=['%'])

        # result
        return df

    def damage(self) -> pd.DataFrame:
        # columns
        x6_columns = {'Normal': (False, False), 'Critical': (True, False),
                      'Headshot': (False, True), 'CritHead': (True, True)}
        x7_columns = {'Health': False, 'Armor': True}
        columns = pd.MultiIndex.from_product([x7_columns.keys(), x6_columns.keys()])
        # index
        scenario_index = {'Basic': False}
        talent_index = {'Base': False}
        index = pd.MultiIndex.from_product([scenario_index.keys(), talent_index.keys()])
        # data
        data = [[self._damage.total_damage(critical=crit, headshot=hs, armor=arm)
                 for arm in x7_columns.values()
                 for crit, hs in x6_columns.values()]
                for _ in scenario_index.values()
                for _ in talent_index.values()]
        df = pd.DataFrame(data, index=index, columns=columns)

        # result
        return df
