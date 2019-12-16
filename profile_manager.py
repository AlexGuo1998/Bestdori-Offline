# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Profile, card and items
# Date:        2019/12/16
# ==============================================

import base64
import request_manager


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


class Card:
    def __init__(self):
        self.id = -1
        self.level = 1
        self.skillLevel = 1
        self.episode1 = False
        self.episode2 = False
        self.trainedArt = False
        self._train = False

    @property
    def rarity(self):
        # TODO
        return 1

    @property
    def train(self):
        rarity = self.rarity
        if rarity <= 2:
            return False
        maxLevel = rarity * 10
        if self.level == maxLevel:
            return self._train
        return self.level > maxLevel

    def toBestdoriCompressedV1(self):
        cardId = card.id
        if cardId >= 10000:
            cardId -= 6928
        elif cardId >= 3072:
            raise ValueError(f'Cannot encode card id: {cardId}')
        episodes = 2 if self.episode2 else 1 if self.episode1 else 0
        temp = (
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

    def __repr__(self):
        trained = 'Trained' if self.train else 'Not Trained'
        skillLevel = str(self.skillLevel) if self.skillLevel > 1 else ' '
        e1 = '√' if self.episode1 else '×'
        e2 = '√' if self.episode2 else '×'
        return (f'#{self.id:4} Lv.{self.level:2} SkillLv.{skillLevel} '
                f'Episodes:{e1}{e2} {trained}')


class Profile:
    pass


if __name__ == '__main__':
    data = '04y0K07o0M0Bo0M2Ko0K'
    o = []
    for i in range(0, len(data), 5):
        card = Card.fromBestdoriCompressedV1(data[i:i + 5])
        print(card)
        o.append(card.toBestdoriCompressedV1())
    print('Check: ' + str(''.join(o) == data))
