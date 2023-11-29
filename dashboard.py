import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT97SgReqxgpkm73G18eGyY7NMKHbSfP9lBmMQia3VW1rZvrT9lvl_r3ub0RLq5t8gPJbzUJyLCsRCB/pub?gid=1139900285&single=true&output=csv'
all_df = pd.read_csv('all.csv')



#konversi fitur tahun, bulan, hari, jam ke satuan fitur tanggal
date = pd.to_datetime(all_df[['year','month','day','hour']])
date = date.apply(lambda x: x)
all_df['date'] = date


min_date = all_df["date"].min()
max_date = all_df["date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://repository-images.githubusercontent.com/452943160/e1d07b82-4391-479d-9f3e-eb74ff4e15f5")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

print(start_date)

main_df = all_df[(all_df['date'] >= str(start_date)) & (all_df['date'] <= str(end_date)) ]


st.header('Dashboard Kualitas Udara :cloud:')

st.subheader('Total Populasi Udara')

col1 ,col2 ,col3 = st.columns(3)
col4 ,col5 ,col6 = st.columns(3)

with col1:
    pm25 = round(main_df['PM2.5'].sum(),0)
    st.metric('PM2.5', value=pm25)
with col2:
    pm10 = round(main_df['PM10'].sum(),0)
    st.metric('PM10', value=pm25)
with col3:
    no2 = round(main_df['NO2'].sum(),0)
    st.metric('NO2', value=no2)
with col4:
    so2 = round(main_df['SO2'].sum(),0)
    st.metric('SO2', value=so2)
with col5:
    co = round(main_df['CO'].sum(),0)
    st.metric('CO', value=co)
with col6:
    o3= round(main_df['O3'].sum(),0)
    st.metric('O3', value=o3)

st.subheader('Kualitas Udara dari waktu ke waktu')

parameters = ['PM2.5','PM10','SO2','NO2','CO','O3',]

# Konversi Kolom Date menjadi objek
main_df['date'] = pd.to_datetime(main_df['date'])

# membuat 3x2 subplot
fig, ax = plt.subplots(3, 2, figsize=(15, 12))

# list kosong untuk menampung Legend dan label
legend_handles = []

# Loop through the parameters and create subplots
for i, param in enumerate(parameters):
    row = i // 2  # Row index (0, 0, 1, 1, 2, 2)
    col = i % 2   # Column index (0, 1, 0, 1, 0, 1)

    if (start_date.year == end_date.year) & (start_date.month == end_date.month):
        grup_data = main_df.groupby([main_df['date'].dt.to_period("D"), 'station'])[param].mean().unstack()
    else:
        grup_data = main_df.groupby([main_df['date'].dt.to_period("M"), 'station'])[param].mean().unstack()
            
    index_bulan = grup_data.index.to_timestamp()  # konversi index menjadi seris data waktu
    for statiun in grup_data.columns:
        line, = ax[row, col].plot(index_bulan, grup_data[statiun],linestyle='--',linewidth='1.5',label=statiun)
        if row == 0 and col == 0:
            legend_handles.append(line)

    ax[row, col].set_title(param)
    ax[row, col].grid(True)
    ax[row, col].tick_params(axis='x', rotation=45)
    

    # membuat legend
    if row == 0 and col == 1:
        ax[row, col].legend(handles=legend_handles, loc='best', bbox_to_anchor=(1, 1), title='Stations')

# atur layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the subplots
st.pyplot(fig)

st.subheader('Statiun Penyumbang Populasi Tertinggi')

# membuat 3x2 subplot
fig, ax = plt.subplots(3, 2, figsize=(19, 13))


for i, param in enumerate(parameters):
    row = i // 2  # Row index (0, 0, 1, 1, 2, 2)
    col = i % 2   # Column index (0, 1, 0, 1, 0, 1)
    
    
    grup_data = main_df.groupby('station')[param].mean().reset_index()
    sns.barplot(
        data=grup_data.sort_values(param, ascending=False),
        x=param,
        y='station',
        #hue='station',
        #estimator='max',
        palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
        ax=ax[row, col]
    )
    
    
    ax[row, col].set_title(param)
    ax[row, col].set_xlabel(None)
    ax[row, col].set_ylabel(None)
    ax[row, col].tick_params(axis='y')

    
st.pyplot(fig)

st.caption('Copyright (c) 2023')
