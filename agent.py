import os
import json
import requests
import google.generativeai as genai
from tavily import TavilyClient

SOLANA_WALLET = "GuJZK4NVNs8rADPJAUc3pqRS1Xy1qyHRN5Qtg6oNrdRZ"

def execute_absolute_zero_core():
    # 1. 脳と目の初期化
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro', generation_config={"response_mime_type": "application/json"})
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    # 2. 【フェーズ1】検索クエリの自律生成
    # 枠をはめないよう、AIに「今探すべき領域」から決めさせる
    query_gen_prompt = """
    あなたは全世界の情報を監視する偵察機です。
    今この瞬間、世界中で「金銭的な解決」が最も切実に求められている、あるいは急激なトレンドの変化が起きている領域を分析し、
    その実態を調査するための検索クエリを英語で3つ生成してください。
    
    出力形式(JSON):
    {"queries": ["query1", "query2", "query3"]}
    """
    query_data = json.loads(model.generate_content(query_gen_prompt).text)
    queries = query_data["queries"]
    print(f"自律生成されたクエリ: {queries}")

    # 3. 【フェーズ2】無限の探索
    search_payload = ""
    for q in queries:
        search_payload += str(tavily.search(query=q, search_depth="advanced"))

    # 4. 【フェーズ3】戦略構築と多角的執行
    strategy_prompt = f"""
    以下の全世界リアルタイム調査データに基づき、Solana({SOLANA_WALLET})へ収益を誘導する最強の戦略を立ててください。
    
    調査データ: {search_payload}
    
    ターゲットの言語、プラットフォーム、データの形式（HTML, Python, 投稿文, 企画書等）を一切限定せず、最も稼げるアウトプットを生成してください。
    
    出力形式(JSON):
    {{
        "target_platform": "サービス名",
        "payload_type": "html/python/text/prompt/json等",
        "payload_content": "実行用データの中身（制限なし。コードなら全量、文章なら全文）"
    }}
    """
    
    print("最終戦略を構築中...")
    final_output = json.loads(model.generate_content(strategy_prompt).text)
    
    # 5. Webhookへの放流
    webhook_url = os.environ["WEBHOOK_URL"]
    if webhook_url:
        requests.post(webhook_url, json=final_output)
        print(f"執行完了: {final_output['target_platform']} 向けに出力しました。")

execute_absolute_zero_core()
