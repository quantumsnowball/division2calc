from build import Build

legendary1 = Build(
    name='Legendary1',
    base_damage=44191,
    n_red_core=5,
    watch_score=50,
    weapon_damage_bonus_pct=0.15,
    specialization_bonus_pct=0.15,
    expertise_level=17,
    critical_hit_chance=0.52,
    critical_hit_damage=1.37,
    headshot_damage=0.95,
    damage_to_armor=0,
    damage_to_health=0.21,
    damage_to_target_out_of_cover=0,
)


def main():
    print(f'{
        legendary1.total_damage(critical=True,
                                headshot=True,
                                dtoHealth=True)=:,.2f
    }')
    print(legendary1.summary())


if __name__ == '__main__':
    main()
