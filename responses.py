import os
from random import choice, randint
import urllib.request

try:
    url = "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"
    response = urllib.request.urlopen(url)
    word_list = response.read().decode('utf8')
except Exception as e:
    print(e)

word_list = str(word_list).split("\n")
word_list = word_list[1:-1]

def contain_unappropriate(txt: str) -> bool:
    if any(word in txt for word in word_list):
        return True
    return False

def get_response(user_input: str, username: str) -> str:
    dialogues = {
    "hello" : [f"Hi, {username} I'm Puping's Wife. I only love Puping."],
    "hi" : [f"Hi, {username} I'm Puping's Wife. I only love Puping."],
    "how are you" : [f"I'm fine, How bout you?"],
    "fine" : [f"nice to hear that ! my husband <3"],
    "roll dice" : [f"you've rolled {randint(0,6)}"],
    "love puping" : [
            "I love him too, wanna be his second wife? 😳",
            "ควย ไอ่เหี้ย จะแย่งผัวกุหรอไอ่สาด 😡",
            "... But I love you. 😳"
        ],
    "puping narak" : [f"narak jing jing"],
    "love you" : [f"Aw so sweet.., But I only love Puping..."],
    "kuy" : [f"kuay rai sus"],
    "ควย" : [f"ควยไรสัด"],
    "hee" : ["hee pong", "hee ban mueng di"],
    "หี" : [f"หีพ่อง", "หีบ้านมึงดิ"],
    "เย็ด" : ["ไปเย็ดหมอนที่บ้านมึงนู่น","อย่ามาพูดจาลามก"]
    }

    lowered: str = user_input.lower()
    if contain_unappropriate(lowered):
        return "Pervert. Please don't speak with unappropriate word or I will ban you."
    else:
        for key in dialogues.keys():
            if key in lowered:
                return choice(dialogues[key])
            
        return "What are you talking about? I don't get it..."
    