#! /usr/bin/env python3

#libraries
import pandas as pd
import numpy as np

##Read dataset
df = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')


##Clean dataset
#check duplicates and null
print('num of null=',sum(df.isnull().any()))
print('num of dupl=',sum(df.duplicated()))
#check identification columns
print('dupl of Pa ID=',sum(df['PatientId'].duplicated())/df.shape[0],'%')
print('dupl of App ID=',sum(df['AppointmentID'].duplicated())/df.shape[0],'%')
df.drop(columns=['AppointmentID'],axis=1,inplace=True)
#rename columns
df.rename(columns={'PatientId':'Patient_Id','ScheduledDay':'Scheduled_Day','AppointmentDay':'Appointment_Day',
                    'Hipertension':'Hypertension','Handcap':'Handicap'},inplace=True)
df.rename(columns=lambda x: x.strip().lower().replace('-','_'),inplace=True)


##Change datatype
df['patient_id'] = df['patient_id'].apply(lambda x: str(int(x)))
df['scheduled_day'] = pd.to_datetime(df['scheduled_day']) #str -> timestamp
df['appointment_day'] = pd.to_datetime(df['appointment_day']) #str -> timestamp
df['no_show'] = df['no_show']=='Yes' #str -> bool
df['male'] = df['gender']=='M' #str -> bool
columns = ['scholarship','hypertension','diabetes','handicap','alcoholism','sms_received']
for c in columns:
    df[c] = df[c].astype(bool) #int -> bool


##Split shows and no_shows
#split dataset
df_show = df.query('no_show == False').drop(columns=['no_show'],axis=1)
df_show.to_csv('show.csv',index=False)
df_noshow = df.query('no_show == True').drop(columns=['no_show'],axis=1)
df_noshow.to_csv('noshow.csv',index=False)

