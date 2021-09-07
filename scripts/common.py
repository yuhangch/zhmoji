import codecs
import json
from typing import Dict


def write_json(file_name: str, data: Dict):
    with codecs.open(file_name, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

# 微软拼音配置
MS_Layout: Dict = {
    "zh": "v",
    "ch": "i",
    "sh": "u",
    "ai": "l",
    "an": "j",
    "ang": "h",
    "ao": "k",
    "ei": "z",
    "en": "f",
    "eng": "g",
    "er": "or",
    "ia": "w",
    "ian": "m",
    "iang": "d",
    "iao": "c",
    "ie": "x",
    "in": "n",
    "ing": ";",
    "iong": "s",
    "iu": "q",
    "ong": "s",
    "ou": "b",
    "ua": "w",
    "uai": "y",
    "uan": "r",
    "uang": "d",
    "ue": "t",
    "ui": "v",
    "un": "p",
    "uo": "o",
    "v": "y",
    "ve": "v",
    # direct initial
    # qwrtypsdfghjklzxcbnm
    # direct final
    # euioa

}


def MSPY_initial_key_parser(pinyin_part: str) -> str:
    if len(pinyin_part) > 1:
        return layout[pinyin_part]
    elif pinyin_part in "qwrtypsdfghjklzxcbnm":
        return pinyin_part
    return ""


def MSPY_final_key_parser(pinyin_part: str, bare: bool) -> str:
    if bare:
        # 微软拼音特殊规则
        print(pinyin_part)
        if pinyin_part == "er":
            return "or"
        elif pinyin_part in "eoa":
            return "o" + pinyin_part
        return "o" + layout[pinyin_part]
    if len(pinyin_part) == 1 and pinyin_part in "euioa":
        return pinyin_part
    return layout[pinyin_part]


# 修改键盘配置
layout = MS_Layout
# 修改声母韵母转换方法
initial_key_parser = MSPY_initial_key_parser
final_key_parser = MSPY_final_key_parser
