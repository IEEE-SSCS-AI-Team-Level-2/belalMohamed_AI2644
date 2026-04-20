import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import os

st.set_page_config(page_title="Zara Sales EDA", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('Zara_sales_EDA.csv', sep=';')
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    cols_to_drop = ['product_id', 'url', 'name', 'description', 'product_category', 'brand', 'currency']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    df = df.drop_duplicates()
    df["revenue"] = df["price"] * df["sales_volume"]
    return df

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        default_users = {"admin": "admin123"}
        with open(USER_FILE, "w") as f:
            json.dump(default_users, f)
        return default_users
    
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    if username in users:
        return False
    
    users[username] = password
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
    return True

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 Zara Sales Portal")
    st.markdown("Please log in or create a new account")

    tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            log_user = st.text_input("Username")
            log_pass = st.text_input("Password", type="password")
            
            if st.form_submit_button("Log In"):
                users = load_users()
                if log_user in users and users[log_user] == log_pass:
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

    with tab_signup:
        with st.form("signup_form"):
            new_user = st.text_input("Choose a Username")
            new_pass = st.text_input("Choose a Password", type="password")
            
            if st.form_submit_button("Sign Up"):
                if len(new_user) < 3 or len(new_pass) < 3:
                    st.warning("Username and password must be at least 3 characters long.")
                else:
                    success = save_user(new_user, new_pass)
                    if success:
                        st.success("Account created successfully! You can now log in via the Log In tab.")
                    else:
                        st.error("Username already exists. Please choose a different one.")
    
    st.stop()


df = load_data()

st.sidebar.title("Navigation")

section = st.sidebar.selectbox(
    "Select Section",
    [
        "Overview",
        "Distributions & Outliers",
        "Categorical Impact",
        "Relationships & Revenue",
        "Summary and Conclusion"
    ]
)

st.sidebar.divider()
st.sidebar.button("Log Out", on_click=lambda: st.session_state.update({'authenticated': False}))

st.title("Zara Sales Exploratory Data Analysis")

if section == "Overview":
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", f"{len(df):,}")
    col2.metric("Median Price ($)", f"{df['price'].median():.2f}")
    col3.metric("Avg Sales Volume", f"{df['sales_volume'].mean():.0f}")
    col4.metric("Total Revenue ($)", f"{df['revenue'].sum():,.2f}")

    st.markdown("---")
    st.subheader("Cleaned Data Sample")
    st.dataframe(df.head(10), use_container_width=True)

elif section == "Distributions & Outliers":
    st.header("Analyzing Distributions")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df, x="price", nbins=40, title="Price Distribution", color_discrete_sequence=['teal'])
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.histogram(df, x="sales_volume", nbins=40, title="Sales Volume Distribution", color_discrete_sequence=['coral'])
        st.plotly_chart(fig2, use_container_width=True)
        
    st.header("Outlier Detection")
    fig3 = px.box(df, x="terms", y="price", title="Price Outliers by Product Type (Terms)", color="terms")
    st.plotly_chart(fig3, use_container_width=True)

elif section == "Categorical Impact":
    st.header("How Categories Impact Sales")
    
    col1, col2 = st.columns(2)
    with col1:
        fig4 = px.box(df, x="promotion", y="sales_volume", title="Sales by Promotion", color="promotion")
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        fig5 = px.box(df, x="season", y="sales_volume", title="Sales by Season", color="season")
        st.plotly_chart(fig5, use_container_width=True)

elif section == "Relationships & Revenue":
    st.header("Price vs Sales Volume")
    fig6 = px.scatter(df, x="price", y="sales_volume", hover_data=["revenue", "terms"], 
                      color="season", title="Price vs Sales Volume (Colored by Season)")
    st.plotly_chart(fig6, use_container_width=True)

    st.header("Correlation Matrix")
    corr = df[["price", "sales_volume", "revenue"]].corr()
    fig7, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig7)

elif section == "Summary and Conclusion":
    st.header("Business Strategy & Conclusion")
    
    st.markdown("""
    ### Key Takeaways
    1. **Inventory & Pricing:** The catalog is heavily anchored by affordable items (Median: $35.95), with the `jackets` category dominating the inventory.
    2. **Premium Outliers:** The extreme high-price outliers are clustered in jackets. These represent Zara's premium tier, acting as margin-expanders rather than volume drivers.
    3. **Demand Elasticity:** There is a moderate negative correlation between price and sales volume. As prices increase, demand drops, confirming standard elasticity.
    4. **Revenue Drivers:** While cheap items drive foot traffic, a small subset of high-volume/high-price items generates the bulk of the absolute revenue. 
    """)
    st.info("Thank you for reviewing this Exploratory Data Analysis.")