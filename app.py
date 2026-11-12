import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import textwrap

st.set_page_config(
    page_title="AI Health Analytics", page_icon="📊", layout="wide"
)


df = pd.read_csv("Ai_impact on health_cleaning.csv")


st.markdown(
    """
    <style>
    /* 1. Main Background */
    .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }

    /* 2. Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D !important;
    }

    /* 3. Single line Menu Title fix */
    div[data-testid="stSidebar"] .menu-title {
        white-space: nowrap !important;
        font-size: 18px !important;
        color: #58A6FF !important;
    }

    /* 4. Navigation icons fix */
    div[data-testid="stSidebar"] .nav-link i,
    div[data-testid="stSidebar"] .nav-link::before {
        display: none !important;
        width: 0px !important;
    }

    /* 5. Custom Column Gap for Single Row Layout */
    div[data-testid="stHorizontalBlock"] {
        gap: 12px !important;
    }

    /* 6. Card Base Styling with Top Highlight Border */
    .kpi-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 135px;
    }

    /* Top Highlight Border Colors for Each Card */
    .card-blue { border-top: 4px solid #58A6FF !important; }
    .card-purple { border-top: 4px solid #BC8CFF !important; }
    .card-pink { border-top: 4px solid #F778BA !important; }
    .card-green { border-top: 4px solid #3FB950 !important; }
    .card-gold { border-top: 4px solid #D29922 !important; }
    .card-cyan { border-top: 4px solid #38BDF8 !important; }

    /* Hover Effect */
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }

    /* Icon (Top) */
    .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 6px;
        line-height: 1;
    }

    /* Label (Middle) */
    .kpi-label {
        font-size: 0.8rem;
        color: #8B949E;
        font-weight: 500;
        margin-bottom: 8px;
        white-space: nowrap;
    }

    /* Value (Bottom) */
    .kpi-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F0F6FC;
        line-height: 1;
    }

    .kpi-value-green {
        color: #3FB950;
    }
    </style>
""",
    unsafe_allow_html=True,
)


with st.sidebar:
    opt = option_menu(
        menu_title="📊 AI Health Analysis",
        options=[
            "🏠 Overview",
            "🔍 Data Explorer",
            "💡 Key Insights",
            "📈 Visual Analytics",
            "ℹ️ About & Methodology",
        ],
        menu_icon="none",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#161B22",
                "border": "none",
            },
            "icon": {"display": "none", "width": "0px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0px",
                "padding": "10px 15px",
                "color": "#8B949E",
                "--hover-color": "#21262D",
                "border-radius": "6px",
                "list-style": "none",
            },
            "nav-link-selected": {
                "background-color": "#238636",
                "color": "#FFFFFF",
                "font-weight": "600",
            },
        },
    )

    st.markdown("")
    st.markdown("### 🔍 Select Filters")

    gender = st.multiselect(
        "Select Gender", options=df["Gender"].unique(), key="m_gender"
    )
    bmi_cat = st.multiselect(
        "Select BMI Category",
        options=df["BMI_Category"].unique(),
        key="m_bmi",
    )
    tool_type = st.multiselect(
        "Select Tool Type", options=df["AI_Tool_Type"].unique(), key="m_tool"
    )


filtered_df = df.copy()

if gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]
if bmi_cat:
    filtered_df = filtered_df[filtered_df["BMI_Category"].isin(bmi_cat)]
if tool_type:
    filtered_df = filtered_df[filtered_df["AI_Tool_Type"].isin(tool_type)]


