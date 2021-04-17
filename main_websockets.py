import requests
from classes import SmashGGGetter
from urllib import parse
from dotenv import load_dotenv
from helper import _grab_and_output_file
import asyncio
import websockets
import os
import time

load_dotenv()
api = "http://ns.streameta.com/api/?token={}".format(os.environ["STREAMETA_TOKEN"])
p1 = ""
p2 = ""

async def hello():
    global p1, p2, getter
    api_result = requests.get(api).json()
    bracket_link = parse.urlparse(api_result["tournament"]["brackets"])
    # TODO: Remove Smash.GG test if new stuff is made
    if bracket_link.hostname != "smash.gg":
        raise Exception("Currently only supports smash.gg")
    getter = SmashGGGetter(bracket_link.path.strip("/"))
    while True:
        try:
            async with websockets.connect("ws://streameta.com:9000") as websocket:
                await websocket.send(os.environ["STREAMETA_TOKEN"])

                #grab initial stuff
                
                p1 = api_result["teams"][0]["players"][0]["person"]["name"]
                p2 = api_result["teams"][1]["players"][0]["person"]["name"]

                while True:
                    message = await websocket.recv()
                    await process(message)
        except:
            #Re-establish connection
            print("Resetting connection")
            pass

messages_to_get = ["teams-1","teams-0-players-0-person-name",
"teams-1-players-0-person-name"]

async def process(message):
    global p1, p2, getter
    # only process messages we're interested in
    if message in messages_to_get:
        # only one thing we care about, player names
        api_result = requests.get(api+"&subset=teams-0-players-0-person-name").json()
        p1_new = api_result["teams"][0]["players"][0]["person"]["name"]
        p2_new = api_result["teams"][1]["players"][0]["person"]["name"]

        if p1_new != p1:
            if p1_new:
                asyncio.gather(_grab_and_output_file(p1_new, getter, "p1_sets.txt"))
            else:
                with open("p1_sets.txt","w+") as file:
                    pass
        if p2_new != p2:
            if p2_new:
                asyncio.gather(_grab_and_output_file(p2_new, getter, "p2_sets.txt"))
            else:
                with open("p2_sets.txt","w+") as file:
                    pass
        p1 = p1_new[:]
        p2 = p2_new[:]
            
asyncio.get_event_loop().run_until_complete(hello())