
import pandas as pd
import streamlit as st

# 🎨 Set Page Title
st.set_page_config(page_title="Data Dashboard", layout="wide")

# 🚀 App Title
st.title("📊 Simple Data Dashboard")

# 📂 File Uploader
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🕒 Convert 'Date' column to datetime if it exists
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 🔄 Remove spaces from column names
    df.columns = df.columns.str.replace(" ", "_")

    # 🎯 Display Dataset Overview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # 📌 Data Summary
    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # 🎛 Data Filtering
    st.subheader("🎚 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("📌 Select column to filter by", columns)

    if df[selected_column].dtype == object:
        unique_values = df[selected_column].dropna().unique()
        selected_value = st.selectbox("🎯 Select value", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
    else:
        min_value, max_value = float(df[selected_column].min()), float(df[selected_column].max())
        selected_value = st.slider(f"🎯 Select range for {selected_column}", min_value, max_value, (min_value, max_value))
        filtered_df = df[(df[selected_column] >= selected_value[0]) & (df[selected_column] <= selected_value[1])]

    st.write(filtered_df)

    # 📈 Data Visualization
    st.subheader("📉 Plot Data")

    # 🔍 Ensure there are numeric columns for plotting
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if numeric_columns:
        x_column = st.selectbox("📍 Select X-axis", df.columns.tolist())  # Allow date selection
        y_column = st.selectbox("📍 Select Y-axis (Numeric Only)", numeric_columns)

        if st.button("📊 Generate Plot"):
            if not filtered_df.empty:
                try:
                    st.line_chart(filtered_df.set_index(x_column)[y_column])
                except KeyError:
                    st.error("⚠️ Please select valid X and Y columns!")
            else:
                st.error("⚠️ Filtered data is empty! Adjust the filters.")
    else:
        st.warning("⚠️ No numeric columns available for plotting. Upload a valid dataset.")

else:
    st.write("📌 Upload a CSV file to begin analysis.")