

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_can_take_biggest_enemy(state):
    enemy_strongest_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    my_strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    try:
        enemy_ships = enemy_strongest_planet.num_ships
        enemy_growth = enemy_strongest_planet.growth_rate
        distance = state.distance(my_strongest_planet.ID, enemy_strongest_planet.ID)

        enemy_growth *= distance
        enemy_ships += enemy_growth

        if enemy_ships <= (my_strongest_planet.num_ships * .75):
            return True
    except AttributeError:
        return False
    return False


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_opponent_has_visited_planets(state):
    if len(state.enemy_planets) == 0:
        return False
    return True
