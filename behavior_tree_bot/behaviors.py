import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_enemy_with_biggest_growth_rate(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    if len(state.my_planets()) == 0:
        return False
    if len(state.enemy_planets()) == 0:
        return False

    my_strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    enemy_list = []
    for planet in state.enemy_planets():
        enemy_list.append((planet.growth_rate, planet))
    enemy_list.sort(key=lambda tup: tup[0], reverse=True)

    for planet_tuple in enemy_list:
        planet = planet_tuple[1]
        enemy_ships = planet.num_ships
        enemy_growth = planet.growth_rate
        distance = state.distance(my_strongest_planet.ID, planet.ID) + 1

        enemy_growth *= distance
        enemy_ships += enemy_growth

        if enemy_ships >= my_strongest_planet.num_ships * .75:
            return issue_order(state, my_strongest_planet.ID, planet.ID, my_strongest_planet.num_ships * .75)
    return False


def take_biggest_planet(state):
    enemy_strongest_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    my_strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    return issue_order(state, my_strongest_planet.ID, enemy_strongest_planet.ID, my_strongest_planet.num_ships * .75)

def get_best_neutral(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) get our most powerful planet
    my_strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) sort them by distance from our strongest planet
    shortest_distance = sys.maxsize
    biggest_size = -1
    lowest_value = sys.maxsize
    dest_planet = None

    best_value = sys.maxsize


    # first, get sorted list of planets by distance
    for planet in state.neutral_planets():
        cur_distance = state.distance(my_strongest_planet.ID, planet.ID)
        cur_size = planet.growth_rate
        cur_value = planet.num_ships

        if cur_value > (my_strongest_planet.num_ships * .75):
            continue

        value = (1 - cur_distance) * (cur_size * 3) * (1 - cur_value)

        if value <= best_value:
            best_value = value
            dest_planet = planet

        # if cur_distance < shortest_distance:
        #     if cur_size > biggest_size:
        #         if cur_value < lowest_value:
        #             dest_planet = planet
        #             shortest_distance = cur_distance
        #             biggest_size = cur_size
        #             lowest_value = cur_value

        # if state.distance(my_strongest_planet.ID, planet.ID) < best_distance:
        #     if planet.num_ships < (my_strongest_planet.num_ships / 2):
        #         dest_planet = planet
        #         best_distance = state.distance(my_strongest_planet.ID, planet.ID)

    # (4) return false if we cannot take a planet
    if dest_planet is None:
        return False
    return issue_order(state, my_strongest_planet.ID, dest_planet.ID, my_strongest_planet.num_ships * .75)


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
