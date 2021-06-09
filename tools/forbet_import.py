from html.parser import HTMLParser

import requests

column_names_dict = {'1': 'win_a', '2': 'win_b', 'X': 'tie', '1/X': 'win_tie_a', 'X/2': 'win_tie_b', '1/2': 'not_tie'}


def tuples_to_dic(tuples):
    return {t[0]: t[1] for t in tuples}


class MyHTMLParser(HTMLParser):

    def __init__(self):
        self.data = {}
        super().__init__()

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag, attrs)
        if ('class', 'event-rate') in attrs:
            entry = tuples_to_dic(attrs)
            eventname = tuple(entry['data-eventname'].split(" - "))
            outcomename = entry['data-outcomename']
            if outcomename == eventname[0]:
                outcomename = '1'
            if outcomename == eventname[1]:
                outcomename = '2'
            outcomeodds = entry['data-outcomeodds']
            if eventname not in self.data:
                self.data[eventname] = {}
            self.data[eventname][outcomename] = outcomeodds

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def feed_games(self, game_type):
        url = 'https://www.iforbet.pl/BettingServlet'
        query_data = {'action': 'getGamesForMarketType', 'categoryId': '36955', 'marketType': '1', 'sportId': '1',
                      'gameType': game_type}
        self.feed(requests.post(url, data=query_data).text)


parser = MyHTMLParser()
parser.feed_games('1')
parser.feed_games('4')
print(parser.data)

with open('odds.sql', 'w') as f:
    for match, odds in parser.data.items():
        print("UPDATE matches SET " + ", ".join([column_names_dict[result]
                                                 + "=" + odd for result, odd in odds.items()]) +
              f" WHERE team_a='{match[0]}' AND team_b='{match[1]}';", file=f)
