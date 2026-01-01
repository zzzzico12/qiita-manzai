import boto3
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# AWS Polly クライアント
polly = boto3.client("polly", region_name="ap-northeast-1")

# 声の設定
VOICE_BOKE = "Takumi"
VOICE_TSUKKOMI = "Mizuki"

# 出力ファイル
OUTPUT_FILE = "manzai_full.mp3"

# ★ 音声を2倍速にする関数
def speedup(audio: AudioSegment, speed: float = 1.2) -> AudioSegment:
    return audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    }).set_frame_rate(audio.frame_rate)

# 台本読み込み
with open("manzai_script.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 最終的に結合する音声
combined = AudioSegment.empty()

index = 1

for line in lines:
    line = line.strip()
    if not line:
        continue

    # 話者判定
    if line.startswith("ボケ："):
        voice = VOICE_BOKE
        text = line.replace("ボケ：", "")
    elif line.startswith("ツッコミ："):
        voice = VOICE_TSUKKOMI
        text = line.replace("ツッコミ：", "")
    else:
        continue

    print(f"Polly生成中: {line}")

    # Polly で音声生成
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice,
        LanguageCode="ja-JP"
    )

    # 一時 mp3 保存
    temp_file = f"temp_{index}.mp3"
    with open(temp_file, "wb") as f:
        f.write(response["AudioStream"].read())

    # pydub で読み込み
    audio = AudioSegment.from_mp3(temp_file)

    # ★ ここで2倍速に変換
    audio_fast = speedup(audio, 1.2)

    # 結合
    combined += audio_fast

    # 一時ファイル削除
    os.remove(temp_file)

    index += 1

# 最後に1つの mp3 として書き出し
combined.export(OUTPUT_FILE, format="mp3")

print("結合完了:", OUTPUT_FILE)
