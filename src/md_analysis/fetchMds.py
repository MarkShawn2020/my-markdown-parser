import re
import os
from typing import Iterator, List

from md_analysis.const import EXCLUDE_DIRS_PATTERN, EXCLUDE_FILES_PATTERN
from md_analysis.ds import MdItem


def yieldMds(fromDir) -> Iterator[MdItem]:
    """
    把所有md文件地址都打印出来
    """

    cnt = 0
    for root, dirs, files in os.walk(fromDir):
        dirs[:] = list(
            filter(lambda x: re.match(EXCLUDE_DIRS_PATTERN, x), dirs))

        files[:] = list(
            filter(lambda x: re.match(EXCLUDE_FILES_PATTERN, x), files))

        for file in files:
            if file.endswith(".md"):
                cnt += 1

                name = os.path.basename(
                    file if file != "readme.md" else root).strip(".md")
                path = os.path.join(root, file)
                print("parsing: ", path)
                yield MdItem(cnt=cnt, name=name, path=path)


def getMds(fromDir: str) -> List[MdItem]:
    return list(yieldMds(fromDir))
