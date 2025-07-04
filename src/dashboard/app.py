import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECTION")

# Load data from MongoDB
@st.cache_data
def load_data():
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df

# Load and sanitize data
df = load_data()

# Convert ObjectId to string (to avoid pyarrow issues)
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

# Convert dates
df["lead_created_at"] = pd.to_datetime(df["lead_created_at"], errors="coerce")

# Title
st.title("Panel de Conversión de Campañas")

# Campaign filter
campaign_names = df["name"].dropna().unique().tolist()
selected_campaigns = st.multiselect(
    "Selecciona una o más campañas",
    options=campaign_names,
    default=campaign_names,
)

# Date filter
min_date = df["lead_created_at"].min()
max_date = df["lead_created_at"].max()
start_date, end_date = st.date_input(
    "Selecciona un intervalo de fechas (fecha de creación del lead)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Checkbox for including invalid conversions
include_invalid = st.checkbox("Incluir conversiones inválidas en los gráficos", value=True)

# Apply filters
filtered_df = df[
    (df["name"].isin(selected_campaigns)) &
    (df["lead_created_at"] >= pd.to_datetime(start_date)) &
    (df["lead_created_at"] <= pd.to_datetime(end_date))
]

# Base and numerator for conversion calculation
source_base_df = filtered_df.copy()
source_numerator_df = filtered_df.copy()
campaign_base_df = filtered_df.copy()
campaign_numerator_df = filtered_df.copy()

if not include_invalid:
    source_numerator_df = source_numerator_df[source_numerator_df["conversion_valid"] == True]
    campaign_numerator_df = campaign_numerator_df[campaign_numerator_df["conversion_valid"] == True]

# Metrics layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Leads", len(filtered_df))
with col2:
    valid_conversions = filtered_df["conversion_valid"].sum()
    st.metric("Conversiones Válidas", valid_conversions)
with col3:
    invalid_df = filtered_df[(filtered_df["conversion_valid"] == False) & (filtered_df["converted"] == True)]
    st.metric("Conversiones Inválidas", len(invalid_df))

# Chart 1: Conversions by campaign name
conversion_by_campaign = (
    campaign_numerator_df[campaign_numerator_df["converted"] == True]
    .groupby("name")["converted"].count()
    .reset_index(name="converted")
)
fig1 = px.bar(
    conversion_by_campaign,
    x="name",
    y="converted",
    title="Conversión por Campaña",
    labels={"name": "Campaña", "converted": "Convertidos"},
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Distribution of amount paid by campaign
fig2 = px.box(
    campaign_numerator_df,
    x="name",
    y="amount_float",
    title="Distribución de Monto Pagado por Campaña",
    labels={"name": "Campaña", "amount_float": "Monto (€)"},
)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Types of anomalies by campaign (always valid)
anomalies_df = filtered_df[
    (filtered_df["conversion_anomaly_type"] != "NO_ANOMALY") &
    (filtered_df["converted"] == True)
]
anomaly_counts = anomalies_df.groupby(
    ["name", "conversion_anomaly_type"]
).size().reset_index(name="count")
fig3 = px.bar(
    anomaly_counts,
    x="name",
    y="count",
    color="conversion_anomaly_type",
    title="Tipos de Anomalía por Campaña",
    labels={
        "name": "Campaña",
        "count": "Cantidad",
        "conversion_anomaly_type": "Tipo de Anomalía",
    },
)
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Conversion rate by campaign source (input_channel)
if "input_channel" in df.columns:
    source_conversion = (
        source_base_df.groupby("input_channel")["lead_id"].count().reset_index(name="total_leads")
        .merge(
            source_numerator_df[source_numerator_df["converted"] == True]
            .groupby("input_channel")["converted"].count().reset_index(name="total_converted"),
            on="input_channel",
            how="left"
        )
    )
    source_conversion["conversion_rate"] = (
        source_conversion["total_converted"] / source_conversion["total_leads"] * 100
    )
    fig_source = px.bar(
        source_conversion,
        x="input_channel",
        y="conversion_rate",
        title="Tasa de Conversión por Fuente de Campaña",
        labels={"input_channel": "Fuente de Campaña", "conversion_rate": "Tasa de Conversión (%)"},
    )
    st.plotly_chart(fig_source, use_container_width=True)

# Chart 5: Percentage of conversion by campaign
conversion_rate_by_campaign = (
    campaign_base_df.groupby("name")["lead_id"].count().reset_index(name="total_leads")
    .merge(
        campaign_numerator_df[campaign_numerator_df["converted"] == True]
        .groupby("name")["converted"].count().reset_index(name="total_converted"),
        on="name",
        how="left"
    )
)
conversion_rate_by_campaign["conversion_rate"] = (
    conversion_rate_by_campaign["total_converted"] / conversion_rate_by_campaign["total_leads"] * 100
)
fig_conv_pct = px.bar(
    conversion_rate_by_campaign,
    x="name",
    y="conversion_rate",
    title="Porcentaje de Conversión de Leads por Campaña",
    labels={"name": "Campaña", "conversion_rate": "Tasa de Conversión (%)"},
)
st.plotly_chart(fig_conv_pct, use_container_width=True)

# Funnel chart: conversion evolution
converted_df = campaign_numerator_df[campaign_numerator_df["converted"] == True]
funnel_fig = go.Figure(go.Funnel(
    y=["Leads", "Convertidos"],
    x=[len(campaign_base_df), len(converted_df)],
    textinfo="value+percent previous"
))
funnel_fig.update_layout(title="Embudo de Conversión")
st.plotly_chart(funnel_fig, use_container_width=True)