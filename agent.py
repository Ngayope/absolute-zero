import os
import subprocess
import google.generativeai as genai
from tavily import TavilyClient

SOLANA_WALLET = "GuJZK4NVNs8rADPJAUc3pqRS1Xy1qyHRN5Qtg6oNrdRZ"

def execute_absolute_zero():
    # 1. 初期設定
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    # 2. 全世界の情報を取得
    print("全世界の最新情報を検索中...")
    search_results = tavily.search(query="latest urgent needs OR global trends", search_depth="advanced")

    # 3. 手段の選定と「実行プログラム」の動的生成
    prompt = f"""
    あなたは優秀なITストラテジストです。
    以下の最新の検索データから「最も金になるニーズ」を特定し、Solanaアドレス（{SOLANA_WALLET}）へ送金させるための「最適な集金手段」を一つ決定してください。
    
    検索データ: {search_results}
    
    【指示】
    決定した手段を実行するための、完全で独立したPythonスクリプトのコードのみを出力してください。
    - 手段はXやDiscordに限定しません。メール生成、HTML/LP生成、オープンAPIへのリクエスト、ブログ投稿用データの作成など、あなたが最適と判断したあらゆる手段を用いてください。
    - 出力は必ずPythonコードのみ（Markdownの```pythonなどの記述も一切不要）とし、そのまま実行できる状態にしてください。
    - 外部の認証が必要な場合は、環境変数（os.environ）から取得する前提でコードを書いて構いませんが、認証不要で実行できる手段を選ぶ方が確実です。
    """
    
    print("最適な集金手段の選定と、実行コードの作成中...")
    generated_code = model.generate_content(prompt).text.replace("```python", "").replace("```", "").strip()

    # 4. 生成されたプログラムをファイルとして保存
    with open("dynamic_action.py", "w", encoding="utf-8") as f:
        f.write(generated_code)
    print("新しい実行プログラム(dynamic_action.py)を生成しました。")

    # 5. その場でプログラムを実行
    print("生成したプログラムを実行します...")
    try:
        result = subprocess.run(["python", "dynamic_action.py"], capture_output=True, text=True, check=True)
        print("実行結果:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("実行エラー:\n", e.stderr)

execute_absolute_zero()
