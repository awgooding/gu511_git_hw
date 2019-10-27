# example from Network tab in Chrome's developer source tools
# Request URL: https://projects.fivethirtyeight.com/complete-history-of-the-nba/data/warriors.json?v=23
# Request Method: GET
# Status Code: 200
# Remote Address: 151.101.250.109:443
# Referrer Policy: no-referrer-when-downgrade


import requests

def get_elo_hist(team_name):

    response =  requests.get(
        url = 'https://projects.fivethirtyeight.com/complete-history-of-the-nba/data/'+team_name+'.json',
        params = {
            #'name':team_name,
            'v':'23'
        }
    )

    return response.json()


def test():
    assert get_elo_hist('lakers')['value'][0]['y'] == 1527
    assert get_elo_hist('bucks')['value'][0]['x'] == 1969