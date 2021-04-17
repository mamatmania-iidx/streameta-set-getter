import re
import asyncio

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

async def _grab_and_output_file(player_name, getter, file_name):
    with open(file_name, mode="w+") as file:
        file.write("Fetching..\n")        
    results = getter.get_participant_sets_with_guess(player_name)
    with open(file_name, mode="w+") as file:
        bracket_name = results[0][0]
        file.write("{}\n".format(bracket_name))
        for result in results:
            if result[3] == None or result[3] == "DQ":
                continue
            if result[0] != bracket_name:
                bracket_name = result[0]
                file.write("\n{}\n".format(bracket_name))
            file.write("{} - {}\n".format(result[2],format_set_string(result[3],player_name)))
