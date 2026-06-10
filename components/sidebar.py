import streamlit as st
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_sidebar(datasets, DDR_FILES):

    logo_base64 = get_base64_image("assets/logo.png")

    # =========================
    # BASIC STYLE
    # =========================
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display:none;}
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #08111f 0%, #0b1a2f 100%);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:

        # =========================
        # LOGO
        # =========================
        st.markdown(f"""
        <div style="text-align:center; padding:10px;">
            <img src="data:image/png;base64,{logo_base64}" width="80">
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # 🟢 ASSET
        # =========================
        st.markdown("### 🟢 ASSET")

        asset = st.radio(
            "",
            list(datasets.keys()),
            key="asset_selector"
        )

        df = datasets[asset].copy()
        df.columns = df.columns.str.strip().str.lower()

        # =========================
        # FILTERS
        # =========================
        st.markdown("### FILTERS")

        doc_type = st.selectbox(
            "Doc Type",
            ["All"] + sorted(df["doc type"].dropna().unique().tolist())
        )

        status = st.selectbox(
            "Status",
            ["All"] + sorted(df["status"].dropna().unique().tolist())
        )

        filtered_df = df.copy()

        if doc_type != "All":
            filtered_df = filtered_df[filtered_df["doc type"] == doc_type]

        if status != "All":
            filtered_df = filtered_df[filtered_df["status"] == status]

        # =========================
        # SEQUENCE
        # =========================
        st.markdown("### SEQUENCE")

        seq_list = sorted(filtered_df["seq no"].dropna().unique().tolist())

        if len(seq_list) == 0:
            st.warning("No records found")
            return asset, filtered_df, None, None

        seq_choice = st.selectbox("Select Seq No", seq_list)

        # =========================
        # 🔵 DESIGN DECISION REGISTER
        # =========================
        st.markdown("---")
        st.markdown("### 🔵 DESIGN DECISION REGISTER")

        # ✅ THIS IS THE IMPORTANT PART (VISIBLE)
        st.write("Select:")

        ddr_assets = ["Ferry", "Flass", "Rossall", "ASP4", "TallyHo"]

        selected_ddr = st.radio(
            "",
            ddr_assets,
            key="ddr_selector"
        )

        # ✅ prevent auto open on first load
        if "ddr_init" not in st.session_state:
            st.session_state.ddr_init = True
            selected_ddr = None

        # =========================
        # RETURN
        # =========================
        return asset, filtered_df, seq_choice, selected_ddr