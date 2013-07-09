#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.html as lh
from lxml.html.clean import clean_html

foo = lh.parse('http://stats.espncricinfo.com/stats/engine/player/45789.html?class=11;type=allround;template=results')
foo = foo.xpath("//tr[contains(@class, 'data1')]")

class Mappings:
    self.country_codes = {
        'Afghanistan' : 40,
        'Australia' : 2,
        'Bangladesh' : 25,
        'Bermuda' : 12,
        'England' : 1,
        'Hong Kong' : 19,
        'India' : 6,
        'Ireland' : 29,
        'Netherlands' : 15,
        'New Zealand' : 5,
        'Pakistan' : 7,
        'Scotland' : 30,
        'South Africa' : 3,
        'Sri Lanka' : 8,
        'West Indies' : 4,
        'Zimbabwe' : 9
    }

    self.venues = {
        'home' : 1,
        'away' : 2,
        'neutral' : 3
    }

    self.formats = {
        'Tests' : 1,
        'ODIs' : 2,
        'T20Is' : 3,
        'All' : 11
    }

    self.mappings = {
        'class' : self.formats,
        'opposition' : self.country_codes,
        'host' : self.country_codes,
        'home_or_away' : self.venues,
        'year' : ''
    }

class PlayerFinder:
    base_url = "http://stats.espncricinfo.com"
    def __init__(self, player_name):
        self.player_name = player_name
        self.response = ""

    def zero_in(self):
        stats_url = self.base_url + \
                "/stats/engine/stats/analysis.html?search=" + \
                self.player_name.replace(" ", "+") + ";template=analysis"
        document = lh.parse(stats_url)
        entries = document.xpath('//a[contains(text(), "Combined Test, ODI and T20I player")]')
        players = document.findall("//span[@style='white-space: nowrap']")

        if len(entries) > 1:
            self.response = []
            for player in players:
                player_text = player.text
                if player_text[0] != "(" and player_text[-1] != ")":
                    self.response.append(player_text)
            self.response = "Huh? " + " or ".join(self.response) + "?"
        elif len(entries) == 0:
            self.response = "Not found."
        else:
            self.response = self.base_url + entries[0].get('href')

        return self.response

if __name__ == "__main__":
    foo = str(raw_input())
    bar = PlayerFinder(foo)
    print bar.zero_in()
