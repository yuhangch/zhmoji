from scripts.emoji_all_parser import write_emoji_json
from scripts.sogou_config import write_config
from scripts.translate_pinyin import write_shuangpin_json, write_quanpin_json
emoji_all_html = "emoji_all.html"
raw_data_path = "../json/data.json"
quanpin_data_path = "../json/quanpin.json"
shuangpin_data_path = "../json/shuangpin.json"
quanpin_config_path = "../PhraseEdit.quanpin.txt"
shuangpin_config_path = "../PhraseEdit.shuangpin.txt"

if __name__ == '__main__':
    # write emoji data
    write_emoji_json(emoji_all_html,raw_data_path)
    # pinyin -> emoji
    write_quanpin_json(quanpin_data_path)
    write_shuangpin_json(shuangpin_data_path)
    # write sogou config
    write_config(quanpin_data_path,quanpin_config_path)
    write_config(shuangpin_data_path,shuangpin_config_path)
