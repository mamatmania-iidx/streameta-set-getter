from queries import *
import pandas
import requests
import os
from dotenv import load_dotenv
from difflib import get_close_matches

# class EventGetter:
#     @abstractmethod
#     def _get_tournament_event_name(self):
#         pass


class SmashGGGetter:
    def __init__(self, event):
        self.slug = event
        self.headers = {"Authorization": "Bearer {}".format(os.environ["SMASHGG_KEY"])}
        self.url = "https://api.smash.gg/gql/alpha"
        self.participants = dict()
        self.event = ""
        self.tournament = ""

        self._get_tournament_event_name()
        self._get_participants_from_server()


    def _get_tournament_event_name(self):
        variables = {"eventSlug":self.slug}
        query_result = self._run_query(GET_TOURNAMENT_EVENT_NAME, variables)
        try:
            self.event = query_result["data"]["event"]["name"]
            self.tournament = query_result["data"]["event"]["tournament"]["name"]
        except:
            raise Exception("Invalid slug.")


    def _get_participants_from_server(self):
        variables = {"eventSlug": self.slug}
        query_result = self._run_query(GET_PARTICIPANTS_ID, variables, page=1)
        pages = []
        #get page count
        max_count = query_result["data"]["event"]["entrants"]["pageInfo"]["totalPages"]
        
        def create_entrant_dict(query_result):
            df = pandas.json_normalize(query_result["data"]["event"]["entrants"]["nodes"])
            # Get gamerTag out
            df['participants']=df['participants'].apply(lambda x: x[0]['gamerTag'])
            df['participants'] = df['participants'].str.lower()
            return dict(zip(df['participants'], df['id']))

        pages.append(create_entrant_dict(query_result))

        # repeat for more than 1 page
        for i in range(2,max_count+1):
            query_result = self._run_query(GET_PARTICIPANTS_ID, variables, page=i)
            pages.append(create_entrant_dict(query_result))
        
        #merge
        for i in range(len(pages)):
            self.participants.update(pages[i])

    def get_participant_sets(self, participant):
        try:
            participant_id = self.participants[participant.lower()]
        except:
            raise KeyError("Player not found.")

        variables = {"eventSlug": self.slug, "playerId": participant_id}
        query_result = self._run_query(GET_PARTICIPANT_SET, variables)
        
        if query_result["data"]["event"]["sets"]["nodes"] is None:
            return None

        temp = pandas.json_normalize(query_result["data"]["event"]["sets"]["nodes"])
        temp = temp.reindex(columns= ['phaseGroup.phase.name', 'phaseGroup.displayIdentifier', 'fullRoundText', 'displayScore'])
        arr = temp.iloc[::-1].values.tolist()
        return arr

    def get_close_participant_name(self, search_string):
        return get_close_matches(search_string.lower(), self.participants.keys())

    def get_participant_sets_with_guess(self, participant):
        result = self.get_close_participant_name(participant)
        return self.get_participant_sets(result[0])
    
    def _run_query(self, query, variables=dict(), page=False):
        if page:
            variables["page"]=page
        r = requests.post(self.url, json={"query":query,"variables":variables},headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception("Something bad occurred with the connection")

if __name__ == "__main__":
    load_dotenv()
    test = SmashGGGetter("tournament/couchwarriors-qld-ranking-battles-march-2021-1/event/smash-ultimate-singles")
    print(test.get_participant_sets_with_guess("fez"))
    
