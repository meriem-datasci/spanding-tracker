import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Spending Calculator", page_icon="💸", layout="centered")

st.title("💸 Predict Your Spending")
st.write("Enter your daily/weekly habits to see how much you spend monthly and yearly in Algerian Dinar (DZD), and discover how much you can save.")

# Store habits in session
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Input form
with st.form("expense_form", clear_on_submit=True):
    name = st.text_input("🔖 Expense Name")
    unit_cost = st.number_input("💲 Unit cost (DZD)", min_value=0.0, format="%.2f")
    times_per_day = st.number_input("⏱ Times per day", min_value=1, step=1)
    days_per_week = st.number_input("📅 Days per week", min_value=1, max_value=7)
    weeks_per_month = st.number_input("📆 Weeks per month", min_value=1, max_value=5)
    months_per_year = st.number_input("🗓 Months per year", min_value=1, max_value=12)

    submitted = st.form_submit_button("➕ Add Expense")
    if submitted and name:
        monthly = unit_cost * times_per_day * days_per_week * weeks_per_month
        yearly = monthly * months_per_year
        st.session_state.expenses.append({
            "Name": name,
            "Monthly": monthly,
            "Yearly": yearly
        })
        st.success(f"✅ Added {name}: {monthly:.2f} DZD/month , {yearly:.2f} DZD/year")

# If expenses exist
if st.session_state.expenses:
    st.subheader("📊 Results")

    df = pd.DataFrame(st.session_state.expenses)

    # Table
    st.dataframe(df.style.format({"Monthly": "{:.2f} DZD", "Yearly": "{:.2f} DZD"}))

    # Totals
    total_monthly = df["Monthly"].sum()
    total_yearly = df["Yearly"].sum()

    st.metric("💵 Total Monthly Spending", f"{total_monthly:.2f} DZD")
    st.metric("💰 Total Yearly Spending", f"{total_yearly:.2f} DZD")

    # 🔹 Saving scenarios
    st.subheader("💡 Saving Scenarios")
    chosen = st.selectbox("Choose a habit to test savings", df["Name"])

    col1, col2 = st.columns(2)

    with col1:
        reduce_factor = st.slider("Reduce habit by (%)", 0, 100, 50, step=10)
    with col2:
        remove = st.checkbox("❌ Remove this habit completely")

    # Calculate savings
    habit = df[df["Name"] == chosen].iloc[0]
    if remove:
        saved_monthly = habit["Monthly"]
        saved_yearly = habit["Yearly"]
        st.success(f"🚫 By removing **{chosen}**, you save: {saved_monthly:.2f} DZD/month = {saved_yearly:.2f} DZD/year")
    else:
        saved_monthly = habit["Monthly"] * (reduce_factor / 100)
        saved_yearly = habit["Yearly"] * (reduce_factor / 100)
        st.success(f"✂️ By reducing **{chosen}** by {reduce_factor}%, you save: {saved_monthly:.2f} DZD/month = {saved_yearly:.2f} DZD/year")

    # Pie chart
    st.write("### 🔵 Distribution of Monthly Spending")
    fig1, ax1 = plt.subplots()
    ax1.pie(df["Monthly"], labels=df["Name"], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Bar chart
    st.write("### 📊 Monthly vs Yearly Spending")
    fig2, ax2 = plt.subplots()
    df.plot(kind="bar", x="Name", y=["Monthly", "Yearly"], ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Reset button
    if st.button("♻️ Reset All Expenses"):
        st.session_state.expenses = []
        st.warning("All expenses have been reset.")
else:
    st.info("ℹ️ Add at least one habit to see the results")
