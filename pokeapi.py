import requests
from pprint import pprint

BASE_URL = "http://pokeapi.co/api/v2"
SPRITE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites"
ENDPOINTS = [
    "ability",
    "berry",
    "berry-firmness",
    "berry-flavor",
    "characteristic",
    "contest-effect",
    "contest-type",
    "egg-group",
    "encounter-condition",
    "encounter-condition-value",
    "encounter-method",
    "evolution-chain",
    "evolution-trigger",
    "gender",
    "generation",
    "growth-rate",
    "item",
    "item-attribute",
    "item-category",
    "item-fling-effect",
    "item-pocket",
    "language",
    "location",
    "location-area",
    "machine",
    "move",
    "move-ailment",
    "move-battle-style",
    "move-category",
    "move-damage-class",
    "move-learn-method",
    "move-target",
    "nature",
    "pal-park-area",
    "pokeathlon-stat",
    "pokedex",
    "pokemon",
    "pokemon-color",
    "pokemon-form",
    "pokemon-habitat",
    "pokemon-shape",
    "pokemon-species",
    "region",
    "stat",
    "super-contest-effect",
    "type",
    "version",
    "version-group",
]


def api_url_build(endpoint, resource_id=None, subresource=None):
    if resource_id is not None:
        if subresource is not None:
            return "/".join([BASE_URL, endpoint, str(resource_id), subresource, ""])

        return "/".join([BASE_URL, endpoint, str(resource_id), ""])

    return "/".join([BASE_URL, endpoint, ""])


def call_api(endpoint, resource_id=None, subresource=None):
    url = api_url_build(endpoint, resource_id, subresource)

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return data


class Pokemon:
    def __init__(self, name, v):
        self.types = []
        self.learnset = {}
        self.moves = []
        self.tmhm = []
        self.generate_mon(name, v)

    def generate_mon(self, name, v):
        data = call_api("pokemon", name)

        for slot in data["types"]:
            self.types.append(slot["type"]["name"])

        self.name = data["name"]
        self.id = data["id"]

        self.base_exp = data["base_experience"]

        self.base_hp = data["stats"][0]["base_stat"]
        self.base_attack = data["stats"][1]["base_stat"]
        self.base_defence = data["stats"][2]["base_stat"]
        self.base_sp_attack = data["stats"][3]["base_stat"]
        self.base_sp_defence = data["stats"][4]["base_stat"]
        self.base_speed = data["stats"][5]["base_stat"]

        for move in data["moves"]:
            name = move["move"]["name"]
            
            for version in move["version_group_details"]:
                # print(version)
                if v == version["version_group"]["name"]:
                    # print(name)
                    if version["level_learned_at"] > 0:
                        self.learnset[version["level_learned_at"]] = name
                    else:
                        self.tmhm.append(name)


mon = Pokemon("squirtle", "red-blue")

# print(mon.types)
# print(mon.name)
# print(mon.id)
# print(mon.base_hp)
# print(mon.base_speed)
print(mon.moves)
print(mon.learnset)
print(mon.tmhm)
        
        
