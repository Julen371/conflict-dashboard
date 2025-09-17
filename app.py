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



# Sidebar navigatie
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Kies een pagina", ["Overview", "Alle landen", "Per continent", "Per land"])

# Pagina: Overview
if page == "Overview":
    st.title("📊 Overzicht slachtoffers per jaar")
    df_year = df.groupby("year").size().reset_index(name="fatalities")
    fig = px.line(df_year, x="year", y="fatalities", markers=True, title="Totaal aantal slachtoffers per jaar")
    st.plotly_chart(fig, use_container_width=True)

# Pagina: Alle landen
elif page == "Alle landen":
    st.title("🌍 Slachtoffers per land")
    df_country = df.groupby("citizenship").size().reset_index(name="fatalities")
    fig = px.bar(df_country, x="citizenship", y="fatalities", title="Slachtoffers per land")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_country)

# Pagina: Per continent
elif page == "Per continent":
    st.title("🗺️ Slachtoffers per continent")
    if "continent" in df.columns:   # alleen als je dataset dit heeft
        df_continent = df.groupby("continent").size().reset_index(name="fatalities")
        fig = px.pie(df_continent, values="fatalities", names="continent", title="Verdeling per continent")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_continent)
    else:
        st.warning("Geen continent-kolom gevonden in dataset.")

# Pagina: Per land
elif page == "Per land":
    st.title("🏳️ Slachtoffers per gekozen land")
    landen = df["citizenship"].unique()
    land = st.selectbox("Kies een land", landen)
    df_land = df[df["citizenship"] == land].groupby("year").size().reset_index(name="fatalities")
    fig = px.line(df_land, x="year", y="fatalities", markers=True, title=f"Slachtoffers per jaar in {land}")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_land)









