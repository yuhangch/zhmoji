import re
from typing import List, Dict

from bs4 import BeautifulSoup
from bs4.element import Tag

from common import write_json


def write_emoji_json(emoji_all: str, output: str):
    soup = BeautifulSoup(open(emoji_all, 'r', encoding='utf-8'), 'html.parser')

    emoji_list: List = []
    category_index: Dict = {}

    sections = soup.findAll("section", {
        "class": re.compile("emoji_card_list")
    })
    count = 0
    for section in sections:
        _count = 0
        section_strings = []
        for c in section.h2.strings:
            section_strings += [c]

        section_strings = [s.strip() for s in section_strings if s != "\n"]
        category_title = section_strings[1]

        section_emojis = section.ul

        for emoji_tag in section_emojis:
            e: dict = {}
            # print(type(emoji))
            if type(emoji_tag) == Tag:
                ok: Tag = emoji_tag
                info_div = emoji_tag.div
                info = [i for i in info_div.strings if i != "\n"]
                e['name'] = info[1]

                alias_raw: str = ok.attrs['data-keyword']
                alias = re.split("[|^]", alias_raw)
                emoji = alias[0]
                alias = list(filter(None, alias[1:]))

                e['emoji'] = emoji
                e['alias'] = list(set(alias))

                if len(emoji) > 0:
                    emoji_list += [e]
                    _count += 1
                    count += 1
        category_index[category_title] = [count - _count, count]
        print(f"[{category_title}]：{_count}")
    print(f"总计：{count}")

    json_data = {
        # 每个分类对应的位置
        "index": category_index,
        # emoji 数据
        "content": emoji_list
    }

    write_json(output, json_data)
