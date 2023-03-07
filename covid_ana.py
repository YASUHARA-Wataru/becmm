# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 06:43:22 2023

@author: YASUHARA Wataru
"""

import base_extract_correlation_minimum_method as becmm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# データ欠損がない前提です,date_parser=date_parse
daily_new_patient_pd = pd.read_csv("usecase_data\\covid\\newly_confirmed_cases_daily.csv",parse_dates=['Date'])
daily_requiring_inpatient_care_pd = pd.read_csv("usecase_data\\covid\\requiring_inpatient_care_etc_daily.csv",parse_dates=['Date'])
daily_severe_cases_pd = pd.read_csv("usecase_data\\covid\\severe_cases_daily.csv",parse_dates=['Date'])
daily_deaths_cumulative_pd = pd.read_csv("usecase_data\\covid\\deaths_cumulative_daily.csv",parse_dates=['Date'])

pref_column = 'ALL'
pref_column_care = '(ALL) Requiring inpatient care'

# all span 1d analysis
daily_new_patient = np.array(daily_new_patient_pd[pref_column])
daily_requiring_inpatient_care = np.array(daily_requiring_inpatient_care_pd[pref_column_care])
daily_severe_cases = np.array(daily_severe_cases_pd[pref_column])
daily_deaths_cumulative = np.array(daily_deaths_cumulative_pd[pref_column])
daily_deaths = daily_deaths_cumulative[:-1] - daily_deaths_cumulative[1:]

# """
# analysis
freq_new_patient = becmm.freq_analysis_1D(daily_new_patient)
freq_requiring_inpatient_care = becmm.freq_analysis_1D(daily_requiring_inpatient_care)
freq_severe_cases = becmm.freq_analysis_1D(daily_severe_cases)
freq_deaths = becmm.freq_analysis_1D(daily_deaths)
spans = np.arange(1,freq_new_patient.shape[0])

# """
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


for i in range(0,daily_new_patient.shape[0]-2):
    temp = np.zeros(window_size)
    if i+window_size < daily_new_patient.shape[0]:
        e_ind = i+window_size
    else:
        e_ind = daily_new_patient.shape[0]

    temp[:e_ind-i] = daily_new_patient[i:e_ind]
    timeseries_freq_new_patient.append(becmm.freq_analysis_1D(temp))

for i in range(0,daily_requiring_inpatient_care.shape[0]-2):
    temp = np.zeros(window_size)
    if i+window_size < daily_requiring_inpatient_care.shape[0]:
        e_ind = i+window_size
    else:
        e_ind = daily_requiring_inpatient_care.shape[0]
        
    temp[:e_ind-i] = daily_requiring_inpatient_care[i:e_ind]
    timeseries_freq_requiring_inpatient_care.append(becmm.freq_analysis_1D(temp))

for i in range(0,daily_severe_cases.shape[0]-2):
    temp = np.zeros(window_size)
    if i+window_size < daily_severe_cases.shape[0]:
        e_ind = i+window_size
    else:
        e_ind = daily_severe_cases.shape[0]
        
    temp[:e_ind-i] = daily_severe_cases[i:e_ind]
    timeseries_freq_severe_cases.append(becmm.freq_analysis_1D(temp))

for i in range(0,daily_deaths.shape[0]-2):
    temp = np.zeros(window_size)
    if i+window_size < daily_deaths.shape[0]:
        e_ind = i+window_size
    else:
        e_ind = daily_deaths.shape[0]
    
    temp[:e_ind-i] = daily_deaths[i:e_ind]
    timeseries_freq_deaths.append(becmm.freq_analysis_1D(temp))

#timeseries_freq_new_patient = np.array(timeseries_freq_new_patient)
#timeseries_freq_requiring_inpatient_care = np.array(timeseries_freq_requiring_inpatient_care)
#timeseries_freq_severe_cases = np.array(timeseries_freq_severe_cases)
#timeseries_freq_deaths = np.array(timeseries_freq_deaths)

# make figure
# get date
daily_new_patient_date_min = daily_new_patient_pd['Date'].min()
daily_requiring_inpatient_care_date_min = daily_requiring_inpatient_care_pd['Date'].min()
daily_severe_cases_date_min = daily_severe_cases_pd['Date'].min()
daily_deaths_cumulative_date_min = daily_deaths_cumulative_pd['Date'].iloc[:-1].min()

daily_new_patient_date_max = daily_new_patient_pd['Date'].max()
daily_requiring_inpatient_care_date_max = daily_requiring_inpatient_care_pd['Date'].max()
daily_severe_cases_date_max = daily_severe_cases_pd['Date'].max()
daily_deaths_cumulative_date_max = daily_deaths_cumulative_pd['Date'].iloc[:-1].max()


date_min = min([daily_new_patient_date_min,\
                daily_requiring_inpatient_care_date_min,\
                daily_severe_cases_date_min,\
                daily_deaths_cumulative_date_min])

date_max = max([daily_new_patient_date_max,\
                daily_requiring_inpatient_care_date_max,\
                daily_severe_cases_date_max,\
                daily_deaths_cumulative_date_max])

x_date = np.arange(date_min, date_max, datetime.timedelta(days=1))

timeseries_freq_new_patient4plot = np.zeros((len(x_date),int(window_size/2)))
timeseries_freq_requiring_inpatient_care4plot = np.zeros((len(x_date),int(window_size/2)))
timeseries_freq_severe_cases4plot = np.zeros((len(x_date),int(window_size/2)))
timeseries_freq_deaths4plot = np.zeros((len(x_date),int(window_size/2)))

