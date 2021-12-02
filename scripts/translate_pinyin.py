import json
from collections import defaultdict
from typing import List
from pypinyin import pinyin, NORMAL, INITIALS, FINALS
from common import write_json, word_product, ShuangpinScheme
from common import raw_data_path


# 全拼转换
def quanpin_of(pinyin_str: str) -> str:
    pinyin_list = list(pinyin(pinyin_str, style=NORMAL, heteronym=True))
    pinyin_result = word_product(pinyin_list)
    return "".join(pinyin_result[0])


# 双拼转换
def shuangpin_of(pinyin_str: str, scheme: ShuangpinScheme) -> str:
    pinyin_list_initials = list(pinyin(pinyin_str, style=INITIALS, strict=False))
    pinyin_list_finals = list(pinyin(pinyin_str, style=FINALS, strict=False))
    initials = [scheme.initial_key_parser(i[0]) for i in pinyin_list_initials]
    # 声母是否存在
    is_bare = [len(i) < 1 for i in initials]
    finals = [scheme.final_key_parser(pinyin_list_finals[i][0], is_bare[i]) for i in range(len(initials))]
    result = list(map(lambda x: x[0] + x[1], zip(initials, finals)))
    return "".join(result)


# https://segmentfault.com/a/1190000017940752
# 判断字符串是否全为中文
def is_all_chinese(word: str) -> bool:
    for _char in word:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def _translate(output: str, pinyin_parser, scheme: ShuangpinScheme = None) -> int:
    pinyin_keys = defaultdict(list)
    with open(raw_data_path, "r", encoding="utf-8") as d:
        raw_data = json.load(d)

    del raw_data['index']
    _count: int = 0
    for emoji_item in raw_data["content"]:
        emoji = emoji_item['emoji']
        alias_list: List[str] = emoji_item['alias']
        for alias in alias_list:
            if alias == "":
                continue
            # 如果全是英文直接返回
            if all(c.isascii() and c.isalpha() for c in alias):
                pinyin_keys[alias].append(emoji)
            # 如果不全是中文，例如（6:00），忽略
            if not all(is_all_chinese(c) for c in alias):
                continue
            # scheme不为空，解析双拼，需指定scheme
            if scheme:
                alias_pinyin = pinyin_parser(alias, scheme)
            else:
                alias_pinyin = pinyin_parser(alias)
            pinyin_keys[alias_pinyin].append(emoji)
            _count += 1
    write_json(output, pinyin_keys)
    return _count


def write_quanpin_json(output: str):
    _count = _translate(output, quanpin_of)
    print(f"生成全拼关键字{_count}。")


def write_shuangpin_json(scheme: ShuangpinScheme, output: str):
    _count = _translate(output, shuangpin_of, scheme)
    print(f"生成{scheme.name}关键字{_count}。")
