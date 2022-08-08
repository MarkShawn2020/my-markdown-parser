import json

import yaml


def calc_words(fp: str) -> int:
    with open(fp) as f:
        return f.read().__len__()


def dump(items, fp, format="json"):
    if format == "json":
        json.dump(items, open(fp, 'w'), ensure_ascii=False, indent=2)
    elif format == "yaml":
        yaml.dump(items, open(fp, 'w'), encoding='UTF-8', allow_unicode=True, indent=2)
    else:
        raise ValueError