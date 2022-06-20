import time
start = time.time()

import g2pk
g2p = g2pk.G2p()
import re
import sys
# import os
# import IPython

from fastapi import FastAPI
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware

# 🚨
#print("🚨 module path🚨")
#for i in sys.path:
#   print(i)
#print("\n")
# 🚨

start_synthesizer = time.time()
from TTS.utils.synthesizer import Synthesizer

def normalize_text(text):
    text = text.strip()

    for c in ",;:":
        text = text.replace(c, ".")
    # text = remove_duplicated_punctuations(text)

    text = jamo_text(text)
    
    # g2p 안쓰면 이부분을 주석하세요
    init_g2pk_time = time.time()
    
    text = g2p.idioms(text)
    text = g2pk.english.convert_eng(text, g2p.cmu)
    text = g2pk.utils.annotate(text, g2p.mecab)
    text = g2pk.numerals.convert_num(text)
    
    text = re.sub("/[PJEB]", "", text)

    text = alphabet_text(text)

    # remove unreadable characters
    # print("✍ before ",text);
    # text = normalize("NFD", text)
    # text = "".join(c for c in text if c in symbols)
    # text = normalize("NFC", text)
    # print("✍ after ",text);

    text = text.strip()
    if len(text) == 0:
        return ""

    # only single punctuation
    if text in '.!?':
        return punctuation_text(text)

    # append punctuation if there is no punctuation at the end of the text
    if text[-1] not in '.!?':
        text += ' '

    return text


def remove_duplicated_punctuations(text):
    text = re.sub(r"[.?!]+\?", "?", text)
    text = re.sub(r"[.?!]+!", "!", text)
    text = re.sub(r"[.?!]+\.", ".", text)
    return text


def split_text(text):
    # text = remove_duplicated_punctuations(text)

    texts = []

    # ?와 !로 나눠지는것을 방지하기 위해
    # for subtext in re.findall(r'[^.!?\n]*[.!?\n]', text):
    for subtext in re.findall(r'[^.\n]*[.\n]', text):
        texts.append(subtext.strip())

    # print("💻 split_text : ",texts)
    return texts


def alphabet_text(text):
    text = re.sub(r"(a|A)", "에이", text)
    text = re.sub(r"(b|B)", "비", text)
    text = re.sub(r"(c|C)", "씨", text)
    text = re.sub(r"(d|D)", "디", text)
    text = re.sub(r"(e|E)", "이", text)
    text = re.sub(r"(f|F)", "에프", text)
    text = re.sub(r"(g|G)", "쥐", text)
    text = re.sub(r"(h|H)", "에이치", text)
    text = re.sub(r"(i|I)", "아이", text)
    text = re.sub(r"(j|J)", "제이", text)
    text = re.sub(r"(k|K)", "케이", text)
    text = re.sub(r"(l|L)", "엘", text)
    text = re.sub(r"(m|M)", "엠", text)
    text = re.sub(r"(n|N)", "엔", text)
    text = re.sub(r"(o|O)", "오", text)
    text = re.sub(r"(p|P)", "피", text)
    text = re.sub(r"(q|Q)", "큐", text)
    text = re.sub(r"(r|R)", "알", text)
    text = re.sub(r"(s|S)", "에스", text)
    text = re.sub(r"(t|T)", "티", text)
    text = re.sub(r"(u|U)", "유", text)
    text = re.sub(r"(v|V)", "브이", text)
    text = re.sub(r"(w|W)", "더블유", text)
    text = re.sub(r"(x|X)", "엑스", text)
    text = re.sub(r"(y|Y)", "와이", text)
    text = re.sub(r"(z|Z)", "지", text)

    return text


def punctuation_text(text):
    # 문장부호
    text = re.sub(r"!", "느낌표", text)
    text = re.sub(r"\?", "물음표", text)
    text = re.sub(r"\.", "마침표", text)

    return text


