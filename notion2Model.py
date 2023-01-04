#!/usr/bin/env python3

import pandas
from pathlib import Path
from abc import ABC, abstractmethod
import re
from collections import namedtuple
from typing import Union


PageKey = namedtuple("PageKey", "name id")

def make_key(name: str) -> PageKey:
    match = re.match(r"(.*) (\S*)$", name)
    if not match or not match.group(1) or not match.group(2):
        raise Exception("Folder or page naming schema invalid, should be tile + id:" + name)
    return PageKey(match.group(1), match.group(2))

class NotionModel:
    def __init__(self) -> None:
        # self.model = {}
        self.all_pages = {}

    def add(self, node: PageKey, key: Union[PageKey, str], val=None) -> None:
        if node not in self.all_pages:
            self.all_pages[node] = {}
        if type(key) == PageKey and key not in self.all_pages:
            self.all_pages[key] = {}
            self.all_pages[node][key] = self.all_pages[key]

        if val:
            self.all_pages[node][key] = val

    def __str__(self) -> str:
        printstr = "COUNT: {}\n\n".format(len(self.all_pages))

        def subprint(vals, lvl):
            printstr2 = ""
            for n in vals:
                if type(vals[n]) == dict:
                    printstr2 += "{}{}: {}\n".format("\t"*lvl, n, len(vals[n]))
                    printstr2 += subprint(vals[n], lvl + 1)
                else:
                    printstr2 += "{}{}: {}\n".format("\t"*lvl, n, vals[n])
            return printstr2

        for n in self.all_pages:
            printstr += str(n) + ": " + str(len(self.all_pages[n])) + "\n"
            printstr += subprint(self.all_pages[n], 1)
        return printstr


class ToModel(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.model = NotionModel()
        pass

    @staticmethod
    def validate_path(path: Path) -> bool:
        if not path.exists() or not path.is_dir():
            raise Exception("The given folder path {} doesn't exist".format(path))
        return True

    @abstractmethod
    def parse(self) -> object:
        pass


class MdCsv2Model(ToModel):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

    def parse(self) -> NotionModel:
        self.subparse(self.path)
        print(self.model)
        return self.model

    def subparse(self, subpath) -> None:
        node = make_key(subpath.stem)
        for f in subpath.iterdir():
            keyname = make_key(f.stem)
            if f.is_dir():
                self.model.add(node,keyname )
                self.subparse(f)
            elif f.suffix == ".md":
                self.model.add(node, keyname)
                self.model.add(keyname, "md", f)
            elif f.suffix == ".csv":
                self.model.add(node, keyname)
                self.model.add(keyname, "csv", f)







