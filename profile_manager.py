# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Profile, card and items
# Date:        2019/12/16
# ==============================================

import json
import typing
from numbers import Real

import request_manager


class Card:
    RARITY_LEVEL_ATTRS_BONUS = [
        [0, 0.027741577148418566, 0.05827079766928518, 0.09157023784727926, 0.12763157919247634,
         0.16646335421245123, 0.2080467329810958, 0.2523725635815978, 0.29945970809515476, 0.3493549269647502,
         0.4019829891560635, 0.45737145350963615, 0.5155589441139967, 0.5765070194790465, 0.6401879689268755,
         0.7066399177484718, 0.77583438444173, 0.8477702087090347, 0.922495295719485, 1],
        [0, 0.017856719467337606, 0.036896819500198366, 0.05712720353262898, 0.0785481410852151,
         0.10115068684022054, 0.12493367020010375, 0.14991873595264252, 0.17609001362625878, 0.20343906942389595,
         0.23198087664087155, 0.26171208783900635, 0.2926379539012518, 0.324741136882865, 0.3580344489450513,
         0.3925231410698117, 0.4281932552740394, 0.46505212999997836, 0.5031024182461973, 0.5423349324988558,
         0.5827566752115649, 0.6243699948827242, 0.6671642798084607, 0.7111523418284023, 0.7563202420759938,
         0.802684231316528, 0.8502340870909751, 0.8989700203928614, 0.9488922676005076, 1],
        [0, 0.006579811100923505, 0.013490376941789076, 0.02072357033736649, 0.0282857469218734,
         0.036174782566627796, 0.044399557457405224, 0.0529520377427399, 0.06182744102603252, 0.07104081341142438,
         0.0805784925749624, 0.09044396348716642, 0.1006360985970335, 0.11115826738840272, 0.12201077801526514,
         0.1331914612552324, 0.14469696632024545, 0.1565321016810991, 0.16870064899154105, 0.18119441263664268,
         0.19401618052690653, 0.20716987792842392, 0.220646377954231, 0.23445670502582086, 0.24859157352745323,
         0.26305982052078125, 0.2778572809267125, 0.29297495807935886, 0.30842764497977343, 0.3242045972904203,
         0.3403108556813293, 0.3567490256479929, 0.37351842656938367, 0.3906106859938102, 0.4080321560667454,
         0.4257874104768857, 0.4438663146273812, 0.4622730945351113, 0.48101099472751, 0.5000713733964425,
         0.5277508312304107, 0.5603880999928903, 0.5979841991476733, 0.6405413574510139, 0.6880557418260439,
         0.7405268767404022, 0.7979648036251932, 0.8603540332444733, 0.9276952510130176, 1],
        [0, 0.0052137940761305835, 0.010626772033633004, 0.01625140619739073, 0.02208300765878985,
         0.028130123879720123, 0.03438591969492338, 0.040845165089679725, 0.04751431401768039, 0.05438920952360014,
         0.06146926738626297, 0.06876102000541633, 0.07625624123106317, 0.08396613839157453, 0.09187956441780568,
         0.1000002838288349, 0.1083369509623417, 0.11687849700242568, 0.12562643419463135, 0.13458349890179105,
         0.14375149230097023, 0.1531220343111895, 0.1627012369922088, 0.1724891364692424, 0.18248307296777722,
         0.19268953004894984, 0.2031038118277759, 0.2137266946705706, 0.22455873405686588, 0.23560016086505522,
         0.246845117069297, 0.2583022752066268, 0.26996585295356473, 0.2818368100569856, 0.29391689352667993,
         0.3062034732003648, 0.31870850250918314, 0.3314136656714306, 0.34432706913752, 0.35744699511750455,
         0.37077464809342076, 0.3843126970348029, 0.39805844303293897, 0.41201000405281624, 0.4261726805173379,
         0.440542342723313, 0.4551202726012628, 0.46990761662317243, 0.48490456025578976, 0.5001066997170803,
         0.5277872974717714, 0.5604260864848988, 0.5980193982337021, 0.640573453684307, 0.6880874211513187,
         0.7405574835992293, 0.7979798883017865, 0.8603639584557542, 0.927706300412736, 1]]

    def __init__(self, cardId=-1, level=1, skillLevel=1, episodes=(False, False), train=False, trainedArt=False):
        self.id: int = cardId
        self.level: int = level
        self.skillLevel: int = skillLevel
        self.episode1: bool = bool(episodes[0])
        self.episode2: bool = bool(episodes[1])
        self._train: bool = bool(train)
        self.trainedArt: bool = bool(trainedArt)

    @property
    def _info(self) -> dict:
        return _CardDataManager.getCardInfo(self.id)
        # {'characterId': 1, 'rarity': 4, 'attribute': 'powerful', 'levelLimit': 50, 'resourceSetName': 'res001004',
        #  'prefix': ['みんなで遊園地！', 'Theme Park Fun!', '大家去遊樂園！', '大家在游乐园！', '모두 함께 놀이동산!'],
        #  'releasedAt': ['1489626000000', '1489658400000', '1489629600000', '1489629600000', '1489626000000'],
        #  'skillId': 7,
        #  'type': 'permanent', 'stat': {'1': {'performance': 4032, 'technique': 3024, 'visual': 2419},
        #                                '60': {'performance': 12177, 'technique': 9132, 'visual': 7308},
        #                                'episodes': [{'performance': 250, 'technique': 250, 'visual': 250},
        #                                             {'performance': 600, 'technique': 600, 'visual': 600}],
        #                                'training': {'performance': 400, 'technique': 400, 'visual': 400}}}

    @property
    def rarity(self) -> int:
        return self._info['rarity']

    @property
    def character(self) -> int:
        return self._info['characterId']

    @property
    def band(self) -> int:
        # 0, 1, 2, 3, 4
        band = (self.character - 1) // 5
        if 0 <= band <= 4:
            return band
        return -1

    @property
    def attribute(self) -> int:
        # 0, 1, 2, 3
        attribute = self._info['attribute']
        return {
            'powerful': 0,
            'cool': 1,
            'happy': 2,
            'pure': 3,
        }.get(attribute, -1)

    @property
    def train(self) -> bool:
        rarity = self.rarity
        if rarity <= 2:
            return False
        maxLevel = rarity * 10
        if self.level == maxLevel:
            return self._train
        return self.level > maxLevel

    @train.setter
    def train(self, x: bool):
        rarity = self.rarity
        if rarity <= 2:
            x = False
        else:
            maxLevel = rarity * 10
            if self.level != maxLevel:
                x = (self.level > maxLevel)
        self._train = x

    @property
    def params(self) -> typing.Tuple[int, int, int]:
        info = self._info
        # print(info)
        level_mul = self.RARITY_LEVEL_ATTRS_BONUS[info['rarity'] - 1]
        maxLevel = len(level_mul)
        mul = level_mul[self.level - 1]
        o = info['stat']['1']
        o1 = o['performance']
        o2 = o['technique']
        o3 = o['visual']
        a = info['stat'][str(maxLevel)]
        b1 = a['performance']
        b2 = a['technique']
        b3 = a['visual']
        o1 += int((b1 - o1) * mul)
        o2 += int((b2 - o2) * mul)
        o3 += int((b3 - o3) * mul)
        if self.train:
            a = info['stat']['training']
            o1 += a['performance']
            o2 += a['technique']
            o3 += a['visual']
        if self.episode1:
            a = info['stat']['episodes'][0]
            o1 += a['performance']
            o2 += a['technique']
            o3 += a['visual']
        if self.episode2:
            a = info['stat']['episodes'][1]
            o1 += a['performance']
            o2 += a['technique']
            o3 += a['visual']
        return o1, o2, o3

    def toBestdoriCompressedV1(self):
        cardId = self.id
        if cardId >= 10000:
            cardId -= 6928
        elif cardId >= 3072:
            raise ValueError(f'Cannot encode card id: {cardId}')
        episodes = 2 if self.episode2 else 1 if self.episode1 else 0
        temp = (1 * 0 +  # exclude, always false in this case
                2 * int(self.trainedArt) +
                4 * self.train +
                8 * episodes +
                24 * (self.skillLevel - 1))
        return ''.join((
            _Base64Variant.encode(cardId, 2),
            _Base64Variant.encode(self.level, 1),
            _Base64Variant.encode(temp, 2)
        ))

    @staticmethod
    def fromBestdoriCompressedV1(s):
        assert len(s) == 5
        card = Card()
        card.id = _Base64Variant.decode(s[0:2])
        if card.id >= 3072:
            card.id += 6928
        card.level = _Base64Variant.decode(s[2:3])
        temp = _Base64Variant.decode(s[3:5])
        # exclude = bool(temp % 2)
        temp //= 2
        card.trainedArt = bool(temp % 2)
        temp //= 2
        card._train = bool(temp % 2)
        temp //= 2
        episodes = temp % 3
        card.episode1 = (episodes >= 1)
        card.episode2 = (episodes >= 2)
        temp //= 3
        card.skillLevel = temp + 1
        return card

    def __str__(self):
        try:
            trained = 'Trained' if self.train else 'Not Trained'
            rarity = self.rarity
            rarity = '★' * rarity + '☆' * (4 - rarity)
            skillLevel = self.skillLevel
            skillLevel = '12345'[:skillLevel] + ' ' * (5 - skillLevel)
            e1 = '1' if self.episode1 else ' '
            e2 = '2' if self.episode2 else ' '
            attrs = self.params
            return (f'#{self.id:4} Lv.{self.level:2} {rarity} Skl.{skillLevel} '
                    f'Epsd.{e1}{e2} Param.({attrs[0]:5}, {attrs[1]:5}, {attrs[2]:5}) {trained}')
        except KeyError:
            return 'Invalid card'

    def __repr__(self):
        return f'Card(cardId={self.id}, level={self.level}, skillLevel={self.skillLevel}, ' \
               f'episodes=({int(self.episode1)}, {int(self.episode2)}), train={int(self.train)}, ' \
               f'trainedArt={int(self.trainedArt)})'

    # def __eq__(self, other):
    #     return ((self.id, self.level, self.skillLevel, self.episode1, self.episode2, self.train)
    #             == (other.id, other.level, other.skillLevel, other.episode1, other.episode2, other.train))


