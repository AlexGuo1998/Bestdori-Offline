# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Song manager, score calculation, etc
# Date:        2019/12/19
# ==============================================

import typing
import json

from request_manager import getManager


class SongNote:
    def __init__(self, time, isSkill, isFever):
        self.time: float = time
        self.skill: bool = isSkill
        self.fever: bool = isFever


class Song:
    DIFFICULTY_STR = ('easy', 'normal', 'hard', 'expert', 'special')
    NOTES_SIMPLE_URL = 'https://bestdori.com/api/songs/chart/notes/simple/{}.{}.json'

    def __init__(self):
        self.id = 0
        self.difficulty = 0
        self.playLevel = 0
        self._notes = None
        self._graphics = None

    @property
    def notes(self):
        if self._notes is None:
            # populate
            manager = getManager()
            s = manager.get(self.NOTES_SIMPLE_URL.format(self.id, self.DIFFICULTY_STR[self.difficulty]))
            j = json.loads(s)
            self._notes = []
            for n in j:
                note = SongNote(n['time'], n.get('skill', False), n.get('fever', False))
                self._notes.append(note)
        return self._notes

    def freeCache(self):
        self._notes = None
        self._graphics = None


class SongMeta:
    def __init__(self):
        self.songId = 0
        self.data = {}
        self.songs: typing.Dict[int, Song] = {}

    @property
    def difficulties(self) -> typing.Set[int]:
        return set(self.songs.keys())

    @staticmethod
    def loadFromBestdori(songId, data):
        meta = SongMeta()
        meta.songId = songId
        meta.data = data
        for difficulty_s in data['difficulty']:
            difficulty = int(difficulty_s)
            song = Song()
            song.id = songId
            song.difficulty = difficulty
            song.playLevel = data['difficulty'][difficulty_s]['playLevel']
            meta.songs[difficulty] = song
        return meta

    def __getitem__(self, difficulty):
        return self.songs[difficulty]


class SongManager:
    META_URL = 'https://bestdori.com/api/songs/all.7.json'
    DATA: typing.Mapping[int, SongMeta] = {}
    INITIALIZED = False

    @classmethod
    def getSongList(cls):
        if not cls.INITIALIZED:
            cls.updateMeta()
        return list(cls.DATA.keys())

    @classmethod
    def getSongMeta(cls, songId):
        if not cls.INITIALIZED:
            cls.updateMeta()
        return cls.DATA[songId]

    @classmethod
    def updateMeta(cls, force=False):
        manager = getManager()
        d = manager.get(cls.META_URL, forceReload=force)
        j = json.loads(d)
        data = {}
        for songId_s in j:
            info = j[songId_s]
            songId = int(songId_s)
            meta = SongMeta.loadFromBestdori(songId, info)
            data[songId] = meta
        cls.DATA = data
        cls.INITIALIZED = True
        pass

    @classmethod
    def cacheAllSongs(cls, difficulty=None):
        if difficulty is None:
            difficulty = {0, 1, 2, 3, 4}
        if not cls.INITIALIZED:
            cls.updateMeta()
        for songId in cls.DATA:
            print(songId)
            meta = cls.DATA[songId]
            for d in meta.difficulties.intersection(difficulty):
                _ = meta[d].notes
                meta[d].freeCache()


if __name__ == '__main__':
    try:
        SongManager.updateMeta()
        SongManager.cacheAllSongs()
    finally:
        getManager().saveCacheIndex()