def jamo_text(text):
    # 기본 자모음
    text = re.sub(r"ㄱ", "기역", text)
    text = re.sub(r"ㄴ", "니은", text)
    text = re.sub(r"ㄷ", "디귿", text)
    text = re.sub(r"ㄹ", "리을", text)
    text = re.sub(r"ㅁ", "미음", text)
    text = re.sub(r"ㅂ", "비읍", text)
    text = re.sub(r"ㅅ", "시옷", text)
    text = re.sub(r"ㅇ", "이응", text)
    text = re.sub(r"ㅈ", "지읒", text)
    text = re.sub(r"ㅊ", "치읓", text)
    text = re.sub(r"ㅋ", "키읔", text)
    text = re.sub(r"ㅌ", "티읕", text)
    text = re.sub(r"ㅍ", "피읖", text)
    text = re.sub(r"ㅎ", "히읗", text)
    text = re.sub(r"ㄲ", "쌍기역", text)
    text = re.sub(r"ㄸ", "쌍디귿", text)
    text = re.sub(r"ㅃ", "쌍비읍", text)
    text = re.sub(r"ㅆ", "쌍시옷", text)
    text = re.sub(r"ㅉ", "쌍지읒", text)
    text = re.sub(r"ㄳ", "기역시옷", text)
    text = re.sub(r"ㄵ", "니은지읒", text)
    text = re.sub(r"ㄶ", "니은히읗", text)
    text = re.sub(r"ㄺ", "리을기역", text)
    text = re.sub(r"ㄻ", "리을미음", text)
    text = re.sub(r"ㄼ", "리을비읍", text)
    text = re.sub(r"ㄽ", "리을시옷", text)
    text = re.sub(r"ㄾ", "리을티읕", text)
    text = re.sub(r"ㄿ", "리을피읍", text)
    text = re.sub(r"ㅀ", "리을히읗", text)
    text = re.sub(r"ㅄ", "비읍시옷", text)
    text = re.sub(r"ㅏ", "아", text)
    text = re.sub(r"ㅑ", "야", text)
    text = re.sub(r"ㅓ", "어", text)
    text = re.sub(r"ㅕ", "여", text)
    text = re.sub(r"ㅗ", "오", text)
    text = re.sub(r"ㅛ", "요", text)
    text = re.sub(r"ㅜ", "우", text)
    text = re.sub(r"ㅠ", "유", text)
    text = re.sub(r"ㅡ", "으", text)
    text = re.sub(r"ㅣ", "이", text)
    text = re.sub(r"ㅐ", "애", text)
    text = re.sub(r"ㅒ", "얘", text)
    text = re.sub(r"ㅔ", "에", text)
    text = re.sub(r"ㅖ", "예", text)
    text = re.sub(r"ㅘ", "와", text)
    text = re.sub(r"ㅙ", "왜", text)
    text = re.sub(r"ㅚ", "외", text)
    text = re.sub(r"ㅝ", "워", text)
    text = re.sub(r"ㅞ", "웨", text)
    text = re.sub(r"ㅟ", "위", text)
    text = re.sub(r"ㅢ", "의", text)

    return text


def normalize_multiline_text(long_text):
    texts = split_text(long_text)
    # print(texts)
    normalized_texts = [normalize_text(text).strip() for text in texts]
    # print(normalized_texts)
    return [text for text in normalized_texts if len(text) > 0]

# def synthesize(text):
#     wavs = synthesizer.tts(text, None, None)
#     return wavs


# 3. 학습한 모델 불러오기
syn_start = time.time();
synthesizer = Synthesizer(
### GlowTTS
   "/home/kseek/aiDisk/glowtts_35k_colab_myScale_backup(0525)/checkpoint_44000.pth.tar",
   "/home/kseek/aiDisk/glowtts_35k_colab_myScale_backup(0525)/config.json",
    None,
### HiFiGAN
   "/home/kseek/aiDisk/hifi_balloon_colab/best_model_345013.pth.tar",
   "/home/kseek/aiDisk/hifi_balloon_colab/config.json",
)

## temp start
print('checkpoint : ',synthesizer.tts_checkpoint)
print('checkpoint : ',synthesizer.vocoder_checkpoint)
fileName = synthesizer.tts_checkpoint
fileName = fileName[-13:-8]
## temp end
if fileName[0].isdigit():
    print(fileName)
else:
    fileName = 'best_model'
    print(fileName)






print("👉 only Synthesizer end : ",time.time()-syn_start) # 여기까지 0.5초

# 4. 음성 합성
texts = """
이제 본격적으로 시작해 볼까요? 첫번째 문제 보여주세요! 문제 나갑니다.  정답은 천사였습니다! 1등 그 영광의 주인공은 바로 홍길동님! 축하드립니다!  여러분들의 선택이 궁금한데요 어떤걸 많이 선택하였을지 그 결과를 공개합니다.
"""
'''
texts="""
빛을 특정 세포나 생체 조직에 쪼여 기능을 제어하는 학문 분야로 아이비에스 연구진은 '이 기술'을 이용해 쥐의 뇌 속 유전자 발현을 제어하기도 했습니다. 안녕하세요.
"""
'''
# import librosa    // Synthesizer에 포함되어 제거
import soundfile as sf
inference_start = time.time();

i=0
for text in normalize_multiline_text(texts):
    wav = synthesizer.tts(text, None, None)
    # IPython.display.display(IPython.display.Audio(wav, rate=22050))
    # output_name = '/home/kseek/boxboxbox/ChoTTS/output/%d.wav'%(i)
    # sf.write(output_name, wav, 22050)

    output_name = '/home/kseek/boxboxbox/TTS/soundData/test.wav'
    sf.write(output_name, wav, 22050)
    i+=1
print("Inference : ",time.time()-inference_start); # 0.2초
print("👉 total time : ",time.time()-start);
