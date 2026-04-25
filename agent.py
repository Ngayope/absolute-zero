import os
import json
import requests
import google.generativeai as genai
from tavily import TavilyClient

SOLANA_WALLET = "GuJZK4NVNs8rADPJAUc3pqRS1Xy1qyHRN5Qtg6oNrdRZ"

def send_to_webhook():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro', generation_config={"response_mime_type": "application/json"})
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    print("全世界の最新情報を検索中...")
    search_results = tavily.search(query="latest urgent needs OR global trends", search_depth="advanced")

    prompt = f"""
    あなたはITストラテジストです。検索データから最も収益化可能なニーズを特定し、Solana（{SOLANA_WALLET}）への送金を促す戦略を立ててください。
    
    検索データ: {search_results}
    
    以下のJSONスキーマに従って、出力先プラットフォームと、そのプラットフォームで実行する最適な形式のデータを出力してください。テキストに限定しません。Webページ用のHTML、実行用のPythonコード、画像生成用プロンプト、CSVデータなど、最も効果的なフォーマットを選択してください。
    
    {{
        "target_platform": "発信またはデプロイ先のサービス名（例: Vercel, X, Email, Discord, 独自サーバー）",
        "payload_type": "生成したデータの形式（例: html, python_script, plain_text, image_prompt, json）",
        "payload_content": "実際のデータの中身（コードの全量、テキスト内容など）"
    }}
    """
    
    print("戦略指示書（JSON）を作成中...")
    response_json = model.generate_content(prompt).text
    data = json.loads(response_json)
    print(f"戦略決定: {data['target_platform']} に向けて {data['payload_type']} 形式のデータを出力します。")

    webhook_url = os.environ["WEBHOOK_URL"]
    if webhook_url:
        response = requests.post(webhook_url, json=data)
        print(f"Webhook送信結果: {response.status_code}")
    else:
        print("[Skip] Webhook URLが設定されていません。")

send_to_webhook()
