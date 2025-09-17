import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Titel
st.title("🇮🇱 Israëlisch–Palestijns Conflict Dashboard")
st.write("Data over slachtoffers in het Israëlsch–Palestijns conflict (2000–2023).")

# Data inladen
df = pd.read_csv("data.csv")

# Jaar uit datum halen
df["year"] = pd.to_datetime(df["date_of_event"]).dt.year

# Slider voor jaarkeuze
year_selected = st.slider(
    "Kies een jaar:",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].min())
)

# --- Staafdiagram: slachtoffers per citizenship in gekozen jaar ---
df_year = df[df["year"] == year_selected]
df_year_grouped = df_year.groupby("citizenship").size().reset_index(name="fatalities")

st.subheader(f"Slachtoffers in {year_selected}")
chart = (
    alt.Chart(df_year_grouped)
    .mark_bar()
    .encode(
        x="citizenship",
        y="fatalities",
        color="citizenship"
    )
)
st.altair_chart(chart, use_container_width=True)

# --- Lijnplot: trend door de tijd ---
df_grouped = df.groupby(["year", "citizenship"]).size().reset_index(name="fatalities")

fig_line = px.line(
    df_grouped,
    x="year",
    y="fatalities",
    color="citizenship",
    markers=True,
    title="Aantal slachtoffers per jaar"
)

st.plotly_chart(fig_line, use_container_width=True)









