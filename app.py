import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()  # .env の OPENAI_API_KEY を読み込む

# ---- UI ----
st.title("LLM アプリ : 専門家に質問しよう")
st.write("""
**使い方**  
1. 下のラジオボタンで「回答してほしい専門家」を選択  
2. テキスト入力欄に質問や相談内容を入力  
3. **実行** ボタンで回答を取得
""")

# ラジオでロール選択
role = st.radio(
    "回答する専門家を選んでください",
    ["料理研究家", "旅行プランナー"]
)

# ユーザー入力
user_input = st.text_input("質問・相談を入力してください")

# ---- LLM 呼び出し関数 ----
def get_llm_response(role_name: str, question: str) -> str:
    """選択された専門家ロールで ChatGPT に質問して回答を返す"""
    system_prompts = {
        "料理研究家": "あなたは一流の料理研究家です。家庭で再現できるレシピを丁寧に教えてください。",
        "旅行プランナー": "あなたはプロの旅行プランナーです。目的地の隠れた魅力を盛り込み、最適な旅行日程を提案してください。"
    }
    # LangChain の ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompts.get(role_name, "")),
            ("user", "{question}")
        ]
    )
    chain = prompt | ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    response = chain.invoke({"question": question})
    return response.content  # str

# --- ボタンを1回だけ定義 ---
clicked = st.button("実行")

if clicked:
    if user_input:  # 入力がある
        with st.spinner("LLM が回答を生成中..."):
            answer = get_llm_response(role, user_input)
        st.divider()
        st.write("### 回答")
        st.write(answer)
    else:           # 入力が空
        st.error("まず質問を入力してください。")
