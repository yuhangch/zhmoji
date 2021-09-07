# ZHMOJI 😍
中文/拼音/双拼 >> emoji

用作搜狗拼音自定义短语，输入😄而不是图片。
## 数据
- [emojiall (2021-09-05)](https://copy.emojiall.com/zh-hans/)

## 依赖
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [pypinyin](https://github.com/mozillazg/python-pinyin)

## 使用

### 数据
- `json/data.json` 

提取自 https://copy.emojiall.com/zh-hans/ emoji数据。

包含数据、分类和分类在数据的索引。
```json lines
{
  "content": [
    {
      "alias": [
        "脸",
        "笑",
        "笑脸",
        "嘿嘿"
      ],
      "emoji": "😀",
      "name": "嘿嘿"
    },
    ···
  ],
  "index": [
    "人类和身体"
    :
    [
      111,
      247
    ],
    ···
  ]
}
```
- 拼音映射
提取自`json/data.json`，通过提取emoji各个alias，形成一个关键字到多个emoji的映射。
```json lines
{
  "a": [
    "😦",
    "😮"
  ],
  "ai": [
    "😍",
    "😥",
    "❤",
    "💓"
  ],
  ···
}
```
1. `json/quanpin.json`
2. `json/shuangpin.json`


### 用于搜狗拼音：
将下列文件内容拷贝到：搜狗拼音>高级设置>自定义短语>直接编辑配置文件。

可选：关掉搜狗输入法默认的表情、图片推荐。
#### 全拼
`PhraseEdit.quanpin.txt`

#### 微软双拼方案

`PhraseEdit.shuangpin.txt`

#### 其他双拼方案

依赖python环境：

配置`scripts/common.py`中双拼方案配置和解析方法
```
    ···
    # 修改双拼方案配置
    layout = Your_Scheme_layout
    
    # 修改声母韵母转换方法
    initial_key_parser = Your_Scheme_initial_key_parser
    final_key_parser = Your_Scheme_final_key_parser
```
安装依赖，执行脚本
```shell
   pip3 install -r scripts/requirements.txt
   python3 scripts/generate.py
```
生成的`PhraseEdit.shuangpin.txt`使用方法与上述相同。

## 存在的问题

- 使用皮肤时，emoji在候选框无法正常显示。[issue#1](https://github.com/yuhangch/zhmoji/issues/1)
- 微软双拼方案中 `;` 无法作为搜狗自定义短语的关键字，可使用全拼来曲线救国。
- 对于关键字对应过多emoji的情况，为保证正常输入，默认只保留前两个，因此对一些特殊情况需要手动配置。
```json lines
"kunchong": [ "🦋", "🐞", "🦟", "🦗"]
```