class Item:
    def __init__(
            self, itemId=0,
            band=(True,) * 5,
            attribute=(True,) * 4,
            param=(True,) * 3,
            bonuses: typing.Tuple[Real, ...] = (0,),
            level=0
    ):
        self.id = itemId
        self._band = band
        self._attribute = attribute
        self._param = param
        # if band & attr match -> add param
        self._levelToBonus = bonuses
        self.level = level

    def getItemBonus(self, card: Card) -> typing.Tuple[Real, Real, Real]:
        if not (self._band[card.band] and self._attribute[card.attribute]):
            return 0, 0, 0
        bonus = self._levelToBonus[self.level]
        return tuple(bonus if param else 0. for param in self._param)

    def __str__(self):
        return f"'Item{self.id}, Lv.{self.level}'"

    def __repr__(self):
        return f"Item({self.id}, level={self.level})"

    @staticmethod
    def getDefaultItems(items, bonusType, fromBestdori=False):
        # bestdori: add 1 to levels
        # items[type][group] = list(all items in group)
        out = []

        bonus1 = (0, 2, 2.5, 3, 3.5, 4, 4.5)
        bonus1_half = (0, 1, 1.25, 1.5, 1.75, 2, 2.25)
        bonus2 = (0, 6, 7, 8, 9, 10, 11)
        bonus2_half = (0, 3, 3.5, 4, 4.5, 5, 5.5)
        band = [[(i == x) for i in range(5)] for x in range(5)]
        bandBonuses = []
        lv = items.get('PoppinParty', [0] * 7)
        if fromBestdori: lv = [_x + 1 for _x in lv]
        bandBonuses.append([
            Item(1, band=band[0], bonuses=bonus1, level=lv[0]),
            Item(6, band=band[0], bonuses=bonus1, level=lv[1]),
            Item(11, band=band[0], bonuses=bonus1, level=lv[2]),
            Item(16, band=band[0], bonuses=bonus1, level=lv[3]),
            Item(21, band=band[0], bonuses=bonus1, level=lv[4]),
            Item(26, band=band[0], bonuses=bonus2, level=lv[5]),
            Item(31, band=band[0], bonuses=bonus2, level=lv[6]),
        ])
        lv = items.get('Afterglow', [0] * 7)
        if fromBestdori: lv = [_x + 1 for _x in lv]
        bandBonuses.append([
            Item(2, band=band[1], bonuses=bonus1, level=lv[0]),
            Item(7, band=band[1], bonuses=bonus1, level=lv[1]),
            Item(12, band=band[1], bonuses=bonus1, level=lv[2]),
            Item(17, band=band[1], bonuses=bonus1, level=lv[3]),
            Item(22, band=band[1], bonuses=bonus1, level=lv[4]),
            Item(27, band=band[1], bonuses=bonus2, level=lv[5]),
            Item(32, band=band[1], bonuses=bonus2, level=lv[6]),
        ])
        lv = items.get('PastelPalettes', [0] * 7)
        if fromBestdori: lv = [_x + 1 for _x in lv]
        bandBonuses.append([
            Item(3, band=band[1], bonuses=bonus1, level=lv[0]),
            Item(8, band=band[1], bonuses=bonus1, level=lv[1]),
            Item(13, band=band[1], bonuses=bonus1, level=lv[2]),
            Item(18, band=band[1], bonuses=bonus1, level=lv[3]),
            Item(23, band=band[1], bonuses=bonus1, level=lv[4]),
            Item(28, band=band[1], bonuses=bonus2, level=lv[5]),
            Item(33, band=band[1], bonuses=bonus2, level=lv[6]),
        ])
        lv = items.get('Roselia', [0] * 7)
        if fromBestdori: lv = [_x + 1 for _x in lv]
        bandBonuses.append([
            Item(4, band=band[1], bonuses=bonus1, level=lv[0]),
            Item(9, band=band[1], bonuses=bonus1, level=lv[1]),
            Item(14, band=band[1], bonuses=bonus1, level=lv[2]),
            Item(19, band=band[1], bonuses=bonus1, level=lv[3]),
            Item(24, band=band[1], bonuses=bonus1, level=lv[4]),
            Item(29, band=band[1], bonuses=bonus2, level=lv[5]),
            Item(34, band=band[1], bonuses=bonus2, level=lv[6]),
        ])
        lv = items.get('HelloHappyWorld', [0] * 7)
        if fromBestdori: lv = [_x + 1 for _x in lv]
        bandBonuses.append([
            Item(5, band=band[1], bonuses=bonus1, level=lv[0]),
            Item(10, band=band[1], bonuses=bonus1, level=lv[1]),
            Item(15, band=band[1], bonuses=bonus1, level=lv[2]),
            Item(20, band=band[1], bonuses=bonus1, level=lv[3]),
            Item(25, band=band[1], bonuses=bonus1, level=lv[4]),
            Item(30, band=band[1], bonuses=bonus2, level=lv[5]),
            Item(35, band=band[1], bonuses=bonus2, level=lv[6]),
        ])
        lv = items.get('Everyone', None)
        if lv is not None:
            if fromBestdori: lv = [_x + 1 for _x in lv]
            bandBonuses.append([
                Item(73, bonuses=bonus1_half, level=lv[0]),
                Item(74, bonuses=bonus1_half, level=lv[1]),
                Item(75, bonuses=bonus1_half, level=lv[2]),
                Item(76, bonuses=bonus1_half, level=lv[3]),
                Item(77, bonuses=bonus1_half, level=lv[4]),
                Item(78, bonuses=bonus2_half, level=lv[5]),
                Item(79, bonuses=bonus2_half, level=lv[6]),
            ])
        out.append(bandBonuses)

        if bonusType == 1:
            bonus3 = (0, 1, 3, 5, 7, 10)
            bonus3_half = (0, 0.5, 1.5, 2.5, 3.5, 5)
        elif bonusType == 2:
            bonus3 = (0, 2, 4, 6, 8, 10, 12)
            bonus3_half = (0, 1, 2, 3, 4, 5, 6)
        else:
            raise ValueError(f'Bonus type: {bonusType}')
        attr = [[(i == x) for i in range(4)] for x in range(4)]
        attributeBonuses = []
        menu = items.get('Menu', [0] * 4)
        plaza = items.get('Plaza', [0] * 4)
        if fromBestdori:
            menu = [_x + 1 for _x in menu]
            plaza = [_x + 1 for _x in plaza]
        attributeBonuses.append([
            Item(56, attribute=attr[0], bonuses=bonus3, level=menu[0]),
            Item(70, attribute=attr[0], bonuses=bonus3, level=plaza[0]),
        ])
        attributeBonuses.append([
            Item(57, attribute=attr[1], bonuses=bonus3, level=menu[0]),
            Item(66, attribute=attr[1], bonuses=bonus3, level=plaza[0]),
        ])
        attributeBonuses.append([
            Item(58, attribute=attr[2], bonuses=bonus3, level=menu[0]),
            Item(67, attribute=attr[2], bonuses=bonus3, level=plaza[0]),
        ])
        attributeBonuses.append([
            Item(60, attribute=attr[3], bonuses=bonus3, level=menu[0]),
            Item(69, attribute=attr[3], bonuses=bonus3, level=plaza[0]),
        ])
        if len(menu) >= 5 and len(plaza) >= 5 and menu[5] and plaza[5]:
            attributeBonuses.append([
                Item(61, bonuses=bonus3_half, level=menu[5]),
                Item(71, bonuses=bonus3_half, level=plaza[5]),
            ])
        out.append(attributeBonuses)

        bonus4 = (0, 8, 10, 12, 14, 16)
        param = [[(i == x) for i in range(3)] for x in range(3)]
        magazine = items.get('Magazine', None)
        if magazine is not None:
            if fromBestdori: magazine = [_x + 1 for _x in magazine]
            if sum(magazine) != 0:
                magazineBonuses = [
                    [
                        Item(80, param=param[0], bonuses=bonus4, level=magazine[0])
                    ], [
                        Item(81, param=param[1], bonuses=bonus4, level=magazine[1])
                    ], [
                        Item(82, param=param[2], bonuses=bonus4, level=magazine[2])
                    ]
                ]
                out.append(magazineBonuses)

        return out


