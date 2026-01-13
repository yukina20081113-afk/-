import streamlit as st
import os

st.title("デジタル備忘録")

SAVE_DIR = "memos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ファイル一覧
files = os.listdir(SAVE_DIR)
selected = st.selectbox(
    "編集するメモを選ぶ（新規は空白）",
    ["新規"] + files
)

# 読み込み
text = ""
filename = ""

if selected != "新規":
    filename = selected
    with open(os.path.join(SAVE_DIR, filename), "r", encoding="utf-8") as f:
        text = f.read()
else:
    filename = st.text_input("ファイル名（例：math.txt）")

# 入力欄（自動保存）
content = st.text_area("メモを書く", value=text, height=300)

# 自動保存
if filename:
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    st.success("自動保存中")
