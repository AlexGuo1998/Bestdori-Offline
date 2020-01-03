# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Recognize & match card
# Date:        2020/1/2
# ==============================================
import math
import json
import typing

from PIL import Image
from request_manager import getManager


class CardRecognizer:
    HASH_URL = 'https://bestdori.com/api/hash/all.json'
    HASHTABLE: typing.Dict[tuple, int] = {}
    INITIALIZED = False
    DCT_TABLE = None

    @classmethod
    def updateHash(cls, force=False):
        manager = getManager()
        d = manager.get(cls.HASH_URL, forceReload=force)
        j = json.loads(d)
        data = {}
        for hashStr in j:
            cardId = j[hashStr]
            h = cls.stringToHash(hashStr)
            data[h] = int(cardId)
        cls.HASHTABLE = data
        cls.INITIALIZED = True

    @classmethod
    def stringToHash(cls, s):
        assert len(s) == 16
        o = []
        for ch in s:
            i = int(ch, 16)
            o.append(bool(i & 8))
            o.append(bool(i & 4))
            o.append(bool(i & 2))
            o.append(bool(i & 1))
        return tuple(o)

    @classmethod
    def freeCache(cls):
        cls.DCT_TABLE = None

    @classmethod
    def recognize(cls, img: Image.Image, limit=5, minMatch=32):
        h = cls.hashImage(img)
        ids = cls.matchHash(h, minMatch)
        return ids[:limit]

    @classmethod
    def hashImage(cls, img: Image.Image):
        # resize image
        size = (32, 32)
        w1 = img.width / 4
        h1 = img.height / 4
        box = (w1, h1, w1 * 3, h1 * 3)
        img = img.resize(size, Image.LANCZOS, box)
        # img = img.resize(size, box=box)
        img = img.convert('L')  # grey

        # cache table
        if cls.DCT_TABLE is None:
            # we only need dist[1 .. 8]
            # table[destination - 1][source] = mul
            pi_64 = math.pi / 64
            cls.DCT_TABLE = [[math.cos(pi_64 * src * dst) for src in range(1, 65, 2)]
                             for dst in range(1, 9)]

        # DCT
        data = list(img.getdata())
        out = []
        for y_d in range(8):  # 1..8 - 1
            t_y = cls.DCT_TABLE[y_d]
            for x_d in range(8):  # 1..8 - 1
                t_x = cls.DCT_TABLE[x_d]
                o = 0.
                for y in range(32):
                    for x in range(32):
                        o += t_y[y] * t_x[x] * data[32 * y + x]
                # 1 / sqrt(2) omitted, for row 1 not used
                # div 4 omitted, for not using absolute value
                out.append(o)

        medium = sorted(out)[32]
        out = tuple(x > medium for x in out)
        return out

    @classmethod
    def matchHash(cls, h, minMatch):
        if not cls.INITIALIZED:
            cls.updateHash()
        result = []
        for h_match in cls.HASHTABLE:
            matchCount = 0
            for i in range(64):
                if h[i] == h_match[i]:
                    matchCount += 1
            if matchCount < minMatch:
                continue
            result.append((matchCount, cls.HASHTABLE[h_match]))
        result.sort(reverse=True)
        return [cardId for count, cardId in result]


if __name__ == '__main__':
    img_orig = Image.open('test.png')
    img_crop = img_orig.crop((147, 428, 381, 662))
    x = CardRecognizer.recognize(img_crop)
    print(x)
    # assert x[0] == 301
