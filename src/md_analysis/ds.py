from __future__ import annotations
from typing import TypedDict, Optional, List


class MdItem(TypedDict):
    cnt: Optional[int]
    name: str
    path: str


class TocItem(TypedDict):
    level: int
    title: str
    fa: Optional[TocItem]
    children: List[TocItem]  # add children for post-process
