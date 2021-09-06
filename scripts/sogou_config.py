import json
import os


def write_config(data:str, output:str):
    with open(data, "r", encoding="utf-8") as d:
        raw_data = json.load(d)
    with open(output, 'w',encoding="utf-8") as o:
        for k in raw_data:
            emojis = raw_data[k]
            o.write(f"{k},2={emojis[0]}\n")
            if len(emojis)>1:
                o.write(f"{k},3={emojis[1]}\n")




