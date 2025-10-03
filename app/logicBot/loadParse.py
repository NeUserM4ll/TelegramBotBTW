import os

from datetime import datetime, timedelta
import json

from logicBot.parser import ParseTeam, ParseMatch

class ParseJob:
    def __init__(self):
        self.parser = ParseTeam()
        self.file_path = 'players.json'
        self.update_interval = timedelta(hours=24)
    def parserLoad(self):
        if os.path.exists(self.file_path):
            last_modified = datetime.fromtimestamp(os.path.getmtime(self.file_path))
            now = datetime.now()

            if now - last_modified < self.update_interval:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print("we are using existing JSON")
                return data

        print("upload JSON ")
        self.parser.parser()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data
    

class FootballParserManager:
    def __init__(self,output_file="matches.json"):
        self.output_file = output_file

    def edit_json(self):
        with open(self.output_file, "r", encoding="utf-8") as f:
            matches = json.load(f)
        for i in range(len(matches)):
            if "score" in matches[i] and "vs" in matches[i]["score"]:
                matches[i]["score"] = "матчу еще только предстоит быть"
                matches[i]["score_home"] = 0
                matches[i]["score_away"] = 0
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=4)

    def starts(self):

        ParseMatch("ПАРИ НН","https://fcnn.ru/season/championship/calendar?_isBase=true&_limit=12&_page=1&_season=25-26-rpl&_type=championship&_view=month").run()
        self.edit_json()
        print("успех")
    
