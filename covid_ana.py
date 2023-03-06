# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 06:43:22 2023

@author: YASUHARA Wataru
"""

import base_extract_correlation_minimum_method as becmm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データ欠損がない前提です

daily_new_patient_pd = pd.read_csv("usecase_data\\covid\\newly_confirmed_cases_daily.csv")
daily_requiring_inpatient_care_pd = pd.read_csv("usecase_data\\covid\\requiring_inpatient_care_etc_daily.csv")
daily_severe_cases_pd = pd.read_csv("usecase_data\\covid\\severe_cases_daily.csv")
daily_deaths_cumulative_pd = pd.read_csv("usecase_data\\covid\\deaths_cumulative_daily.csv")

pref_column = 'ALL'
pref_column_care = '(ALL) Requiring inpatient care'

# all span 1d analysis
daily_new_patient = np.array(daily_new_patient_pd[pref_column])
daily_requiring_inpatient_care = np.array(daily_requiring_inpatient_care_pd[pref_column_care])
daily_severe_cases = np.array(daily_severe_cases_pd[pref_column])
daily_deaths_cumulative = np.array(daily_deaths_cumulative_pd[pref_column])
daily_deaths = daily_deaths_cumulative[:-1] - daily_deaths_cumulative[1:]

# get date
daily_new_patient_date = np.array(daily_new_patient_pd['Date'])
daily_requiring_inpatient_care_date = np.array(daily_requiring_inpatient_care_pd['Date'])
daily_severe_cases_date = np.array(daily_severe_cases_pd['Date'])
daily_deaths_cumulative_date = np.array(daily_deaths_cumulative_pd['Date'])[:-1]

# """
# analysis
freq_new_patient = becmm.freq_analysis_1D(daily_new_patient)
freq_requiring_inpatient_care = becmm.freq_analysis_1D(daily_requiring_inpatient_care)
freq_severe_cases = becmm.freq_analysis_1D(daily_severe_cases)
freq_deaths = becmm.freq_analysis_1D(daily_deaths)
spans = np.arange(1,freq_new_patient.shape[0])

# make figure
min_data_num = 515
#fig, ax = plt.subplots(4, 1, sharex="all", figsize=(6, 5),tight_layout=True)
fig, ax = plt.subplots(4, 1, figsize=(6, 5),tight_layout=True)
plt.rcParams['font.family'] = 'MS Gothic'
fig.suptitle("2020/05/09以降の感染者データの周期")
ax[0].set_title('新規患者数周期')
ax[0].plot(spans[:min_data_num],freq_new_patient[:min_data_num])
ax[0].set_xticks(spans[::30])
ax[1].set_title('要入院患者数周期')
ax[1].plot(spans[:min_data_num],freq_requiring_inpatient_care[:min_data_num])
ax[1].set_xticks(spans[::30])
ax[2].set_title('重症患者数周期')
ax[2].plot(spans[:min_data_num],freq_severe_cases[:min_data_num])
ax[2].set_xticks(spans[::30])
ax[3].set_title('死亡者数周期')
ax[3].plot(spans[:min_data_num],freq_deaths[:min_data_num])
ax[3].set_xticks(spans[::30])

plt.show()
# """

# freq change analysis
window_size = 400
timeseries_freq_new_patient = []
timeseries_freq_requiring_inpatient_care = []
timeseries_freq_severe_cases = []
timeseries_freq_deaths = []

for i in range(0,freq_severe_cases.shape[0]-window_size):
    daily_new_patient_temp = daily_new_patient[i:i+window_size]
    daily_requiring_inpatient_care_temp = daily_new_patient[i:i+window_size]
    daily_severe_cases_temp = daily_new_patient[i:i+window_size]
    daily_deaths_temp = daily_new_patient[i:i+window_size]
    
    timeseries_freq_new_patient.append(becmm.freq_analysis_1D(daily_new_patient_temp))
    timeseries_freq_requiring_inpatient_care.append(becmm.freq_analysis_1D(daily_requiring_inpatient_care_temp))
    timeseries_freq_severe_cases.append(becmm.freq_analysis_1D(daily_severe_cases_temp))
    timeseries_freq_deaths.append(becmm.freq_analysis_1D(daily_deaths_temp))


timeseries_freq_new_patient = np.array(timeseries_freq_new_patient)
timeseries_freq_requiring_inpatient_care = np.array(timeseries_freq_requiring_inpatient_care)
timeseries_freq_severe_cases = np.array(timeseries_freq_severe_cases)
timeseries_freq_deaths = np.array(timeseries_freq_deaths)

print(timeseries_freq_new_patient.shape)
print(timeseries_freq_requiring_inpatient_care.shape)
print(timeseries_freq_severe_cases.shape)
print(timeseries_freq_deaths.shape)


# make figure
days_max = min_data_num*2 - window_size -1

fig, ax = plt.subplots(4, 1, sharex="all", figsize=(6, 5),tight_layout=True)
#fig, ax = plt.subplots(4, 1, figsize=(6, 5),tight_layout=True)
plt.rcParams['font.family'] = 'MS Gothic'
fig.suptitle("2020/05/09以降の感染者データの周期")
ax[0].set_title('新規患者数周期の変化')
x_0,y_0 = np.meshgrid(daily_new_patient_date,np.arange(1,timeseries_freq_new_patient.shape[1]))
ax[0].pcolor(x_0,y_0,timeseries_freq_new_patient.T)
ax[1].set_title('要入院患者数周期の変化')
x_1,y_1 = np.meshgrid(daily_requiring_inpatient_care_date,np.arange(1,timeseries_freq_requiring_inpatient_care.shape[1]))
ax[1].pcolor(x_1,y_1,timeseries_freq_requiring_inpatient_care.T)
ax[2].set_title('重症患者数周期の変化')
x_2,y_2 = np.meshgrid(daily_severe_cases_date,np.arange(1,timeseries_freq_severe_cases.shape[1]))
ax[2].pcolor(x_2,y_2,timeseries_freq_severe_cases.T)
ax[3].set_title('死亡者数周期の変化')
x_3,y_3 = np.meshgrid(daily_deaths_cumulative_date,np.arange(1,timeseries_freq_deaths.shape[1]))
ax[3].pcolor(x_3,y_3,timeseries_freq_deaths.T)
fig.autofmt_xdate()

plt.show()
# """


