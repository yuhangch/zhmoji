import codecs
import json
from itertools import product
from typing import Dict, List, Set, Any

emoji_all_html = "emoji_all.html"
raw_data_path = "../json/emoji.json"
quanpin_data_path = "../json/emoji.quanpin.json"
quanpin_config_path = "../PhraseEdit.quanpin.txt"
shuangpin_data_path = "../json/emoji.shuangpin.{scheme_id}.json"
shuangpin_config_path = "../PhraseEdit.shuangpin.{scheme_id}.txt"


def write_json(file_name: str, data: Dict):
    with codecs.open(file_name, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


def word_product(word_list: List[List]) -> List:
    result: List = []
    for i in product(*word_list):
        result.append("".join(list(i)))
    return result


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
        return MS_Layout[pinyin_part]
    elif pinyin_part in "qwrtypsdfghjklzxcbnm":
        return pinyin_part
    return ""


def MSPY_final_key_parser(pinyin_part: str, bare: bool) -> str:
    if bare:
        # 微软拼音特殊规则
        if pinyin_part == "er":
            return "or"
        elif pinyin_part in "eoa":
            return "o" + pinyin_part
        return "o" + MS_Layout[pinyin_part]
    if len(pinyin_part) == 1 and pinyin_part in "euioa":
        return pinyin_part
    return MS_Layout[pinyin_part]


Xiaohe_Layout: Dict = {
    "iu": "q",
    "ei": "w",
    "uan": "r",
    "ue": "t",
    "ve": "t",
    "un": "y",
    "uo": "o",
    "ie": "p",
    "ong": "s",
    "iong": "s",
    "ai": "d",
    "en": "f",
    "eng": "g",
    "ang": "h",
    "an": "j",
    "uai": "k",
    "ing": "k",
    "uang": "l",
    "iang": "l",
    "ou": "z",
    "ua": "x",
    "ia": "x",
    "ao": "c",
    "ui": "v",
    "in": "b",
    "iao": "n",
    "ian": "m",
    "sh": "u",
    "ch": "i",
    "zh": "v",
}


def Xiaohe_initial_key_parser(pinyin_part: str) -> str:
    if len(pinyin_part) > 1:
        return Xiaohe_Layout[pinyin_part]
    elif pinyin_part in "qwrtypsdfghjklzxcbnm":
        return pinyin_part
    return ""


def Xiaohe_final_key_parser(pinyin_part: str, bare: bool) -> str:
    if bare:
        # 小鹤双拼零声母情况
        # 单字母韵母，零声母 + 韵母所在键，如： 啊＝aa 哦=oo 额=ee
        if len(pinyin_part) == 1 and pinyin_part in "euioa":
            return pinyin_part + pinyin_part
        # 双字母韵母，零声母 + 韵母末字母，如： 爱＝ai 恩=en 欧=ou
        elif len(pinyin_part) == 2:
            return pinyin_part
        # 三字母韵母，零声母 + 韵母所在键，如： 昂＝ah
        else:
            return pinyin_part[0] + Xiaohe_Layout[pinyin_part]
    if len(pinyin_part) == 1:
        return pinyin_part
    else:
        return Xiaohe_Layout[pinyin_part]


# 处理性别（男人捂脸🤦‍♀️ -> 捂脸🤦‍♀️）
def gender_special_processor(alias_set: Set[str]):
    alias_set_copy = alias_set.copy()
    keywords = word_product(
        [
            ["男", "女"],
            ["人", "生", "子"]
        ]
    ) + ["的男人", "的女人"]
    for keyword in keywords:
        for alias in alias_set:
            if keyword in alias:
                _alias = alias.replace(keyword, "")
                if len(_alias) > 0:
                    alias_set_copy.add(_alias)

    return alias_set_copy


# 处理":"
def colon_special_processor(alias_set: Set[str]):
    alias_set_copy = alias_set.copy()
    for alias in alias_set:
        if ":" in alias:
            alias_set_copy.discard(alias)
            alias_split = alias.split(":")
            if len(alias_split) != 2:
                continue
            _alias = alias_split[1].strip()
            alias_set_copy.add(_alias)
    return alias_set_copy


# 处理"｜"
def pipe_special_processor(alias_set: Set[str]):
    alias_set_copy = alias_set.copy()
    for alias in alias_set:
        if "｜" in alias:
            alias_set_copy.discard(alias)
            alias_split = alias.split("｜")
            for _alias in alias_split:
                if _alias and _alias != "":
                    alias_set_copy.add(_alias)
    return alias_set_copy


class ShuangpinScheme:
    id: str
    name: str
    layout: Dict
    initial_key_parser: Any
    final_key_parser: Any

    def __init__(self, id, name, layout, initial_key_parser, final_key_parser):
        self.id = id
        self.name = name
        self.layout = layout
        self.initial_key_parser = initial_key_parser
        self.final_key_parser = final_key_parser


# 已支持的双拼方案
shuangpin_schemes = [
    ShuangpinScheme("mspy",
                    "微软双拼",
                    MS_Layout,
                    MSPY_initial_key_parser,
                    MSPY_final_key_parser),
    ShuangpinScheme("xiaohe",
                    "小鹤双拼",
                    Xiaohe_Layout,
                    Xiaohe_initial_key_parser,
                    Xiaohe_final_key_parser),
    # TODO:其他双拼方案
]

# 特殊处理
special_processors = [
    gender_special_processor,
    colon_special_processor,
    pipe_special_processor
]
