import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def get_best_neutral(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) get our most powerful planet
    my_strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) sort them by distance from our strongest planet
    best_distance = sys.maxsize
    dest_planet = None
    for planet in state.neutral_planets():
        if state.distance(my_strongest_planet.ID, planet.ID) < best_distance:
            if planet.num_ships < (my_strongest_planet.num_ships / 2):
                dest_planet = planet
                best_distance = state.distance(my_strongest_planet.ID, planet.ID)

    # (4) return false if we cannot take a planet
    if dest_planet is None:
        return False
    return issue_order(state, my_strongest_planet.ID, dest_planet.ID, my_strongest_planet.num_ships / 2)


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
