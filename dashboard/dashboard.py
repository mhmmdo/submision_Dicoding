import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#line 16 : helper function
#line 35 : menyiapkan dataset
#line 41 : filter data
#line 67 : visualisasi pertama
#line 96 : visualisasi kedua
#line 141: visualisasi ketiga


#menyiapkan helper function untuk dataframe
def create_daerah_df(df):
    daerah_df = df.groupby("kolom_station").index_AQI.sum().sort_values(ascending=False).reset_index()
    return daerah_df

def create_Viklim_mean_df(df):
    Viklim_mean_df= df.groupby(by="kualitas_udara").agg({
        "kolom_TEMP": ['mean'],
        "kolom_PRES" : ['mean'],
        "kolom_DEWP" : ['mean'],
        "kolom_WSPM" : ['mean']
    })
    Viklim_mean_df = Viklim_mean_df.T
    return Viklim_mean_df

def create_df_time(df):
    df_time= df
    return df_time

#menyiapkan dataset
df_AQI=pd.read_csv("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding/main/dashboard/df_AQI.csv")
df_AQI.sort_values(by="kolom_datetime")
df_AQI.reset_index(inplace=True)
df_AQI["kolom_datetime"]=pd.to_datetime(df_AQI["kolom_datetime"])

#filter data
min_date = df_AQI["kolom_datetime"].min()
max_date = df_AQI["kolom_datetime"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding/main/dashboard/Air%20Quality%20Index.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_AQI[(df_AQI["kolom_datetime"] >= str(start_date)) & 
                (df_AQI["kolom_datetime"] <= str(end_date))]

daerah_df = create_daerah_df(main_df)
Viklim_mean_df = create_Viklim_mean_df(main_df)
time_df = create_df_time(main_df)

#membuat header dashboard
st.header('Air Quality Index dashboard :cloud:')

st.subheader("Best & Worst Air Quality Index (AQI)")
#membuat subplot grid
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

#membuat template color untuk visualisasi
colors1 = ["#00FF00" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]
colors2 = ["#1E90FF" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]

#membuat barplot dengan inisialisasi ax[0]
sns.barplot(x="index_AQI", y="kolom_station", data=daerah_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Air Quality Index (AQI)", loc="center", fontsize=30)
ax[0].tick_params(axis ='y', labelsize=20)
ax[0].tick_params(axis ='x', labelsize=20)

#membuat barplot dengan inisialisasi ax[1]
sns.barplot(x="index_AQI", y="kolom_station", data=daerah_df.sort_values(by="index_AQI", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Air Quality Index (AQI)", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis ='x', labelsize=20)

st.pyplot(fig)

st.subheader("Average variable Iklim")

col1, col2, col3, col4= st.columns(4)

with col1:
    mean_temp = round(Viklim_mean_df.T.kolom_TEMP.mean(), 2)
    st.metric("Avarage TEMP", value=mean_temp)

with col2:
    mean_pres = round(Viklim_mean_df.T.kolom_PRES.mean(), 2)
    st.metric("Avarage PRES", value=mean_pres)

with col3:
    mean_dewp = round(Viklim_mean_df.T.kolom_DEWP.mean(), 2)
    st.metric("Avarage DEWP", value=mean_dewp)

with col4:
    mean_wspm = round(Viklim_mean_df.T.kolom_WSPM.mean(), 2)
    st.metric("Avarage WSPM", value=mean_wspm)

species = ("TEMP", "PRES", "DEWP", "WSPM") 

#mengatur posisi, lebar, & jarak setiap bar
x = np.arange(len(species))
width = 0.25
multiplier = 1

fig, ax = plt.subplots(layout='constrained') #membuat subplot grid

#looping untuk mengisi subplot grid dengan plots
for attribute, measurement in Viklim_mean_df.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=4, rotation=30)
    multiplier += 1

# Menambah text, title,& label
ax.set_ylabel('Mean')
ax.set_title('Pengaruh TEMP, WSPM, PRES, & DEWP')
ax.set_xticks(x + width, species)
ax.legend(loc='upper left', ncols=4)
ax.set_ylim(-2, 45)

st.pyplot(fig)

st.subheader("Air Quality Index by variable time")

col1, col2, col3, col4= st.columns(4)

with col1:
    max_year = time_df.groupby(by= "kolom_year").index_AQI.sum().idxmax()
    st.metric("Best Year", value=max_year)

with col2:
    max_month= time_df.groupby(by= "kolom_month").index_AQI.sum().idxmax()
    st.metric("Best Month", value=max_month)

with col3:
    max_day = time_df.groupby(by= "kolom_day").index_AQI.sum().idxmax()
    st.metric("Best Day", value=max_day)

with col4:
    max_hour = time_df.groupby(by= "kolom_hour").index_AQI.sum().idxmax()
    st.metric("Best Hour", value=max_hour)

cat_var=["kolom_year", "kolom_month", "kolom_day", "kolom_hour"] #membuat list untuk label attribute visualisasi

# Membuat subplot grid
fig, ax= plt.subplots(nrows= 2, ncols= int(len(cat_var)/2), figsize= (40,15))

# Looping untuk mengisi subplot grid dengan plots
k= 0
for i in range(2):
    for j in range(int(len(cat_var)/2)):
        sns.barplot(y= time_df.groupby(by= cat_var[k]).index_AQI.sum(),
                    x= time_df.groupby(by= cat_var[k]).mean(numeric_only=True).index, ax= ax[i,j], palette= 'winter')

        ax[i,j].set_title(f'{cat_var[k].upper()}', fontsize= 30)
        ax[i,j].set_ylabel('')
        ax[i,j].set_xlabel('')
        ax[i,j].tick_params(axis='y', labelsize=30)
        ax[i,j].tick_params(axis='x', labelsize=25)
        plt.xticks(rotation=315)
        k+=1

st.pyplot(fig)
