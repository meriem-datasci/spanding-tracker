import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Spending Tracker", page_icon="💸", layout="centered")

st.title("💸 Spending Tracker (Multiple Habits)")
st.write("Fill in your different habits below. You can add multiple rows at once, and the app will calculate your monthly and yearly spending in Algerian Dinar (DZD).")

# Initial empty table
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame({
        "Name": ["Coffee", "Transport", "Subscription"],  # example defaults
        "Unit Cost (DZD)": [80, 200, 1000],
        "Times/Day": [1, 2, 1],
        "Days/Week": [7, 5, 7],
        "Weeks/Month": [4, 4, 4],
        "Months/Year": [12, 12, 12]
    })

st.write("✍️ Edit or add habits below (you can add as many rows as you want):")

# Editable data grid
df = st.data_editor(
    st.session_state.expenses_df,
    num_rows="dynamic",  # allow adding rows
    use_container_width=True
)

# Save updates
st.session_state.expenses_df = df

# If table is not empty → calculate results
if not df.empty:
    df["Monthly"] = df["Unit Cost (DZD)"] * df["Times/Day"] * df["Days/Week"] * df["Weeks/Month"]
    df["Yearly"] = df["Monthly"] * df["Months/Year"]

    st.subheader("📊 Results")
    st.dataframe(df.style.format({"Monthly": "{:.2f} DZD", "Yearly": "{:.2f} DZD"}))

    total_monthly = df["Monthly"].sum()
    total_yearly = df["Yearly"].sum()

    st.metric("💵 Total Monthly Spending", f"{total_monthly:.2f} DZD")
    st.metric("💰 Total Yearly Spending", f"{total_yearly:.2f} DZD")

    # Pie chart
    st.write("### 🔵 Monthly Spending Distribution")
    fig1, ax1 = plt.subplots()
    ax1.pie(df["Monthly"], labels=df["Name"], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Bar chart
    st.write("### 📊 Monthly vs Yearly Spending")
    fig2, ax2 = plt.subplots()
    df.plot(kind="bar", x="Name", y=["Monthly", "Yearly"], ax=ax2)
    st.pyplot(fig2)

    # Reset button
    if st.button("♻️ Reset All"):
        st.session_state.expenses_df = pd.DataFrame({
            "Name": [],
            "Unit Cost (DZD)": [],
            "Times/Day": [],
            "Days/Week": [],
            "Weeks/Month": [],
            "Months/Year": []
        })
        st.experimental_rerun()
else:
    st.info("ℹ️ Add at least one habit in the table to see the results.")
