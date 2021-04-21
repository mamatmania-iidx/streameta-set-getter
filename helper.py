import re
import asyncio
from difflib import get_close_matches

def format_set_string(string, player):
    result = re.match("(.*) ([0-9]+) - (.*) ([0-9]+)", string)
    p1 = result[1]
    p1_score = result[2]
    p2 = result[3]
    p2_score = result[4]

    # Remove player crew/team
    temp = p1.split("|")
    if len(temp) > 1:
        p1_teamless = "".join(temp[1:]).strip()
    else:
        p1_teamless = p1

    temp = p2.split("|")
    if len(temp) > 1:
        p2_teamless = "".join(temp[1:]).strip()
    else:
        p2_teamless = p2

    closest = get_close_matches(player, [p1_teamless, p2_teamless])

    # Modify here if you want to customize things
    if closest[0] == p1_teamless:
        # Player won
        return "{}-{} ✔ {}".format(p1_score, p2_score, p2_teamless)
    else:
        # Player lost
        return "{}-{} ❌ {}".format(p2_score, p1_score, p1_teamless)

round_dict = {"Quarter-Final": "Quarters",
        "Semi-Final": "Semis",
        "Final": "Final"}

def process_round_name(round):
    if round in "Grand Final Reset":
        # Leave GF and GF reset untouched
        return round
    else:
        temp = round.split(" ")
        result = temp[0] + " "
        try:
            result += round_dict[" ".join(temp[1:])]
        except:
            for i in temp[1:]:
                result += i[0]
        return result

async def _grab_and_output_file(player_name, getter, file_name, max_matches=999):
    with open(file_name, mode="w+", encoding='utf-8') as file:
        file.write("Fetching..\n")
    try:    
        results = getter.get_participant_sets_with_guess(player_name)
        results = results[-max_matches:]
        with open(file_name, mode="w+", encoding='utf-8') as file:
            #Modify here for custom formatting.
            #bracket_name = results[0][0]
            #file.write("{} | ".format(bracket_name))
            for result in results:
                if result[3] == None or result[3] == "DQ":
                    continue
                #if result[0] != bracket_name:
                #    bracket_name = result[0]
                #    file.write("{} | ".format(bracket_name))
                file.write("{}\n".format(format_set_string(result[3],player_name)))
    except:
        with open(file_name, mode="w+") as file:
            file.write("Player not found in SmashGG.\n")
