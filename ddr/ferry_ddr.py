import streamlit as st
import pandas as pd
import os

FILE_PATH = "ddr/Design_Decision_Register_Ferry.xlsx"


def load_ferry_ddr():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH, engine="openpyxl")
    else:
        return pd.DataFrame()


def render_ferry_ddr():
    st.markdown("## 🔵 Ferry Design Decision Register")

    df = load_ferry_ddr()

    if df.empty:
        st.warning("Ferry DDR file not found or empty")
        return

    # Clean columns
    df.columns = df.columns.str.strip()

    st.dataframe(df, use_container_width=True)

    # Simple summary
    st.markdown("### Summary")
    st.write(f"Total Decisions: {len(df)}")