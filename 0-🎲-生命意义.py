import json

import streamlit as st

st.set_page_config(page_icon="🎲", page_title="MLM RPG")

st.title("🎲 MLM RPG")

ROOT_DIR = "asset"


def load_script() -> dict:
    with open(ROOT_DIR + "/script.json", "r") as f:
        return json.load(f)


if "history" not in st.session_state:
    st.session_state["history"] = []

if "current" not in st.session_state:
    st.session_state["current"] = {}

if st.session_state["current"] == {}:
    with st.form("选择故事起点"):
        script = load_script()
        idx = st.radio(
            "故事编号",
            options=range(len(script.keys())),
            format_func=lambda i: f"故事 {i}",
            index=0,
            horizontal=True,
        )
        if st.form_submit_button("开始新的故事吧！") and idx is not None:
            choice = list(script.keys())[idx]
            st.session_state["current"] = {choice: script[choice]}
            st.experimental_rerun()
else:
    for h in st.session_state["history"]:
        st.info(h[0])
        st.info(h[1])
    if isinstance(st.session_state["current"], dict):
        text: str = list(st.session_state["current"].keys())[0]
        st.info(text.replace("|", "\n\n"))
        with st.form("……"):
            choice = st.radio(
                "options",
                options=list(st.session_state["current"][text].keys()),
                label_visibility="hidden",
            )
            if st.form_submit_button("确定"):
                st.session_state["history"].append((text.replace("|", "\n\n"), choice))
                st.session_state["current"] = st.session_state["current"][text][choice]
                st.experimental_rerun()
    else:
        match st.session_state["current"][-2:]:
            case "HE":
                st.success(st.session_state["current"][:-2].replace("|", "\n\n"))
            case "NE":
                st.warning(st.session_state["current"][:-2].replace("|", "\n\n"))
            case "BE":
                st.error(st.session_state["current"][:-2].replace("|", "\n\n"))
            case _:
                st.info(st.session_state["current"].replace("|", "\n\n"))
        if st.button("remake!"):
            st.session_state["history"] = []
            st.session_state["current"] = {}
            st.experimental_rerun()
