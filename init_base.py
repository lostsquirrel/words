


import os
import xml.etree.ElementTree as ET
from datetime import datetime
from word import services as wordService

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")

def parse_wordbook(filename: str):
    keyMap = dict(
        GUID="guid",
        DisplayName="name",
        CreateTime="create_time",
        LastModifiedTime="modified_time"
    )
    tree = ET.parse(filename)
    root = tree.getroot()
    e = dict()
    for x in root:
        if x.tag in keyMap.keys():
        # print(x.tag)
            key = keyMap[x.tag]
            if key.endswith("time"):
                e[key] = parse_date(x.text)
            else:
                e[key] = x.text
    return e

def print_workbook_insert(book: dict) -> None:
    return "INSERT INTO wordbook (guid, name, create_time, modified_time) VALUES ({guid}, '{name}', '{create_time}', '{modified_time}');".format(**book)

def parse_word(filename: str):
    tree = ET.parse(filename)
    root = tree.getroot()
    guid = None
    for x in root:
        # print(x.tag)
        if x.tag =="GUID":
            guid = int(x.text)
        if x.tag == 'Words':
            for y in x:
                # print(y)
                word = [guid]
                for z in y:
                    if z.tag == "HeadWord":
                        word.append(z.text)
                        # print(z.text)
                    if z.tag == "QuickDefinition":
                        desc = z.text
                        if desc is None:
                            desc = ""
                        word.append(desc)
                    if z.tag == "Phonetic":
                        phonetic = []
                        for p in z:
                            s = []
                            for a in p:
                                if a.text is not None:
                                    s.append(a.text)
                            phonetic.append(",".join(s))
                        word.append(";".join(phonetic))

                print(word)
                wordService.saveWord(word)
                # break

if __name__ == '__main__':

    dir = "/data/backup/dict"
    books = list()
    for f in os.listdir(dir):
        if f.endswith(".txt"):
            print(f)
            # e = parse_wordbook(os.path.join(dir, f))
            # books.append(e)
            parse_word(os.path.join(dir, f))
            # break
    # books.sort(key=lambda x: int(x['guid']))
    # for x in map(print_workbook_insert, books):
    #     print(x)
    # print(books)