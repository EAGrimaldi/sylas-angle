from typing import Iterable, Union
import urllib.request, json

#  tier list of ultimates for Sylas to steal based on Rime's challenger guide (last updated in July 2022)
#  https://docs.google.com/spreadsheets/d/16lC9hutxugFT9eOFoVWKrKNpWuAhApshUSDgciphRWA/edit#gid=0

class Calculator:
    def __init__(self) -> None:
        with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/12.7.1/data/en_US/champion.json") as url:
            champion_json = json.loads(url.read().decode())
        self.int_to_name = {}
        for champion in champion_json["data"].values():
            self.int_to_name[int(champion["key"])] = champion["name"]
        self.tiers_champs = {
            "Z": {
                "Amumu", "Blitzcrank", "Cho'Gath", "Ezreal", "Fiddle", "Gangplank", "Gnar", "Hecarim", "Malphite", "Nasus", "Rumble", "Seraphine", "Swain", "Vex", 
            },
            "S": {
                "Akali", "Alistar", "Annie", "Ashe", "Bard", "Ekko", "Gwen", "Irelia", "Ivern", "Jax", "Kennen", "Leona", "Miss Fortune", "Mordekaiser", "Morgana", 
                "Neeko", "Nocturne", "Nunu & Willump", "Renekton", "Shen", "Singed", "Twisted Fate", "Vel'Koz", "Viktor", "Volibear", "Xin Zhao", "Zeri", "Ziggs", 
            },
            "A": {
                "Ahri", "Diana", "Evelynn", "Galio", "Karthus", "Kayn", "Kindred", "Lissandra", "Lucian", "Lulu", "Malzahar", "Maokai", "Nautilus", "Nilah", 
                "Ornn", "Pantheon", "Qiyana", "Renata Glasc", "Shyvana", "Udyr", "Varus", "Veigar", "Vladimir", "Yone", "Yuumi", "Zilean", 
            },
            "B": {
                "Aatrox", "Aphelios", "Cassiopeia", "Fizz", "Garen", "Gragas", "Heimerdinger", "Karma", "Kayle", "Kled", "Lee Sin", "Lillia", "Lux", "Orianna", "Pyke", 
                "Rammus", "Rek'Sai", "Rell", "Sejuani", "Shaco", "Sett", "Sion", "Skarner", "Soraka", "Tristana", "Tryndamere", "Wukong", "Xerath", "Yasuo", "Zyra", 
            },
        }
        # UNDER REVIEW:
        # Jax rework
        # Udyr rework
        self.champs_tiers = {}
        for tier, list in self.tiers_champs.items():
            for champ in list:
                self.champs_tiers[champ] = tier
        self.tiers_scores = {"Z": 6, "S": 4, "A": 3, "B": 1}
    def champ_strength(self, champ: Union[int, str]) -> int:
        if isinstance(champ, int):
            champ = self.int_to_name(champ)
        return self.tiers_scores[self.champs_tiers[champ]] if champ in self.champs_tiers else 0
    def team_strength(self, team: Iterable[Union[int, str]]) -> int:
        strength = 0
        for champ in team:
            strength += self.champ_strength(champ)
        return strength

if __name__ == "__main__":
    import sys
    calculator = Calculator()
    champs = []
    for champ in sys.argv[1:]:
        champs.append(champ.title())
    print(calculator.team_strength(champs))