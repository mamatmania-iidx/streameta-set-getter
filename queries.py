GET_TOURNAMENT_EVENT_NAME="""
query ($eventSlug: String){
  event(slug: $eventSlug){
    name
    tournament{
      name
    }
  }
}
"""


GET_PARTICIPANTS_ID = """
query ($eventSlug: String, $page: Int){
  event(slug: $eventSlug){
    entrants(query:{
      page:$page
      perPage:32}){
      pageInfo {
        total
        totalPages
      }
      nodes{
        id
        participants{
          id
          gamerTag
        }
      }
    }
  }
}
"""

GET_PARTICIPANT_SET ="""
query ParticipantSet($eventSlug: String, $playerId: ID){
  event(slug: $eventSlug){
    sets(filters:
    {
      entrantIds:[$playerId]
      hideEmpty:true
    }){
      nodes{
        phaseGroup {
            displayIdentifier
                phase{
                    name
                }
            }
        fullRoundText
        displayScore
        completedAt
        
      }
    }
  }
}"""