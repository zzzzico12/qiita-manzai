import os
import io
import sys
from dotenv import load_dotenv
from strands import Agent, tool

# .envファイルから環境変数を読み込む
load_dotenv()

# ============================
# ボケエージェント
# ============================
@tool
def boke_agent(query: str):
    agent = Agent(
        model="jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt=(
            "あなたは漫才コンビのボケ担当です。"
            "関西弁で、1〜2文でテンポよくボケてください。"
            "返答は必ず『ボケ：<内容>』の形式にしてください。"
        )
    )
    return str(agent(query))


# ============================
# ツッコミエージェント
# ============================
@tool
def tsukkomi_agent(query: str):
    agent = Agent(
        model="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
        system_prompt=(
            "あなたは漫才コンビのツッコミ担当です。"
            "関西弁で、1〜2文でテンポよくツッコんでください。"
            "返答は必ず『ツッコミ：<内容>』の形式にしてください。"
        )
    )
    return str(agent(query))


# ============================
# 監督エージェント（オーケストレーター）
# ============================
orchestrator = Agent(
    model="jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
    system_prompt=(
        "あなたは漫才の監督です。"
        "あなた自身は絶対に返答を生成しません。"
        "必ず boke_agent または tsukkomi_agent を tool 呼び出しとして返してください。"
        "返答は必ず『ボケ：<内容>』『ツッコミ：<内容>』の形式に統一してください。"
        "ボケ→ツッコミ→ボケ→ツッコミ…の順で5ターン進めてください。"
        "ツール呼び出し以外の文章は一切出力してはいけません。"
    ),
    tools=[boke_agent, tsukkomi_agent]
)

# ============================
# ★ orchestrator 実行全体を stdout キャプチャ
# ============================
buffer = io.StringIO()
stdout_backup = sys.stdout
sys.stdout = buffer

# ここでツール実行ログ（漫才）が stdout に出る
result = orchestrator("テーマは『AIとおばあちゃん』で漫才を始めてください。")

# stdout を元に戻す
sys.stdout = stdout_backup

# キャプチャした内容を取得
text = buffer.getvalue()

print("===DEBUG START===")
print(text)
print("===DEBUG END===")

# ============================
# 出力結果をそのまま保存
# ============================
with open("manzai_script.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("manzai_script.txt に書き込み成功")