f_index = int((daily_new_patient_date_min - date_min).days)
#timeseries_freq_new_patient4plot[f_index:f_index+timeseries_freq_new_patient.shape[0],:] = timeseries_freq_new_patient
timeseries_freq_new_patient4plot[f_index:f_index+len(timeseries_freq_new_patient),:] = timeseries_freq_new_patient
f_index = int((daily_requiring_inpatient_care_date_min - date_min).days)
#timeseries_freq_requiring_inpatient_care4plot[f_index:f_index+timeseries_freq_requiring_inpatient_care.shape[0],:] = timeseries_freq_requiring_inpatient_care
timeseries_freq_requiring_inpatient_care4plot[f_index:f_index+len(timeseries_freq_requiring_inpatient_care),:] = timeseries_freq_requiring_inpatient_care
f_index = int((daily_severe_cases_date_min - date_min).days)
#timeseries_freq_severe_cases4plot[f_index:f_index+timeseries_freq_severe_cases.shape[0],:] = timeseries_freq_severe_cases
timeseries_freq_severe_cases4plot[f_index:f_index+len(timeseries_freq_severe_cases),:] = timeseries_freq_severe_cases
f_index = int((daily_deaths_cumulative_date_min - date_min).days)
#timeseries_freq_deaths4plot[f_index:f_index+timeseries_freq_deaths.shape[0],:] = timeseries_freq_deaths
timeseries_freq_deaths4plot[f_index:f_index+len(timeseries_freq_deaths),:] = timeseries_freq_deaths

x,y = np.meshgrid(np.arange(1,int(window_size/2)+1),x_date)

fig, ax = plt.subplots(4, 4, sharey="all", figsize=(6, 5),tight_layout=True)
#fig, ax = plt.subplots(4, 1, figsize=(6, 5),tight_layout=True)
plt.rcParams['font.family'] = 'MS Gothic'

fig.suptitle("2020/05/09以降の感染者データの周期")
ax[0][0].set_title('新規患者数周期の変化')
#ax[0][0].pcolor(x,y,timeseries_freq_new_patient4plot.T)
#ax[0][0].plot([x_date[-1]-np.timedelta64(window_size,'D'),x_date[-1]],[int(window_size/2),0])
ax[0][0].pcolor(timeseries_freq_new_patient)
ax[1][0].set_title('要入院患者数周期の変化')
#ax[1][0].pcolor(x,y,timeseries_freq_requiring_inpatient_care4plot.T)
#ax[1][0].plot([x_date[-1]-np.timedelta64(window_size,'D'),x_date[-1]],[int(window_size/2),0])
ax[1][0].pcolor(timeseries_freq_requiring_inpatient_care)
ax[2][0].set_title('重症患者数周期の変化')
#ax[2][0].pcolor(x,y,timeseries_freq_severe_cases4plot.T)
#ax[2][0].plot([x_date[-1]-np.timedelta64(window_size,'D'),x_date[-1]],[int(window_size/2),0])
ax[2][0].pcolor(timeseries_freq_severe_cases)
ax[3][0].set_title('死亡者数周期の変化')
#ax[3][0].pcolor(x,y,timeseries_freq_deaths4plot.T)
#ax[3][0].plot([x_date[-1]-np.timedelta64(window_size,'D'),x_date[-1]],[int(window_size/2),0])
ax[3][0].pcolor(timeseries_freq_deaths)

# """
ax[3][1].set_title('新規患者数周期の変化')
ax[3][1].pcolor(x,y,timeseries_freq_new_patient4plot.T)
ax[0][1].set_title('要入院患者数周期の変化')
ax[0][1].pcolor(x,y,timeseries_freq_requiring_inpatient_care4plot.T)
ax[1][1].set_title('重症患者数周期の変化')
ax[1][1].pcolor(x,y,timeseries_freq_severe_cases4plot.T)
ax[2][1].set_title('死亡者数周期の変化')
ax[2][1].pcolor(x,y,timeseries_freq_deaths4plot.T)

ax[2][2].set_title('新規患者数周期の変化')
ax[2][2].pcolor(x,y,timeseries_freq_new_patient4plot.T)
ax[3][2].set_title('要入院患者数周期の変化')
ax[3][2].pcolor(x,y,timeseries_freq_requiring_inpatient_care4plot.T)
ax[0][2].set_title('重症患者数周期の変化')
ax[0][2].pcolor(x,y,timeseries_freq_severe_cases4plot.T)
ax[1][2].set_title('死亡者数周期の変化')
ax[1][2].pcolor(x,y,timeseries_freq_deaths4plot.T)

ax[1][3].set_title('新規患者数周期の変化')
ax[1][3].pcolor(x,y,timeseries_freq_new_patient4plot.T)
ax[2][3].set_title('要入院患者数周期の変化')
ax[2][3].pcolor(x,y,timeseries_freq_requiring_inpatient_care4plot.T)
ax[3][3].set_title('重症患者数周期の変化')
ax[3][3].pcolor(x,y,timeseries_freq_severe_cases4plot.T)
ax[0][3].set_title('死亡者数周期の変化')
ax[0][3].pcolor(x,y,timeseries_freq_deaths4plot.T)
# """
fig.autofmt_xdate()

plt.show()
# """


