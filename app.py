import streamlit as st
import pandas as pd
import altair as alt
import ploty.express as px

# Titel
st.title("🇮🇱 Israëlisch–Palestijns Conflict Dashboard")
st.write("Data over slachtoffers in het Israëlisch-Palestijns conflict (2000–2023).")

# Data inladen
df = pd.read_csv("data.csv")

# Maak een kolom 'year' uit de datum
df["year"] = pd.to_datetime(df["date_of_event"]).dt.year

# Selecteer jaar
year_selected = st.slider("Kies een jaar:", int(df["year"].min()), int(df["year"].max()), int(df["year"].max()))
df_year = df[df["year"] == year_selected]

# Data groeperen per citizenship
df_year_grouped = df_year.groupby("citizenship").size().reset_index(name="fatalities")

# Plot maken
chart = (
    alt.Chart(df_year_grouped)
    .mark_bar()
    .encode(
        x="citizenship",
        y="fatalities",
        color="citizenship"
    )
)

st.subheader(f"Slachtoffers in {year_selected}")
st.altair_chart(chart, use_container_width=True)

fig_line = px.line(
    df,
    x="year",                # jaartal
    y="fatalities",          # aantal slachtoffers
    color="citizenship",     # split per Israel/Palestinian
    markers=True,            # bolletjes op de lijn
    title="Aantal slachtoffers per jaar"
)

fig_line.show()











