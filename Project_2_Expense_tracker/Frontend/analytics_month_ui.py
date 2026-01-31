import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_month_tab():
    st.title("Expense Breakdown By Category")
    response = requests.get(f"{API_URL}/month_summary/")

    month_data = response.json().get("data", [])


    data_dict = {
        "Month_Number": [m["month_number"] for m in month_data],
        "Month_Name": [m["month_name"] for m in month_data],
        "Total": [m["total"] for m in month_data]
    }

    df = pd.DataFrame(data_dict)
    df_sorted = df.sort_values("Month_Number")

    st.bar_chart(
        data=df.set_index("Month_Name")["Total"],
        use_container_width=True
    )

    st.subheader("Monthly Expense Table")
    st.dataframe(df_sorted)