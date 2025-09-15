import streamlit as st
import pandas as pd
import altair as alt

# Titel van dashboard
st.title("📊 Israëlisch-Palestijns Conflict Dashboard")
st.write("Data over slachtoffers in het Israëlisch-Palestijns conflict (2000–2023).")

# Data inladen
df = pd.read_csv("data.csv")

# Eerste check
st.subheader("Dataset voorbeeld")
st.write(df.head())

# Selectie per jaar
years = df["year"].unique()
year_selected = st.slider("Kies een jaar:", int(df["year"].min()), int(df["year"].max()), int(df["year"].max()))

df_year = df[df["year"] == year_selected]

# Plot maken
chart = (
    alt.Chart(df_year)
    .mark_bar()
    .encode(
        x="side",  # bv. Israeli / Palestinian
        y="fatalities",
        color="side"
    )
)

st.subheader(f"Slachtoffers in {year_selected}")
st.altair_chart(chart, use_container_width=True)

# Totaal aantal slachtoffers
st.subheader("📌 Totaal aantal slachtoffers per jaar")
chart_total = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="year:O",
        y="fatalities:Q",
        color="side"
    )
)
st.altair_chart(chart_total, use_container_width=True)
