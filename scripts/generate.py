from emoji_all_parser import write_emoji_json
from sogou_config import write_config
from translate_pinyin import write_shuangpin_json, write_quanpin_json
from common import shuangpin_schemes, emoji_all_html, raw_data_path, quanpin_data_path, quanpin_config_path, \
    shuangpin_data_path, shuangpin_config_path

if __name__ == '__main__':
    # 解析、生成emoji数据
    write_emoji_json(emoji_all_html, raw_data_path)
    # 全拼 -> emoji
    write_quanpin_json(quanpin_data_path)
    # 生成全拼方案 PhraseEdit
    write_config(quanpin_data_path, quanpin_config_path)

    for scheme in shuangpin_schemes:
        _data_path = shuangpin_data_path.format(scheme_id=scheme.id)
        _config_path = shuangpin_config_path.format(scheme_id=scheme.id)

        # 双拼方案 -> emoji
        write_shuangpin_json(scheme, _data_path)
        # 生成双拼方案 PhraseEdit
        write_config(_data_path, _config_path)
