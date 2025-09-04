from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import requests
import json

# 初始化 MCP 服務器
mcp = FastMCP(
    name="genai-api",
    stateless_http=True,
    host="0.0.0.0",
    port=8000
)

# 定義 MCP 工具，封裝 API 調用
@mcp.tool()
def query_genai_api(query: str):
    """調用 GenAI API 查詢資訊，例如 Bamboo Crafts Center 的開放時間。"""
    api_url = "https://mfitixkd24e2jo7updj4rtpn.agents.do-ai.run/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer P9g7-B259ShF2RYBM-5KWWCmvZrQHJj_",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500,
        "max_completion_tokens": 500,
        "stream": False,
        "k": 5,
        "retrieval_method": "none",
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None,
        "stream_options": None,
        "kb_filters": None,
        "filter_kb_content_by_query_metadata": False,
        "instruction_override": None,
        "include_functions_info": False,
        "include_retrieval_info": False,
        "include_guardrails_info": False,
        "provide_citations": True
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # 檢查 HTTP 錯誤
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 設置 FastAPI 應用並掛載 MCP
app = FastAPI(title="GenAI API MCP Server")
app.mount("/mcp", mcp.streamable_http_app())

# 啟動服務器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")