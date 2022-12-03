import streamlit as st
import pandas as pd
from plotly import graph_objects as go
from plotly import express as px
import random

st.set_page_config(page_icon="📋", page_title="MLM 量表", layout="wide")


if "results" not in st.session_state:
    st.session_state["results"] = {}

L, M, R = st.columns([1, 5, 1])

with M:
    st.title("📋 MLM 量表")
    st.radio(
        "语言 / Language",
        options=[0, 1],
        format_func=lambda i: ["中文", "English"][i],
        key="lang",
        horizontal=True,
    )
    df = pd.read_csv(
        "asset/MLM.csv" if st.session_state["lang"] else "asset/MLM-CR.csv"
    )

    if st.session_state["results"] == {}:
        with st.form("……"):
            new_df = df.copy().iloc[random.sample(range(len(df)), len(df)), :]
            st.markdown("---")
            for _, idx, des, neg, pos, rat in new_df.itertuples():
                format_dict = {
                    1: neg,
                    2: "",
                    3: "",
                    4: "Hard to say" if st.session_state["lang"] else "不确定",
                    5: "",
                    6: "",
                    7: pos,
                }
                st.markdown(
                    '<p style="font-size: 1.25rem;">' + des + "</p>",
                    unsafe_allow_html=True,
                )
                st.select_slider(
                    label='<p style="font-size: 2rem;">' + des + "</p>",
                    options=[1, 2, 3, 4, 5, 6, 7],
                    value=4,
                    format_func=lambda x: format_dict[x],
                    key=idx,
                    label_visibility="hidden",
                )
                st.markdown("---")
            if st.form_submit_button("提交"):
                st.session_state["results"] = {
                    i: st.session_state[str(i)] for i in range(1, len(df) + 1)
                }
                st.experimental_rerun()
    else:
        st.subheader(
            "Your meaning of life measure profile"
            if st.session_state["lang"]
            else "您对生命意义的感知画像"
        )
        sections = (
            ["Exciting", "Accomplished", "Principled", "Purposeful", "Valued"]
            if st.session_state["lang"]
            else ["令人激动的", "有成就的", "有原则的", "有目标的", "有价值的"]
        )
        ranges = [1, 6, 11, 16, 20, 24]
        mins = [
            sum(
                1 if df.loc[x - 1, "Rating"] > 0 else -7
                for x in range(ranges[i], ranges[i + 1])
            )
            for i in range(len(sections))
        ]
        maxs = [
            sum(
                7 if df.loc[x - 1, "Rating"] > 0 else -1
                for x in range(ranges[i], ranges[i + 1])
            )
            for i in range(len(sections))
        ]
        scores = [
            sum(
                st.session_state["results"][idx]
                for idx in range(ranges[i], ranges[i + 1])
            )
            for i in range(len(sections))
        ]
        data = pd.DataFrame(
            {
                "r": [
                    (scores[i] - mins[i]) / (maxs[i] - mins[i])
                    for i in range(len(sections))
                ],
                "theta": sections,
            }
        )
        fig = px.line_polar(
            data,
            r="r",
            theta="theta",
            line_close=True,
            template="plotly_dark",
        )
        fig.update_traces(fill="toself")
        fig.update_layout(
            dict(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                template=None,
                polar=dict(
                    radialaxis=dict(range=[0, 1], showticklabels=False, ticks=""),
                ),
            ),
            overwrite=True,
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Retake test" if st.session_state["lang"] else "重新测试"):
            st.session_state["results"] = {}
            st.experimental_rerun()
