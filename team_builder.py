# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Team builder
# Date:        2019/12/19
# ==============================================
import timeit
import typing
import functools
from profile_manager import Item, Card, Profile


# from song_manager import Song
class Song:
    pass


class Team:
    def __init__(self):
        self.target = 0  # for add-to-result comparision
        # self.cards: typing.Tuple[Card, Card, Card, Card, Card] = (Card(), Card(), Card(), Card(), Card())
        self.cards: typing.Tuple[Card, Card, Card, Card, Card] = None
        self.items: typing.List[Item] = []
        # following fields only get filled in post-process
        self.bandPower = 0
        self.bandPowerRaw = 0
        self.eventPoint = 0
        self.eventBonus = 0
        self.scoreMax = 0
        self.scoreMin = 0
        self.scoreAvg = 0
        self.scoreMaxCount = 0

    def __str__(self):
        items = [x.id for x in self.items]
        return f'target={int(self.target)}, leader={self.cards[0]}, item={items}'


class TeamBuilder:
    def __init__(self):
        # make some data global for convenience
        self.song: Song = Song()
        self.pRate: float = 1.
        self.result: typing.List[Team] = []
        self.cardData: typing.Dict[Card, dict] = {}
        self.activeItems: typing.List[Item] = []

        self.stopCount = [0] * 5  # stop when x card needed

    def run(self, cards: typing.List[Card], itemList: typing.List[typing.List[typing.List[Item]]], song: Song,
            pRate: float = 1., forceCenter: typing.Union[typing.Sequence[Card], None] = None,
            teamCount=10):
        # TODO: free live only, max team power
        if forceCenter is None:
            forceCenter = cards
        self.song = song
        self.pRate = pRate
        self.result = [Team()] * teamCount
        self.stopCount = [0] * 5
        for self.activeItems in self.enumerateItems(itemList):
            self.cardData = self.preProcess(cards, forceCenter)
            # self.sortCards(cards)
            self.bruteForceBuilder(cards)
        self.postProcess()
        return self.result

    def preProcess(self, cards: typing.List[Card], forceCenter: typing.Sequence[Card]) -> typing.Dict[Card, dict]:
        def addBonus(x, y):
            a, b, c = x
            d, e, f = y
            return a + d, b + e, c + f

        o = {}
        for card in cards:
            data = {}
            data['center'] = card in forceCenter
            data['skillTag'] = card.skillId * 10 + card.skillLevel  # TODO
            data['skillMul'] = data['skillTag']  # TODO
            # TODO: cache other data?
            bonus = functools.reduce(addBonus, (item.getItemBonus(card) for item in self.activeItems), (0, 0, 0))
            data['power'] = sum(x * (1 + y) for x, y in zip(card.params, bonus))
            o[card] = data
        return o

    @staticmethod
    def enumerateItems(itemList: typing.List[typing.List[typing.List[Item]]]) -> typing.Iterator[typing.List[Item]]:
        def nextGroup():
            index = len(groups) - 1
            while index >= 0:
                groups[index] += 1
                if groups[index] >= len(itemList[index]):
                    groups[index] = 0
                    index -= 1
                else:
                    return True
            return False

        groups = [0] * len(itemList)
        more = True
        while more:
            o = []
            for itemType, group in enumerate(groups):
                o.extend(itemList[itemType][group])
            yield o
            more = nextGroup()

    def bruteForceBuilder(self, cards):
        self._bruteForceBuilderHelper(cards, [])

    def _bruteForceBuilderHelper(self, cardsIn: typing.List[Card], cardsOut: typing.List[Card]):
        needCount = 5 - len(cardsOut)
        if needCount == 0:
            self.stopCount[0] += 1
            self.addToResult(cardsOut)
        else:
            # test character id, filter unusable cards
            characterOut = set(x.character for x in cardsOut)
            cardsIn = [x for x in cardsIn if x.character not in characterOut]
            # sort cards
            self.sortCards(cardsIn, needCount)
            # test for early-stop
            if needCount < 5 and not self.testContinueBuilding(cardsIn, cardsOut):
                self.stopCount[needCount] += 1
                return
            while len(cardsIn) >= needCount:
                newCard = cardsIn.pop(0)
                newCardOut = cardsOut + [newCard]
                self._bruteForceBuilderHelper(cardsIn, newCardOut)

    def sortCards(self, cards: typing.List[Card], needCount: int) -> None:
        if needCount == 5:
            # center first
            cards.sort(key=lambda card: self.cardData[card]['skillMul'], reverse=True)
            cards.sort(key=lambda card: self.cardData[card]['power'], reverse=True)
            cards.sort(key=lambda card: self.cardData[card]['center'], reverse=True)
        elif needCount == 4:
            # power first
            cards.sort(key=lambda card: self.cardData[card]['skillMul'], reverse=True)
            cards.sort(key=lambda card: self.cardData[card]['power'], reverse=True)
        else:
            # need not to sort, already sorted in (4)
            pass

    def testContinueBuilding(self, cardsIn: typing.List[Card], cardsOut: typing.List[Card]) -> bool:
        assert len(cardsIn) > 0
        needCount = 5 - len(cardsOut)
        power = sum(self.cardData[x]['power'] for x in cardsOut)
        maxPowerIn = self.cardData[cardsIn[0]]['power']
        power += maxPowerIn * needCount
        return power > self.result[-1].target

    def addToResult(self, cardsOut: typing.List[Card]):
        team = Team()
        team.cards = tuple(cardsOut)
        team.target = sum(self.cardData[x]['power'] for x in cardsOut)
        team.items = self.activeItems
        if team.target > self.result[-1].target:
            self.result.append(team)
            self.result.sort(key=lambda x: x.target, reverse=True)
            self.result.pop(-1)

    def postProcess(self):
        pass


