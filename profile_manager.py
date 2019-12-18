# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Profile, card and items
# Date:        2019/12/16
# ==============================================

import json
import typing

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

    @property
    def rarity(self) -> int:
        return self._info['rarity']

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
    def attrs(self) -> typing.Tuple[int, int, int]:
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
        cardId = _card.id
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
            skillLevel = 'x' * skillLevel + ' ' * (5 - skillLevel)
            e1 = '√' if self.episode1 else '×'
            e2 = '√' if self.episode2 else '×'
            attrs = self.attrs
            return (f'#{self.id:4} Lv.{self.level:2} {rarity} Skl.{skillLevel} '
                    f'Episodes:{e1}{e2} ({attrs[0]:5}, {attrs[1]:5}, {attrs[2]:5}) {trained}')
        except KeyError:
            return 'Invalid card'

    # def __repr__(self):
    #     return f'Card(cardId={self.id}, level={self.level}, skillLevel={self.skillLevel}, ' \
    #            f'episodes=({int(self.episode1)}, {int(self.episode2)}), train={int(self.train)}, ' \
    #            f'trainArt={int(self.trainedArt)})'


class Profile:
    pass


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
    _data = '04y0K07o0M0Bo0M2Ko0K'
    _o = []
    for _i in range(0, len(_data), 5):
        _card = Card.fromBestdoriCompressedV1(_data[_i:_i + 5])
        print(_card)
        # print(repr(_card))
        _o.append(_card.toBestdoriCompressedV1())
    print('Check: ' + str(''.join(_o) == _data))

# if __name__ == '__main__':
#     _card = Card.fromBestdoriCompressedV1('04y0K')
#     print(_card)
#     request_manager.getManager().saveCacheIndex()
