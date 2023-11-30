import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict

st.title("Dashboard Air Quality :sparkles:")

task1, task2, task3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3"])
df = pd.read_csv("dashboard/main_data.csv")
stasiun = df["station"].unique()


def senyawa_kadar_visualisasi(senyawa):
    stasiun_kadar = {
        stasiun[i]: df[df["station"] == stasiun[i]][senyawa].mean()
        for i in range(len(stasiun))
    }

    stasiun_max = max(stasiun_kadar, key=stasiun_kadar.get)
    max_val = stasiun_kadar[stasiun_max]
    sorted_stasiun_kadar = OrderedDict(
        sorted(stasiun_kadar.items(), key=lambda x: x[1])
    )
    fig, ax = plt.subplots()
    ax.bar(
        list(sorted_stasiun_kadar.keys()),
        list(sorted_stasiun_kadar.values()),
        color="blue",
        width=0.5,
    )
    ax.set_title(f"AVG Polutan {senyawa} di setiap stasiun")
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Rata-rata Polutan")
    ax.set_xticklabels(list(sorted_stasiun_kadar.keys()), rotation=45, ha="right")

    st.pyplot(fig)

    st.subheader("Hasil analisa:")
    st.caption(
        f"Polutan {senyawa} tertinggi pada Stasiun: {stasiun_max} dengan nilai: {round(max_val, 2)}"
    )


def task2_season(stations):
    tren_pm25 = (
        df.groupby(by=["station", "year", "Musim"])
        .agg(
            {
                "PM2.5": "mean",
            }
        )
        .reset_index()
    )

    all_years = tren_pm25["year"].unique()
    all_color = ["chocolate", "maroon", "green", "blue", "indigo"]
    all_season = tren_pm25["Musim"].unique()

    fig, ax = plt.subplots()

    for i, year in enumerate(all_years):
        color = all_color[i]
        data = tren_pm25[
            (tren_pm25["station"] == stations) & (tren_pm25["year"] == year)
        ]

        year_seasons = data["Musim"]
        values = data["PM2.5"]

        ax.plot(year_seasons, values, marker="o", color=color, label=year)

    ax.set_xlabel("Season")
    ax.set_ylabel("Value")
    ax.set_title(f"PM2.5 Line Plot Stasiun {stations}")
    st.pyplot(fig)


def task3_corr():
    fig, ax = plt.subplots()
    ax.scatter(df["PM2.5"], df["PM10"])
    ax.set_xlabel("PM2.5")
    ax.set_ylabel("PM10")
    ax.set_title("Scatter Plot PM2.5 vs PM10")
    st.pyplot(fig)

    # Korelasi
    correlation = df["PM2.5"].corr(df["PM10"])
    st.subheader(f"Koefisien Korelasi antara PM2.5 dan PM10: {correlation}")
    st.caption(
        "ini menunjukkan bahwa terdapat hubungan positif yang kuat antara kedua variabel tersebut. Artinya, ketika nilai PM2.5 meningkat, nilai PM10 juga cenderung untuk meningkat, dan sebaliknya. Pola ini cenderung mengikuti tren yang sama."
    )


with task1:
    st.header("Bagaimana Kualitas Udara pada setiap variabel di setiap stasiun?")

    st.subheader("Chart: ")
    option = st.radio("Pilih opsi:", ("PM2.5", "PM10", "SO2", "NO2", "CO", "O3"))
    senyawa_kadar_visualisasi(option)


with task2:
    st.header("Bagaimana tren musiman dari PM2.5?")

    st.subheader("Chart")

    all_season = df["station"].unique()

    option = st.radio("Pilih Stasiun:", tuple(all_season))
    task2_season(option)

with task3:
    st.header("Apakah terdapat korelasi antara PM2.5 terhadap PM10?")

    st.subheader("Korelasi")

    task3_corr()
