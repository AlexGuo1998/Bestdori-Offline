# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Team builder
# Date:        2019/12/19
# ==============================================

import typing

from profile_manager import Item, Card, Profile
from song_manager import Song


class Band:
    def __init__(self):
        self.target = 0  # for add-to-result comparision
        self.cards: typing.Tuple[Card, Card, Card, Card, Card] = (Card(), Card(), Card(), Card(), Card())

    def bandPower(self, items: typing.Union[typing.List[Item], None] = None):
        if items is None:
            return sum(sum(card.params) for card in self.cards)
        else:
            return sum(sum(item.getItemBonus(card)) for item in items for card in self.cards)

    def eventBonus(self, ):
        return


class TeamBuilder:
    def __init__(self):
        pass

    def run(self, cards: typing.List[Card], items: typing.List[typing.List[Item]], song: Song):
        self.preProcess(cards)
        pass

    def preProcess(self, cards: typing.List[Card]) -> typing.Dict[Card, dict]:
        # return {x: {} for x in cards}
        pass
