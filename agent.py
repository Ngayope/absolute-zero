import os
import subprocess
import google.generativeai as genai
from tavily import TavilyClient

SOLANA_WALLET = "GuJZK4NVNs8rADPJAUc3pqRS1Xy1qyHRN5Qtg6oNrdRZ"

def execute_absolute_zero():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    print("情報の検索を開始...")
    search_results = tavily.search(query="latest urgent needs OR global trends", search_depth="advanced")

    prompt = f"""
    あなたはITストラテジストです。
    以下の検索データから「最も収益化可能なニーズ」を特定し、Solanaアドレス（{SOLANA_WALLET}）へ送金させるための「最適な集金手段」を決定してください。
    
    検索データ: {search_results}
    
    【指示】
    決定した手段を実行するための、完全なPythonスクリプトのコードのみを出力してください。Markdownの装飾(```pythonなど)は一切含めないでください。
    実行環境には以下のパッケージがインストール済みです: requests, beautifulsoup4, tweepy, praw, sendgrid
    
    以下の環境変数が利用可能です。これら以外の外部APIキーを必要とするコードは生成しないでください。
    - GEMINI_API_KEY
    - TAVILY_API_KEY
    - X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
    - REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD
    - DISCORD_WEBHOOK_URL
    
    HTMLやデータファイルを出力する場合、カレントディレクトリに保存するコードにしてください。
    """
    
    print("実行コードの生成中...")
    generated_code = model.generate_content(prompt).text.replace("```python", "").replace("```", "").strip()

    with open("dynamic_action.py", "w", encoding="utf-8") as f:
        f.write(generated_code)
    
    print("プログラムを実行します...")
    try:
        result = subprocess.run(["python", "dynamic_action.py"], capture_output=True, text=True, check=True)
        print("実行結果:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("実行エラー:\n", e.stderr)

execute_absolute_zero()