if __name__ == '__main__':
    from profile_manager import Profile
    p = Profile.loadFromBestdori({"name":"Alex","server":3,"compression":"1","data":"04y0K07o0M0Bo0M2Ko0K0Vo0M0lo0M0xo0K13o0M1Jo0K1Ro0K1Zo0K1bo0M1do0M1io0M02U0G06U0G0AU0G0EU0G0IU0G2LU0G0MU0G2MU0G0QU0G0UU0G0YU0G0cU0G0gU0G0kU0G0oU0G0sU0G0wU0G0-U0G12U0G16U0G1AU0G1EU0G1IU0G1MU0G1QU0G1YU0G1eU0G1fU0G1jU0G1kU0G01K0G05K0G09K0G0DK0G0HK0G0LK0G0PK0G0TK0G0XK0G0bK0G0zK0G11K0G15K0G19K0G1DK0G1HK0G1LK0G1PK0G1TK0G1XK0G1no0K1oU0G0fK0G0jK0G0nK0G0rK0G0vK0G1qo0K1tU0G1Vo0M1pU0G1uU0G17o0M1mo0M22U0G20o0M23y0M24o0M27U0G1_o0K21U0G1xo0M1zU0G25o0M26U0G2CU0G29o0M0Fo0M2Ao0M2BU0G1cy0M2Eo0M2HU0G0to0M1No0M0po0M2QU0G2Po0M1ly1U1UU0G2Fo0M2GU0G2VU0G2Uo0M2Ny0K0_o0M1-y0M2Yo0K2bU0G1ro0M2aU0G2Zo0M2WU0G1Bo0M2gU0G2fU0G2eo0M0No0M0ho0M2do0M2jo0M2kU0G2uU0G2to0M0Gy0K03o0M2io0K2lU0G2vU0G32U0G31o0M3ao0M3bU0G33U0G1gy1s30o0M2so0M3cU0G3ko0M3lU0G3po0M3qU0G3_U003-U003zU003yU003xU002ry1s2RU0G1wy0M42o0M43U0G3mU0G2hy1q48U0G47o0M3oo0K3rU0G44U0G4Co0M4DU0G49U0G4Mo0K4NU0G4Ro0M4SU0G4Lo0K4EU0G0Ro0M4OU0G1sy0M4XU0G4Wo0M4YU0G40y0M1ho0M4Vo0M4bo0M4cU0G4dU0G0Cy144go0M4hU0G","items":{"Menu":[4,4,4,4],"Plaza":[4,4,4,4],"Roselia":[4,4,4,4,4,4,4],"Afterglow":[4,4,4,4,4,4,4],"PoppinParty":[4,4,4,4,4,4,4],"PastelPalettes":[4,4,4,4,4,4,4],"HelloHappyWorld":[4,4,4,4,4,4,4]}})
    builder = TeamBuilder()
    # x = timeit.timeit('builder.run(p.cards, p.items, Song(), 1, None, 10)', globals=globals(), number=1)
    # print(x)
    for _ in range(10):
        builder.run(p.cards, p.items, Song(), 1, None, 10)
