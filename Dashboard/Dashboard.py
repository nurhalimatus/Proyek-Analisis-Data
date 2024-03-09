import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_sharing(df):
    sumshare_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    sumshare_df = sumshare_df.reset_index()
    return sumshare_df

def create_monthly_sharing(df):
    df_2011 = df[df['dteday'].dt.year == 2011]
    monthlyshare_df = df_2011.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
        "windspeed": "mean",
        "weathersit": "mean"
    })
    
    monthlyshare_df.index = monthlyshare_df.index.strftime('%B %Y')
    monthlyshare_df.reset_index(inplace=True)  
    return monthlyshare_df

def create_weathersit(df):
    weathersit_df = df.groupby(by="weathersit").agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return weathersit_df

def create_windspeed(df):
    windspeed_df = df.groupby(by="windspeed").agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return windspeed_df

clean_df = pd.read_csv("https://raw.githubusercontent.com/Diahnhs/Projek-Analisa-Data/main/Dashboard/main_data.csv?token=GHSAT0AAAAAACPJKHYD53EIRTUYVF3H7JAYZPMDW2Q")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

with st.sidebar:
    st.subheader("Filter data")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

sumsharing_df = create_sum_sharing(main_df)
monthlysum_df = create_monthly_sharing(main_df)
byweathersit_df = create_weathersit(main_df)
byhwindspeed_df = create_windspeed(main_df)

st.header("Bike Sharing")

# menampilkan grafik berdasarkan cuaca
st.subheader("Performance based on weather")
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(3)
width = 0.20
ax.bar(x - width / 2, byweathersit_df['casual'], width)
ax.bar(x + width / 2, byweathersit_df['registered'], width)
ax.set_xticks(x + 0, (["Clear,\nFew clouds,\nPartly cloudy",
                     "Mist + Cloudy,\nMist + Broken clouds,\nMist + Few clouds,\nMist",
                     "Light Snow,\nLight Rain + Thunderstorm\n+ Scattered clouds,\nLight Rain + Scattered clouds"]))
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

#menampilkan grafik penyewaan sepeda berdasarkan cuaca dan angin setiap bulan
st.subheader("Monthly Bike Sharing based on weathersit and windspeed")
fig, ax = plt.subplots(figsize=(10, 5))
x = monthlysum_df['dteday']
ax.plot(x, monthlysum_df['windspeed'], marker='o')  
ax.plot(x, monthlysum_df['weathersit'], marker='o') 
ax.tick_params(axis='x', rotation=90)
ax.legend(["windspeed", "weathersit"])
st.pyplot(fig)