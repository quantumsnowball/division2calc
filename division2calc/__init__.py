import pprint
from pathlib import Path
from typing import Literal, get_args

import click
import pandas as pd

import division2calc.gear.attrs as gearattrs
import division2calc.gear.brandsets.Lengmo as Lengmo
import division2calc.gear.brandsets.OverlordArmaments as Overlord
import division2calc.gear.gearsets.StrikersBattlegear as Striker
import division2calc.gear.mods as gearmods
from division2calc.build import Build
from division2calc.build.specialization import Gunner
from division2calc.utils import load_builds_file, pformat_dataclass
from division2calc.weapon.StElmosEngine import StElmosEngine

__all__ = [
    'Build',
    'Gunner',
    'StElmosEngine',
    'Striker',
    'Lengmo',
    'Overlord',
    'gearattrs',
    'gearmods',
]


@click.group()
def division2calc() -> None:
    pass


@division2calc.command()
@click.argument('file', required=True, type=click.Path())
@click.option('-i', '--index', type=int, default=0, help='which build in the list to display')
@click.option('--x', is_flag=True, default=False, help='Enable x summary')
@click.option('--damage', is_flag=True, default=False, help='Enable damage summary')
@click.option('--dydx', is_flag=True, default=False, help='Enable dydx summary')
def summary(file: Path,
            index: int,
            damage: bool,
            x: bool,
            dydx: bool) -> None:
    build = load_builds_file(file)[index]
    all = not any((x, damage, dydx))
    if all or damage:
        click.secho(f'\ndamage: Build({build.name})', fg='yellow')
        print(build.summary.damage().round(2))
    if all or x:
        click.secho(f'\nx: Build({build.name})', fg='yellow')
        print(build.summary.x.round(4))
    if all or dydx:
        click.secho(f'\ndydx: Build({build.name})', fg='yellow')
        print(build.summary.dydx.round(4))
    # pprint.pp(dataclass_asdict(build))
    # print(build_as_yaml(build))
    # pprint.pp(build)
    # print(pformat_dataclass(build))


@division2calc.command()
@click.argument('file', required=True, type=click.Path())
@click.option('-i', '--indices', default=(0, 1,), type=click.Tuple([int, int]),
              help='which two builds in the list to display, e.g. -i 0 1')
@click.option('--x', is_flag=True, default=False, help='Enable x comparison')
@click.option('--damage', is_flag=True, default=False, help='Enable damage comparison')
@click.option('--dydx', is_flag=True, default=False, help='Enable dydx comparison')
def compare(file: Path,
            indices: tuple[int, int],
            damage: bool,
            x: bool,
            dydx: bool) -> None:
    builds = load_builds_file(file)
    build1, build2 = tuple(builds[i] for i in indices)
    all = not any((x, damage, dydx))
    if all or damage:
        click.secho(f'\ndiff(damage): Build({build2.name}) net Build({build1.name})', fg='yellow')
        diff: pd.DataFrame = build2.summary.damage() - build1.summary.damage()
        print(diff.round(2))
        click.secho(f'\ndiff%(damage): Build({build2.name}) net Build({build1.name})', fg='yellow')
        diffpct: pd.DataFrame = (build2.summary.damage() / build1.summary.damage() - 1)*100
        print(diffpct.round(4))
    if all or x:
        click.secho(f'\ndiff(x): Build({build2.name}) net Build({build1.name})', fg='yellow')
        diff: pd.DataFrame = build2.summary.x - build1.summary.x
        print(diff.round(4))
    if all or dydx:
        click.secho(f'\ndiff(dydx): Build({build2.name}) net Build({build1.name})', fg='yellow')
        diff: pd.DataFrame = build2.summary.dydx - build1.summary.dydx
        print(diff.round(4))


Metric = Literal['damage', 'x', 'dydx']
Profile = Literal['basic', 'min', 'average', 'max']
SortOrder = Literal['asc', 'desc']
SortBy = tuple[str, SortOrder]
ClickMetric = click.Choice(get_args(Metric))
ClickProfile = click.Choice(get_args(Profile))
ClickSortOrder = click.Choice(get_args(SortOrder))
ClickSortBy = click.Tuple([str, ClickSortOrder])


@division2calc.command()
@click.argument('file', required=True, type=click.Path())
@click.option('-m', '--metric', default='damage', type=ClickMetric)
@click.option('-p', '--profile', default='basic', type=ClickProfile)
@click.option('-by', '--sort-by', default=None, type=ClickSortBy,
              help='sort dataframe by field with order, e.g. -by x6 desc')
def rank(file: Path,
         metric: Metric,
         profile: Profile,
         sort_by: SortBy) -> None:
    builds = load_builds_file(file)
    data = {b.name: getattr(b.summary, metric).loc[profile]
            for b in builds}
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.names = ('build name',)
    df.columns.names = (metric,)
    if sort_by:
        by, order = sort_by
        df.sort_values(by, ascending=order == 'asc', inplace=True)
    print(df)
