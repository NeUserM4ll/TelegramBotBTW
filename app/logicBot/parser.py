
import requests
from bs4 import BeautifulSoup
import json
import os
import time


url = "https://fcnn.ru/season/championship/stat"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')




class ParseTeam:
    def __init__(self):
       
        self.players = []
   
    def parser(self):
        for row in soup.select('table tr'):
            cols = row.find_all('td')
            if len(cols) >= 12:  # 12 колонок: #, имя, позиция, и, ип, бз, вз, вбз, г, ПАС, п, у
                # Чистим дубли в имени
                name = ' '.join(cols[1].get_text(strip=True).split())
                player = {
                    'number': cols[0].get_text(strip=True),
                    'name': name,
                    'position': cols[2].get_text(strip=True),
                    'matches': cols[3].get_text(strip=True),        
                    'full_games': cols[4].get_text(strip=True),       
                    'was_replaced': cols[5].get_text(strip=True),      
                    'came_replace': cols[6].get_text(strip=True),     
                    'was_and_came_replace': cols[7].get_text(strip=True), 
                    'goals': cols[8].get_text(strip=True),           
                    'assists': cols[9].get_text(strip=True),          
                    'yellow_cards': cols[10].get_text(strip=True),   
                    'red_cards': cols[11].get_text(strip=True),      
                    'image': cols[1].find('img')['src'] if cols[1].find('img') else None
                }
                self.players.append(player)

       
        with open('player.json', 'w', encoding='utf-8') as f:
            json.dump(self.players, f, ensure_ascii=False, indent=4)

        print(f"Сохранили {len(self.players)} игроков в player.json")

class ParseGame:
    def __init__(self):
        self.game = []
        self.statTeam = {}

    def parser(self):
       for row in soup.select('.TableTeamStat-module__bDPElrad tr'):
        cells = row.find_all('td')
        if len(cells) == 4:  # We expect 4 cells: statistic name, total, home, away
            stat_name = cells[0].get_text(strip=True)
            total = int(cells[1].get_text(strip=True))
            home = int(cells[2].get_text(strip=True))
            away = int(cells[3].get_text(strip=True))
            
            # Store the statistics in the dictionary
            self.statTeam[stat_name] = {
                'всего': total,
                'дома': home,
                'в гостях': away
            }
            with open('players.json', 'w', encoding='utf-8') as f:
                json.dump(self.statTeam, f, ensure_ascii=False, indent=4)



        pass

class ParseMatch:
        def __init__(self, team_name, url, output_file="matches.json"):
            self.team_name = team_name
            self.url = url
            self.output_file = output_file
            self.headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/118.0.5993.0 Safari/537.36"
                )
            }
            self.expire_seconds = 24 * 60 * 60  # 24 часа

        def is_file_expired(self):
            if not os.path.exists(self.output_file):
                return True
            mtime = os.path.getmtime(self.output_file)
            return (time.time() - mtime) > self.expire_seconds

        def run(self):
            if not self.is_file_expired():
                print(f"Файл {self.output_file} ещё свежий, не обновляем.")
                return

            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            matches = []

            for article in soup.select(
                "ul.ArticleMonth-module__iqjysL3m article.ArticleCalendarLine-module__tNh6P3l9"
            ):
                tour = article.select_one(
                    "div.ArticleCalendarLine-module__lDB62GZ2 span"
                ).get_text(strip=True)
                date_day = article.select_one(
                    "div.ArticleCalendarLine-module__GsPDVEsn span:nth-child(1)"
                ).get_text(strip=True)
                date_month = article.select_one(
                    "div.ArticleCalendarLine-module__GsPDVEsn span:nth-child(2)"
                ).get_text(strip=True)
                date_time = article.select_one(
                    "div.ArticleCalendarLine-module__t1ZF4tjN span:nth-child(2)"
                ).get_text(strip=True)

                teams = article.select("div.VersusLine-module__TQtiY22F h3")
                if len(teams) == 2:
                    home = teams[0].get_text(strip=True)
                    away = teams[1].get_text(strip=True)
                else:
                    continue

                score_div = article.select_one("div.VersusLine-module__dyCmWl4f")
                score_text = score_div.get_text(strip=True) if score_div else None

                score_home = score_away = None
                team_stats = {
                    "played": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "goals_for": 0,
                    "goals_against": 0,
                    "points": 0,
                }

                if score_text:
                    parts = score_text.split("-")
                    if len(parts) == 2:
                        score_home = int(parts[0].strip())
                        score_away = int(parts[1].strip())

                        if self.team_name in [home, away]:
                            team_stats["played"] = 1
                            if self.team_name == home:
                                team_stats["goals_for"] = score_home
                                team_stats["goals_against"] = score_away
                                if score_home > score_away:
                                    team_stats["wins"] = 1
                                    team_stats["points"] = 3
                                elif score_home == score_away:
                                    team_stats["draws"] = 1
                                    team_stats["points"] = 1
                                else:
                                    team_stats["losses"] = 1
                            else:  # self.team_name == away
                                team_stats["goals_for"] = score_away
                                team_stats["goals_against"] = score_home
                                if score_away > score_home:
                                    team_stats["wins"] = 1
                                    team_stats["points"] = 3
                                elif score_away == score_home:
                                    team_stats["draws"] = 1
                                    team_stats["points"] = 1
                                else:
                                    team_stats["losses"] = 1

                matches.append(
                    {
                        "tour": tour,
                        "date": f"{date_day} {date_month}",
                        "time": date_time,
                        "home": home,
                        "away": away,
                        "score": score_text,
                        "score_home": score_home,
                        "score_away": score_away,
                        "team_stats": team_stats,
                    }
                )

            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(matches, f, ensure_ascii=False, indent=4)

            print(f"Сохранили {len(matches)} матчей в {self.output_file}")


if __name__ == "__main__":

    parrt = ParseTeam()
    parrt.parser()