class Profile:
    def __init__(self, name=None, server=3):
        self.name = name
        self.server = server
        self.cards: typing.List[Card] = []
        self.items: typing.List[typing.List[Item]] = []

    @staticmethod
    def loadFromBestdori(data: dict):
        name = data['name']
        server = data['server']
        p = Profile(name, server)
        compression = data.get('compression')
        if compression != '1':
            raise ValueError(f'Unsupported compression level {compression}')
        cardData = data['data']
        for i in range(0, len(cardData), 5):
            card = Card.fromBestdoriCompressedV1(cardData[i:i + 5])
            p.cards.append(card)
        bonusType = 2 if server in (0, 2) else 1  # TODO temporary solution
        items = data['items']
        p.items = Item.getDefaultItems(items, bonusType, fromBestdori=True)
        return p

    def __str__(self):
        return f'Profile {self.name} (Server {self.server}), {len(self.cards)} card(s)'

    def __repr__(self):
        cards = ',\n  '.join(repr(x) for x in self.cards)
        items = '],\n  ['.join((',\n   '.join(repr(y) for y in x) for x in self.items))
        return (
            f"Profile({self.name!r}, server={self.server}) {{\n"
            f"'cards': [\n  {cards}],\n"
            f"'items': [\n  [{items}]]}}"
        )


