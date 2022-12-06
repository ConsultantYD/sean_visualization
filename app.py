import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.title("Water Test Results")

metal_cols = ["Copper", "Iron", "Zinc", "Manganese", "Lead"]

#df = pd.read_excel("sean_db_clean.xlsx")
#clean_data = clean_dataframe(df)
clean_data = pd.read_csv("clean_data.csv")

years_list = np.unique(clean_data.Year.values)
clean_years_list = years_list[~np.isnan(years_list)].astype(int)

st.subheader("General Settings")
col01, col02 = st.columns((4, 2))
years = col01.multiselect("Select desired years",
                          clean_years_list, clean_years_list)
q_min, q_max = col02.select_slider("Quantile Selection", value=[
                                   5, 95], options=range(0, 101))
min_val = clean_data.quantile(q_min / 100)
max_val = clean_data.quantile(q_max / 100)
data = clean_data
data = data[(data >= min_val) & (data <= max_val)].dropna()

data = data[(data["Year"].isin(years))]

description = data[metal_cols].describe()

st.subheader("Statistics")
_, col_center, _ = st.columns((1, 3, 1))
col_center.write(description.iloc[1:])

st.subheader("Histogram")
columns = st.multiselect("Select metals", metal_cols, metal_cols[0])
fig1 = px.histogram(data[columns], marginal='box', opacity=1)
st.plotly_chart(fig1)