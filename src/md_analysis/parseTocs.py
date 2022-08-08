from __future__ import annotations
import os
import re
from typing import List, Union
from pprint import pprint

from termcolor import colored

from md_analysis.config import WITH_WORDS, WITH_SEQ
from md_analysis.const import DEV
from md_analysis.ds import TocItem
from md_analysis.fetchMds import yieldMds
from md_analysis.utils import calc_words


def dropTocLevel(toc: TocItem) -> Union[dict, str]:
    if toc['children']:
        return {toc['title']: [dropTocLevel(i) for i in toc['children']]}
    else:
        return toc['title']


def parseTocsFromLines(s: List[str], title: str = ''):
    toc_tree = TocItem(level=1, title=title, children=[], fa=None)
    cur: TocItem = toc_tree
    is_blocking = False

    def add_toc_item(new: TocItem):
        nonlocal cur
        # business readability > coding readability > efficiency
        if (new['level'] > cur['level'] + 1):
            pprint({"new": new, "cur": cur})
            raise Exception('should new heading not too big')

        if cur['level'] == new['level'] == 1:
            # TODO: check the consistency between filename with h1
            # assert cur['title'] == new['title'], "should h1 equal to filename"
            cur['title'] = new['title']
            return

        assert 'children' in cur, "should children not None"
        if new['level'] > cur['level']:
            new['fa'] = cur
            cur['children'].append(new)
            cur = new
        else:
            assert cur["fa"], 'should fa not None'
            add_toc_item(new)

    for line in s:
        # suppress code block
        if re.match(r'^```', line):
            is_blocking = not is_blocking
        if is_blocking:
            continue

        line_level_match = re.match(r'^(\s*#+\s*)(.*?)$', line)
        if line_level_match != None:
            level_s, title = line_level_match.groups()
            assert re.match(
                r'^#+ $', level_s), f"should line starswith (^#+ $), line: [{line}], matched: [{level_s}]"

            level = level_s.strip().__len__()
            # print({"level": level, "title": title})
            add_toc_item(TocItem(title=title, level=level, children=[], fa=None))

        assert not is_blocking, f"should not blocking now: [{title}]"

        while cur["fa"]:
            cur = cur.pop('fa')
        return toc_tree


def parseTocsFromFile(fp: str, with_level=False) -> dict:
    print(f'parsing: {fp}')
    fn = os.path.basename(fp).strip(".md")
    with open(fp) as f:
        toc_with_level = parseTocsFromLines(f.readlines(), fn)
        if with_level:
            return dict(toc_with_level)

        toc_without_level = dropTocLevel(toc_with_level)

        # IMPROVE: support only one `#` in file
        if isinstance(toc_without_level, str):
            toc_without_level = {toc_without_level: toc_without_level}

        return toc_without_level


def parseTocsFromDir(fromDir):
    seq = 0
    words = 0
    items = {}

    for item in yieldMds(fromDir):
        seq += 1
        toc_item = list(parseTocsFromFile(item['path']).items())
        assert toc_item.__len__() == 1, "should only one h1"
        (k, v) = toc_item[0]
        assert k not in items, f"should {k} not in items before"

        word = calc_words(item['path'])
        words += word
        if DEV:
            k = item['path'][fromDir.__len__() + 1:]
        if WITH_WORDS:
            k += f"({word})"
        if WITH_SEQ:
            k = f"{seq:03}. {k}"
        items[k] = v

    # pprint(items)
    print(colored(f'articles: {seq}, words: {words}', 'green'))