class _Base64Variant:
    TABLE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'

    @classmethod
    def decode(cls, s: str) -> int:
        out = 0
        for ch in s:
            i = cls.TABLE.index(ch)
            out = out * 64 + i
        return out

    @classmethod
    def encode(cls, num: int, digit: int) -> str:
        out = []
        for i in range(digit):
            out.append(cls.TABLE[num % 64])
            num //= 64
        return ''.join(reversed(out))


class _CardDataManager:
    DATA_URL = 'https://bestdori.com/api/cards/all.5.json'
    DATA = {}
    INITIALIZED = False

    @classmethod
    def getCardInfo(cls, cardId):
        if not cls.INITIALIZED:
            cls.update()
        return cls.DATA.get(cardId, {})

    @classmethod
    def update(cls, force=False):
        manager = request_manager.getManager()
        d = manager.get(cls.DATA_URL, force=force)
        j = json.loads(d)
        data = {}
        for cardId_s in j:
            info = j[cardId_s]
            cardId = int(cardId_s)
            data[cardId] = info
        cls.DATA = data
        cls.INITIALIZED = True


if __name__ == '__main__':
    d = {"name": "Alex", "server": 3, "compression": "1",
         "data": "04y0K07o0M0Bo0M2Ko0K",
         "items": {"Menu": [4, 4, 4, 4], "Plaza": [4, 4, 4, 4], "Roselia": [4, 4, 4, 4, 4, 4, 4],
                   "Afterglow": [4, 4, 4, 4, 4, 4, 4], "PoppinParty": [4, 4, 4, 4, 4, 4, 4],
                   "PastelPalettes": [4, 4, 4, 4, 4, 4, 4], "HelloHappyWorld": [4, 4, 4, 4, 4, 4, 4]}}
    _profile = Profile.loadFromBestdori(d)
    print(repr(_profile))
    print(_profile)
