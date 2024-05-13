import click

import division2calc.gear.attrs as gearattrs
import division2calc.gear.brandsets.Lengmo as Lengmo
import division2calc.gear.brandsets.OverlordArmaments as Overlord
import division2calc.gear.gearsets.StrikersBattlegear as Striker
import division2calc.gear.mods as gearmods
import division2calc.weapon.AR as AR
from division2calc.agent import Build
from division2calc.agent.specialization import Gunner
from division2calc.command.breakdown import breakdown
from division2calc.command.compare import compare
from division2calc.command.damage import damage
from division2calc.command.dydx import dydx
from division2calc.command.rank import rank
from division2calc.command.stats import stats
from division2calc.command.summary import summary
from division2calc.command.x import x

__all__ = [
    'Build',
    'Gunner',
    'AR',
    'Striker',
    'Lengmo',
    'Overlord',
    'gearattrs',
    'gearmods',
]


@click.group()
def division2calc() -> None:
    pass


division2calc.add_command(stats)
division2calc.add_command(breakdown)
division2calc.add_command(damage)
division2calc.add_command(x)
division2calc.add_command(dydx)
division2calc.add_command(summary)
division2calc.add_command(compare)
division2calc.add_command(rank)
