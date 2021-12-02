# ZHMOJI 😍
中文/拼音/双拼 >> emoji

用作搜狗拼音自定义短语，输入😄而不是图片。
## 更新
- 2021-12-02 添加`len() > 1`的emoji [issue#7](https://github.com/yuhangch/zhmoji/issues/7) ，适应多双拼方案。
- 2021-11-30 增加小鹤双拼支持，感谢 [@raawaa](https://github.com/raawaa) 。
- 2021-09-07 修复微软双拼单韵母解析错误。
## 数据
- [emojiall (2021-09-05)](https://copy.emojiall.com/zh-hans/)

## 依赖
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [pypinyin](https://github.com/mozillazg/python-pinyin)

## 使用

### 数据
- `json/emoji.json` 

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
提取自`json/emoji.json`，通过提取emoji各个alias，形成一个关键字到多个emoji的映射。
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
1. `json/emoji.quanpin.json`
2. `json/emoji.shuangpin.{scheme}.json`


### 用于搜狗拼音：
将下列文件内容拷贝到：搜狗拼音 > 高级设置 > 自定义短语 > 直接编辑配置文件。

可选：关掉搜狗输入法默认的表情、图片推荐。
#### 全拼
`PhraseEdit.quanpin.txt`

#### 双拼方案

- 微软双拼 `PhraseEdit.shuangpin.mspy.txt`
- 小鹤双拼 `PhraseEdit.shuangpin.xiaohe.txt`

#### 其他双拼方案

依赖python环境：

配置`scripts/common.py`中双拼方案配置和解析方法，例如添加小鹤双拼方案：
```
    # 布局方案
    Xiaohe_Layout = {···}
    # 声母解析器
    def Xiaohe_initial_key_parser(pinyin_part: str) -> str:
        pass
    # 韵母解析器    
    def Xiaohe_final_key_parser(pinyin_part: str) -> str:
        pass
    
    # 注册双拼方案
    shuangpin_schemes = [
    ···,
    ShuangpinScheme("xiaohe",
                    "小鹤双拼",
                    Xiaohe_Layout,
                    Xiaohe_initial_key_parser,
                    Xiaohe_final_key_parser),
    ]
```
安装依赖，执行脚本
```shell
   pip3 install -r scripts/requirements.txt
   cd scripts
   python3 generate.py
```
生成的`PhraseEdit.shuangpin.{custom-scheme}.txt`使用方法与上述相同。

## 存在的问题

- emoji在候选框无法显示时，可尝试在外观中把字体调为等线。[issue#1](https://github.com/yuhangch/zhmoji/issues/1)
- 微软双拼方案中 `;` 无法作为搜狗自定义短语的关键字，可使用全拼来曲线救国。
- 对于关键字对应过多emoji的情况，为保证正常输入，默认只保留前两个，因此对一些特殊情况需要手动配置。
```json lines
"kunchong": [ "🦋", "🐞", "🦟", "🦗"]
```
- 即使只保留两个emoji候选，加上输入法自己的推荐，有时也会影响输入，比如`you`的候选：[有，🈶，▶，￡，由]，需要在使用中自己做一些精简。