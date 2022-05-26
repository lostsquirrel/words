import unittest
from word import services as wordService
from word.models import wordDAO


def rebuild_phonetic(_ps):
    psx = []
    for pe in _ps:
        si = pe.rfind(",")
        if si != -1:
            pp = "__".join([pe[:si], pe[si+1:]])
            psx.append(pp)
    return psx


class WordServicesTest(unittest.TestCase):

    def test_word(self):
        page = 1
        guid = 1011
        while True:
            words = wordService.get_world_by_book(guid, page, 10)
            if len(words.list) == 0:
                break
            page += 1
            print(page)

    def test_fix_phonetic(self):
        guid = 1011
        offset = 0
        while True:
            ws = wordDAO.find_by_book(guid, 10, offset)
            if len(ws) == 0:
                break
            for w in ws:
                ps = w[3]
                _ps = ps.split(";")
                psx = self.rebuild_phonetic(_ps)
                pn = ";".join(psx)
                if p.find("_") != -1:
                    print(x)

    def test_sx(self):

        s = ("12,3,456", "678,0000")
        sx = rebuild_phonetic(s)
        print(sx)