if opt == "🏠 Overview":
    st.title("🏠 AI Health & Wellness Overview")
    st.markdown(
        "##### Real-time insights into AI tool adoption, health scores, and participant outcomes."
    )
    st.markdown("---")

    
    total_participants = len(filtered_df)
    avg_score_before = (
        filtered_df["Health_Score_Before_AI"].mean()
        if "Health_Score_Before_AI" in filtered_df.columns
        and total_participants > 0
        else 0
    )
    avg_score_after = (
        filtered_df["Health_Score_After_AI"].mean()
        if "Health_Score_After_AI" in filtered_df.columns
        and total_participants > 0
        else 0
    )
    avg_improvement = (
        filtered_df["Improvement_Percentage"].mean()
        if "Improvement_Percentage" in filtered_df.columns
        and total_participants > 0
        else 0
    )
    avg_satisfaction = (
        filtered_df["Satisfaction_Score"].mean()
        if "Satisfaction_Score" in filtered_df.columns
        and total_participants > 0
        else 0
    )
    total_tools = (
        filtered_df["AI_Tool_Type"].nunique()
        if "AI_Tool_Type" in filtered_df.columns and total_participants > 0
        else 0
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card card-blue">
                <div class="kpi-icon">👥</div>
                <div class="kpi-label">Participants</div>
                <div class="kpi-value">{total_participants:,}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card card-purple">
                <div class="kpi-icon">📊</div>
                <div class="kpi-label">Score Before AI</div>
                <div class="kpi-value">{avg_score_before:.1f}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card card-pink">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-label">Score After AI</div>
                <div class="kpi-value">{avg_score_after:.1f}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card card-green">
                <div class="kpi-icon">📈</div>
                <div class="kpi-label">Improvement %</div>
                <div class="kpi-value kpi-value-green">{avg_improvement:+.1f}%</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            f"""
            <div class="kpi-card card-gold">
                <div class="kpi-icon">⭐</div>
                <div class="kpi-label">Satisfaction</div>
                <div class="kpi-value">{avg_satisfaction:.1f}<span style="font-size:0.8rem; color:#8B949E;"> / 10</span></div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col6:
        st.markdown(
            f"""
            <div class="kpi-card card-cyan">
                <div class="kpi-icon">🤖</div>
                <div class="kpi-label">AI Tool Types</div>
                <div class="kpi-value">{total_tools}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    
    st.subheader("📊 Health Improvement & Satisfaction by AI Tool Type")
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df.groupby("AI_Tool_Type", as_index=False).agg(
                {"Improvement_Percentage": "mean"}
            ),
            x="AI_Tool_Type",
            y="Improvement_Percentage",
            color="AI_Tool_Type",
            text_auto=".1f",
            title="Average Improvement Percentage per AI Tool Type",
            template="plotly_dark",
            color_discrete_sequence=[
                "#58A6FF",
                "#238636",
                "#D29922",
                "#BC8CFF",
                "#38BDF8",
                "#FF7B72",
            ],
        )
        fig.update_traces(
            textposition="outside",
            marker=dict(line=dict(color="#30363D", width=1.5)),
        )
        fig.update_layout(
            paper_bgcolor="#0D1117",
            plot_bgcolor="#0D1117",
            font=dict(color="#C9D1D9", size=13),
            xaxis_title="AI Tool Category",
            yaxis_title="Avg Improvement (%)",
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

elif opt == "🔍 Data Explorer":

    st.markdown(
        """
        <style>
            /* 1. Remove Top Extra Space */
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 1rem !important;
            }
            
            /* 2. Title & Component Styling */
            .main-title {
                color: #58A6FF;
                font-size: 28px;
                font-weight: 700;
                margin-top: 0px !important;
                margin-bottom: 15px !important;
            }

            .info-card {
                background: linear-gradient(135deg, #161B22 0%, #21262D 100%);
                border: 1px solid #30363D;
                color: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            .info-metric {
                font-size: 24px;
                font-weight: bold;
                margin-top: 5px;
                color: #58A6FF;
            }
            .sub-title {
                color: #C9D1D9;
                font-size: 20px;
                font-weight: 600;
                margin-top: 0px;
                margin-bottom: 10px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">🔍 Data Explorer</div>', unsafe_allow_html=True
    )  
    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown(
            """
                <div class="info-card">
                    <h3>📊 Dataset Overview</h3>
                    <p style="margin-bottom: 15px; font-size: 14px; color: #8B949E;">Summary of loaded dataset size:</p>
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 14px; opacity: 0.9;">Total Rows:</span>
                        <div class="info-metric">{:,}</div>
                    </div>
                    <div>
                        <span style="font-size: 14px; opacity: 0.9;">Total Columns:</span>
                        <div class="info-metric">{}</div>
                    </div>
                </div>
            """.format(
                df.shape[0], df.shape[1]
            ),
            unsafe_allow_html=True,
        )


        
    with col1:

        st.markdown(
            """
            <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 16px; margin-top: 15px;">
                <h4 style="color: #58A6FF; margin: 0 0 10px 0; font-size: 15px;">⚡ Quick Stats</h4>
                <div style="font-size: 13px; color: #C9D1D9; line-height: 1.8;">
                    • <b>Numeric Columns:</b> {num_cols}<br>
                    • <b>Categorical Columns:</b> {cat_cols}<br>
                    • <b>Missing Values:</b> {missing}
                </div>
            </div>
            """.format(
                num_cols=len(df.select_dtypes(include=["number"]).columns),
                cat_cols=len(df.select_dtypes(include=["object"]).columns),
                missing=df.isnull().sum().sum(),
            ),
            unsafe_allow_html=True,
        )

        with st.expander("📋 View Column Names"):
            
            for col in df.columns:
                st.markdown(
                    f'<div style="color: #C9D1D9; font-size: 13.5px; padding: 3px 0;">🔹 {col}</div>',
                    unsafe_allow_html=True,
                   
                )
                
        with col2:
            st.markdown(
                '<div class="sub-title">🎛️ Row Viewer</div>',
                unsafe_allow_html=True,
            )

            num_rows = st.slider(
                "Select number of rows to preview in expanders:",
                min_value=5,
                max_value=100,
                value=5,
                step=5,
            )

            with st.expander(f"📌 First {num_rows} Rows of Dataset", expanded=True):
                st.dataframe(df.head(num_rows), use_container_width=True)

            with st.expander(f"📌 Last {num_rows} Rows of Dataset", expanded=False):
                st.dataframe(df.tail(num_rows), use_container_width=True)



    st.markdown("---")

    
    st.markdown(
        """
        <style>
            /* Custom styling for Download Button */
            div.stDownloadButton > button {
                background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
                color: #FFFFFF !important;
                border: 1px solid #3fb950 !important;
                border-radius: 8px !important;
                padding: 10px 24px !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(46, 160, 67, 0.2) !important;
            }
            div.stDownloadButton > button:hover {
                background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(46, 160, 67, 0.4) !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

           
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name="filtered_dataset.csv",
                mime="text/csv",
                use_container_width=True,
            )

elif opt =="💡 Key Insights":

    
    st.markdown(
        """
        <style>
        /* High Quality Dark Theme Background */
        .stApp {
            background: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), 
                        url('https://images.unsplash.com/photo-1505751172876-fa1923c5c528?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* Glassmorphism Card Style */
        .insight-card {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            transition: all 0.35s ease-in-out;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        /* Hover Effect for Cards */
        .insight-card:hover {
            transform: translateY(-8px);
            box-shadow: 0px 12px 30px rgba(255, 187, 120, 0.25);
            background: rgba(255, 255, 255, 0.12);
            border-color: #ffbb78;
        }

        /* Card Label & Icons */
        .card-label {
            font-size: 1rem;
            color: #cbd5e1;
            margin-bottom: 8px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-value {
            font-size: 1.85rem;
            font-weight: 700;
            color: #ffbb78;
            letter-spacing: 0.5px;
        }

        .insight-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #ffbb78;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .insight-desc {
            font-size: 0.95rem;
            color: #e2e8f0;
            line-height: 1.6;
        }

        .highlight-num {
            color: #aec7e8;
            font-weight: 700;
            background: rgba(174, 199, 232, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

   
    st.title("💡 Key Insights & Analytics Dashboard")
    st.markdown(
        "Comprehensive analysis and findings from the AI Health Engagement dataset."
    )
    st.write("---")

    tab1, tab2 = st.tabs(
        [
        
            "🔥 Correlation Heatmap",
            "📊 Stats & Unique Metrics",
        ]
    )
   
    with tab1:
        corr_cols = [
            "Age",
            "BMI",
            "AI_Health_App_Usage_Hours_Per_Week",
            "Exercise_Hours_Per_Week",
            "Health_Score_Before_AI",
            "Health_Score_After_AI",
            "Improvement_Percentage",
        ]

        if "df" in locals() or "df" in globals():
            cols = [col for col in corr_cols if col in df.columns]

            if cols:
                corr_matrix = df[cols].corr()

                fig = px.imshow(
                    corr_matrix,
                    text_auto=".2f",
                    color_continuous_scale="Blues",
                    title="Correlation Heatmap",
                    template="plotly_white",
                )
                fig.update_layout(
                    width=900,
                    height=750,
                    title={
                        "text": "Correlation Matrix",
                        "x": 0.5,
                        "xanchor": "center",
                        "font": {"size": 22, "color": "White"},
                    },
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(
                    "Required numerical columns for correlation heatmap are missing."
                )
        else:
            st.error(
                "Dataset 'df' is not loaded. Please upload or load your data first."
            )

    
    with tab2:
        if "df" in locals() or "df" in globals():

           
            st.subheader("📈 Statistical Summary (Mean Values)")

            n1, n2, n3 = st.columns(3)
            with n1:
                val = (
                    f"{df['Age'].mean():.1f} yrs"
                    if "Age" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🎂 Average Age</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with n2:
                val = (
                    f"{df['BMI'].mean():.2f}" if "BMI" in df.columns else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">⚖️ Average BMI</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with n3:
                val = (
                    f"{df['AI_Health_App_Usage_Hours_Per_Week'].mean():.1f} hrs/wk"
                    if "AI_Health_App_Usage_Hours_Per_Week" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">📱 Mean App Usage</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            n4, n5, n6 = st.columns(3)
            with n4:
                val = (
                    f"{df['Exercise_Hours_Per_Week'].mean():.1f} hrs/wk"
                    if "Exercise_Hours_Per_Week" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🏃 Mean Exercise</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with n5:
                val = (
                    f"{df['Health_Score_After_AI'].mean():.1f}"
                    if "Health_Score_After_AI" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🩺 Avg Post-AI Score</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with n6:
                val = (
                    f"{df['Improvement_Percentage'].mean():.2f}%"
                    if "Improvement_Percentage" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🚀 Mean Improvement</div>
                        <div class="card-value">{val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            st.write("---")

            
            st.subheader("🔍 Column Unique Values Count")

            c1, c2, c3 = st.columns(3)
            with c1:
                uniq_val = (
                    f"{df['Age'].nunique():,}"
                    if "Age" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🎯 Unique Ages</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with c2:
                uniq_val = (
                    f"{df['BMI'].nunique():,}"
                    if "BMI" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">📏 Unique BMI Values</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with c3:
                uniq_val = (
                    f"{df['AI_Health_App_Usage_Hours_Per_Week'].nunique():,}"
                    if "AI_Health_App_Usage_Hours_Per_Week" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">⏱️ Unique App Hours</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            c4, c5, c6 = st.columns(3)
            with c4:
                uniq_val = (
                    f"{df['Exercise_Hours_Per_Week'].nunique():,}"
                    if "Exercise_Hours_Per_Week" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🚴 Unique Exercise Hours</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with c5:
                uniq_val = (
                    f"{df['Health_Score_After_AI'].nunique():,}"
                    if "Health_Score_After_AI" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">🏆 Unique Health Scores</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with c6:
                uniq_val = (
                    f"{df['Improvement_Percentage'].nunique():,}"
                    if "Improvement_Percentage" in df.columns
                    else "N/A"
                )
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="card-label">📊 Unique % Improvements</div>
                        <div class="card-value">{uniq_val}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

elif opt == "📈 Visual Analytics":

    st.markdown("""
        <style>
        /* Tabs Container */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 12px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        /* Individual Tab Buttons */
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            background-color: #ffffff;
            border-radius: 10px;
            color: #495057;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid #dee2e6;
            padding: 0px 20px;
            transition: all 0.3s ease-in-out;
        }

        /* Tab Hover Effect */
        .stTabs [data-baseweb="tab"]:hover {
            color: #1e88e5;
            border-color: #1e88e5;
            background-color: #f0f7ff;
            transform: translateY(-2px);
        }

        /* Active Tab Styling */
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%) !important;
            color: #ffffff !important;
            border-color: #1565c0 !important;
            box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
        }

        /* Hide Default Tab Highlight Line */
        .stTabs [data-baseweb="tab-border-highlight"] {
            background-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    
    st.title("📊 Visual Analytics Dashboard")
    st.markdown("Select a dimension below to explore interactive charts.")

    
    tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📌 Categorical & Dist",
        "🔥 Correlation & Matrix",
        "📈 Trends & Comparison",
        "🌳 Hierarchical",
        
    ]
)

    with tab1:
        
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.histogram(
                df,
                x="AI_Tool_Type",
                color="Gender",
                nbins=20,
                title="AI tool Usage by Gender",
                # text_auto=True,
                color_discrete_sequence=["#2b8cbe", "#e34a33", "#636363"],
                barmode="group"
            )
            fig1.update_layout(
                title_x=0.2,
                xaxis_title="AI Tool Type",
                yaxis_title="Count",
                bargap=0.05,
                font=dict(size=15),
        
            )
            fig1.update_traces(marker_line_color="black", marker_line_width=1)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            dark_palette = ["#2b5c8f", "#4682b4", "#76a5af", "#e06666"]
            fig2 = px.pie(
                df,
                names="Improvement_Category",
                title="Proportion of Improved Categories",
                hole=0.4,
                color_discrete_sequence=dark_palette,
            )
            fig2.update_traces(textinfo="value + percent")
            fig2.update_layout(
                font=dict(size=16),
        
                title_x=0.2,
            )
            st.plotly_chart(fig2, use_container_width=True)

        
        col1, col2 = st.columns(2)

        with col1:
            fig3 = px.histogram(
                df,
                x="Age",
                color="Gender",
                barmode="group",
                nbins=30,
                color_discrete_map={
                    "Male": "#00F0FF",
                    "Female": "#FF007F",
                    "Other": "#7000FF",
                },
                title="Demographic Distribution: Age Breakdown by Gender",
                template="plotly_white",
            )
            fig3.update_traces(opacity=0.75)
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            fig4 = px.pie(
                df,
                names="AI_Tool_Type",
                hole=0.45,
                title="Distribution of AI Tool Usage",
                color_discrete_sequence=["#60A5FA", "#4ADE80", "#FBBF24", "#FB7185"],
                template="plotly_dark",
            )
            fig4.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig4, use_container_width=True)

        
        col1, col2 = st.columns(2)

        with col1:
            fig5 = px.box(
                df,
                x="BMI_Category",
                y="Improvement",
                color="BMI_Category",
                color_discrete_sequence=[
                    "#2b5c8f",
                    "#d95f02",
                    "#7570b3",
                    "#e7298a",
                ],
                title="Health Score Distribution by BMI Category",
                labels={
                    "Improvement": "Absolute Health Score Improvement",
                    "BMI_Category": "BMI Category",
                },
                template="plotly_white",
            )
            st.plotly_chart(fig5, use_container_width=True)

        with col2:
            fig = px.violin(
            df, 
            x='AI_Usage_Level', 
            y='Satisfaction_Score', 
            color='AI_Usage_Level', 
            box=True, 
            points='outliers',
            color_discrete_sequence=["#00F0FF", "#FF007F", "#7000FF"],
            # color_discrete_sequence=px.colors.qualitative.Prism,
            title='Satisfaction Score Distribution across AI Usage Levels',
            labels={'Satisfaction_Score': 'Satisfaction Score', 'AI_Usage_Level': 'AI Usage Level'},
            template='plotly_white'
        )
            st.plotly_chart(fig,use_container_width=True)

        fig = px.histogram(
        df, 
        x='Age_Group', 
        color='Improvement_Category',
        barmode='group',
        title='Improvement Category Distribution across Age Groups',
        labels={'Age_Group': 'Age Group', 'count': 'Number of Patients'},
        template='plotly_dark'
    )
        fig.update_layout(title_x=0.2)
        st.plotly_chart(fig,use_container_width=True)


    with tab2:
        fig = px.density_heatmap(
        df, 
        x='AI_Health_App_Usage_Hours_Per_Week', 
        y='Satisfaction_Score',
        color_continuous_scale='YlGnBu',
        title=' AI Usage Hours vs. Satisfaction Score',
        labels={'AI_Health_App_Usage_Hours_Per_Week': 'AI App Usage Hours', 'Satisfaction_Score': 'Satisfaction Score'},
        template='plotly_dark'
    )
        fig.update_layout(title_x=0.2,font=dict(size=14),title_font_size=28)
        st.plotly_chart(fig,use_container_width=True) 

        fig_scatter = px.scatter(
        df, 
        x='AI_Health_App_Usage_Hours_Per_Week', 
        y='Improvement_Percentage', 
        color='BMI_Category', 
        size='Satisfaction_Score',          
        color_discrete_sequence=px.colors.qualitative.Bold,
        title='AI App Usage Hours vs Health Score Improvement % (by BMI Category)',
        labels={
            'AI_Health_App_Usage_Hours_Per_Week': 'Weekly AI App Usage (Hours)', 
            'Improvement_Percentage': 'Health Improvement %',
            'BMI_Category': 'BMI Profile',
            'Satisfaction_Score': 'Patient Satisfaction'
        },
        template='plotly_white'
    )

        fig_scatter.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey'))) 
        fig_scatter.update_layout(title_x=0.0,font=dict(size=14),title_font_size=26)
        st.plotly_chart(fig_scatter,use_container_width=True)


        df_ = df.groupby(['AI_Tool_Type', 'AI_Health_App_Usage_Hours_Per_Week'])['Improvement_Percentage'].mean().reset_index()

        fig = px.density_heatmap(
            df_, 
            x='AI_Health_App_Usage_Hours_Per_Week', 
            y='AI_Tool_Type', 
            z='Improvement_Percentage', 
            histfunc='avg',
            title='Heatmap: AI Usage Hours vs. Tool Type (Avg Improvement %)',
            labels={
                'AI_Health_App_Usage_Hours_Per_Week': 'AI Usage (Hours / Week)', 
                'Improvement_Percentage': 'Avg Improvement (%)',
                'AI_Tool_Type': 'AI Tool'
            },
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.update_layout(title_x=0.0,font=dict(size=14),title_font_size=26)
        st.plotly_chart(fig,use_container_width=True)

    with tab3:
        fig= px.box(
        df,
        x="Total_Engagement_Hours_Per_Week",
        y="Improvement_Percentage",
        labels={
        "Total_Engagement_Hours_Per_Week":"Engagement Hours Per Week",
        "Improvement_Percentage":"Improvement Percentage",
        },
        

        title="Engagement Hours vs Improvement Percentage"
        )
        fig.update_layout(
            title_x=0.1,
            font=dict(size=14),
            title_font_size=26
        )
        fig.update_traces(
            marker_size=5
        )    
        st.plotly_chart(fig,use_container_width=True)


        df_ = df.groupby('Age_Group')[['Health_Score_Before_AI', 'Health_Score_After_AI']].mean().reset_index()

        fig = px.line(
            df_, 
            x='Age_Group', 
            y=['Health_Score_Before_AI', 'Health_Score_After_AI'],
            markers=True,
            color_discrete_sequence=["#E15759", '#4E79A7'],
            title='Average Health Score Before vs. After AI by Age Group',
            labels={'value': 'Mean Health Score', 'variable': 'Stage', 'Age_Group': 'Age Group'},
            template='plotly_dark'
        )
        fig.update_layout(
                    title_x=0.1,
                    font=dict(size=14),
                    title_font_size=26
                )
        st.plotly_chart(fig,use_container_width=True)


        df_= df.groupby(['Chronic_Condition', 'Gender'])['Improvement_Per_AI_Hour'].mean().reset_index()

        fig = px.bar(
            df_, 
            x='Improvement_Per_AI_Hour', 
            y='Chronic_Condition', 
            color='Gender', 
            barmode='group', 
            orientation='h',
            color_discrete_sequence=px.colors.qualitative.Bold,
            title="AI Efficiency by Condition & Gender",
            labels={'Improvement_Per_AI_Hour': 'Avg Improvement Per AI Hour', 'Chronic_Condition': 'Chronic Condition'},
            template='plotly_white'
        )
        fig.update_layout(
            title_x=0.1,
            font=dict(size=14),
            title_font_size=26
        )
        st.plotly_chart(fig,use_container_width=True)   


        df_=df.groupby('Age_Group')[["Improvement_Percentage","Satisfaction_Score","AI_Health_App_Usage_Hours_Per_Week"]].mean().reset_index()

        fig= px.line(
            df_,
            x="Age_Group",
            y=["Improvement_Percentage","Satisfaction_Score"],
            markers= True,
            title="Trends in Improvement % and Satisfaction Score across Age Groups",
            labels={"value":"Average Metric Score","variable":"Health Metrics","Age_Group":"Age Group"},
            color_discrete_sequence=["#2B5C8F","#D95F02"],
            template="plotly_white"
        )
        fig.update_traces(line=dict(width=3),marker=dict(size=9,symbol="circle"))
        fig.update_layout(
            title_x=0.1,
            xaxis_title="Age Group",
            yaxis_title="Average Score / Percentage",
            hovermode="x unified",
            legend=dict(title=None),
            font=dict(size=14),
            title_font_size=26
        )
        st.plotly_chart(fig,use_container_width=True)

    with tab4:
            fig = px.treemap(
            df, 
            path=['BMI_Category', 'AI_Tool_Type'], 
            values='Improvement',
            color='Improvement',
            color_continuous_scale='RdYlGn',
            title='Health Improvement Volume by BMI Category and AI Tool',
            template='plotly_white'
        )
            st.plotly_chart(fig,use_container_width=True)


            fig = px.sunburst(
            df, 
            path=['Gender', 'AI_Tool_Type', 'Satisfaction_Level'], 
            title='Gender -> AI Tool Type -> Satisfaction Level Hierarchy',
            color_discrete_sequence=px.colors.qualitative.Bold,
            
        )
            st.plotly_chart(fig,use_container_width=True)


elif opt == "ℹ️ About & Methodology":
    # Custom CSS for dark cards with refined layout
    st.markdown("""
        <style>
        .about-card {
            background: linear-gradient(145deg, #161b22, #1f242d);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .about-card:hover {
            transform: translateY(-2px);
            border-color: #58a6ff;
        }
        .about-card h3 {
            color: #58a6ff;
            font-size: 1.25rem;
            margin-bottom: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        .about-card p {
            color: #c9d1d9;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        }
        .about-card ul {
            color: #c9d1d9;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0;
            padding-left: 20px;
        }
        .about-card li {
            margin-bottom: 8px;
        }
        .about-card b {
            color: #f0f6fc;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("ℹ️ About & Methodology")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="about-card">
            <h3>📌 Project Overview</h3>
            <p>
                This application analyzes how AI health tools impact daily lifestyle and health outcomes. 
                It helps track health progress, exercise routines, and user satisfaction across different demographics.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>📊 Main Metrics Included</h3>
            <ul>
                <li><b>Demographics:</b> Age groups, gender, and BMI categories</li>
                <li><b>Engagement:</b> AI app usage hours and weekly exercise levels</li>
                <li><b>Impact:</b> Health scores before and after AI adoption</li>
                <li><b>Satisfaction:</b> User feedback and overall risk levels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="about-card">
            <h3>🛠️ How It Works</h3>
            <p>
                The platform runs on a pre-cleaned, structured dataset of 5,000 user records. 
                Key indicators like <b>Improvement Percentage</b> and <b>Satisfaction Scores</b> are calculated 
                directly to measure real-world AI efficiency.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>🎯 Objective</h3>
            <p>
                To provide data-driven insights on how AI tools enhance physical fitness, 
                mental health tracking, and overall medical adherence for users.
            </p>
        </div>
        """, unsafe_allow_html=True)
