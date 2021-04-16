import requests
from classes import SmashGGGetter
from urllib import parse
from dotenv import load_dotenv
import re
import os
import time

load_dotenv()

# Format sets for clarity, because pain.
def format_set_string(string, player):
    result = re.match("(.*) ([0-9]+) - (.*) ([0-9]+)", string)
    p1 = result[1]
    p1_score = result[2]
    p2 = result[3]
    p2_score = result[4]
    if player.lower() in p1.lower():
        temp = p2.split("|")
        if len(temp) > 1:
            p2 = "".join(p2.split("|")[1:]).strip()
        return "{}-{} vs {}".format(p1_score, p2_score, p2)
    else:
        temp = p1.split("|")
        if len(temp) > 1:
            p1 = "".join(p1.split("|")[1:]).strip()
        return "{}-{} vs {}".format(p2_score, p1_score, p1)



site = requests.get(os.environ["STREAMETA_API_LINK"]).json()
bracket_link = parse.urlparse(site["tournament"]["brackets"])
getter = SmashGGGetter(bracket_link.path.strip("/"))


while True:

    p1 = site["teams"][0]["players"][0]['person']['name']
    p2 = site["teams"][1]["players"][0]['person']['name']

    player_name = p1
    results = getter.get_participant_sets_with_guess(player_name)
    with open("p1_sets.txt", mode="w+") as file:
        bracket_name = results[0][0]
        file.write("{}\n".format(bracket_name))
        for result in results:
            if result[3] == None or result[3] == "DQ":
                continue
            if result[0] != bracket_name:
                bracket_name = result[0]
                file.write("{}\n".format(bracket_name))
            file.write("{} - {}\n".format(result[2],format_set_string(result[3],player_name)))


    player_name = p2
    results = getter.get_participant_sets_with_guess(player_name)
    with open("p2_sets.txt", mode="w+") as file:
        bracket_name = results[0][0]
        file.write("{}\n".format(bracket_name))
        for result in results:
            if result[3] == None or result[3] == "DQ":
                continue
            if result[0] != bracket_name:
                bracket_name = result[0]
                file.write("\n{}\n".format(bracket_name))
            file.write("{} - {}\n".format(result[2],format_set_string(result[3],player_name)))

    time.sleep(3)
    site = requests.get(os.environ["STREAMETA_API_LINK"]).json()