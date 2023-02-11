from typing import Iterable, Union
import urllib.request, json

#  tier list of ultimates for Sylas to steal
#  partially based on Rime's (NA challenger) tier list (last updated August 2022)
#  https://docs.google.com/spreadsheets/d/16lC9hutxugFT9eOFoVWKrKNpWuAhApshUSDgciphRWA/edit#gid=0
#  partially based on BZ's (EUW challenger) tier list (last updated February 2023)
#  https://twitter.com/BZ_EUW/status/1621602893735280640

class Calculator:
    def __init__(self) -> None:
        with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/12.7.1/data/en_US/champion.json") as url:
            champion_json = json.loads(url.read().decode())
        self.int_to_name = {}
        for champion in champion_json["data"].values():
            self.int_to_name[int(champion["key"])] = champion["name"]
        self.tiers_champs = {
            "Z": {
                "Alistar", "Amumu", "Ashe", "Blitzcrank", "Fiddle", "Gangplank", "Gnar", "Hecarim", "Jax", "Malphite", "Nasus", "Rumble", "Singed", "Swain", 
                "Udyr", "Varus", "Vex", "Zeri", 
            },
            "S": {
                "Akali", "Annie", "Azir", "Cho'Gath", "Ekko", "Ezreal", "Garen", "Irelia", "Ivern", "Kayle", "Kennen", "Leona", "Lissandra", "Lucian", "Mordekaiser", 
                "Morgana", "Nautilus", "Neeko", "Pantheon", "Sejuani", "Seraphine", "Shen", "Twisted Fate", "Veigar", "Viktor", "Volibear", "Xin Zhao", "Ziggs", 
            },
            "A": {
                "Aatrox", "Ahri", "Aurelion Sol", "Cassiopeia", "Corki", "Diana", "Evelynn", "Galio", "Gragas", "Gwen", "Heimerdinger", "Karma", "Karthus", "Kayn", 
                "Lulu", "Malzahar", "Maokai", "Miss Fortune", "Nunu & Willump", "Nocturne", "Ornn", "Qiyana", "Rammus", "Rell", "Renata Glasc", "Renekton", "Shaco", 
                "Shyvana", "Sona", "Tahm Kench", "Teemo", "Tristana", "Urgot", "Vel'Koz", "Vladimir", "Xerath", "Yone", "Yuumi", "Zed", "Zilean", 
            },
            "B": {
                "Bard", "Braum", "Fizz", "Jarvan IV", "Katarina", "Kindred", "Kled", "Lee Sin", "Lillia", "Lux", "Nilah", "Olaf", "Orianna", "Pyke", "Rakan", "Rek'Sai", 
                "Riven", "Ryze", "Sett", "Sion", "Skarner", "Soraka", "Taliyah", "Talon", "Taric", "Tryndamere", "Vi", "Warwick", "Wukong", "Yasuo", "Zyra", 
            },
        }
        # UNDER REVIEW:
        # Aurelion Sol rework
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