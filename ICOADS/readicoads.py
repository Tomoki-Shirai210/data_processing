import os
import netCDF4
import numpy as np
import jdutil
from jdutil import date_to_jd


###変数の定義と読み込み
nc = netCDF4.Dataset('ICOADS_R3.0.2_2022-07.nc', 'r')
time = nc.variables['time'][:]
date = nc.variables['date'][:]
hour = nc.variables['HR'][:] 

###日付の設定
year = 2022
smonth = 7
sdate = 15
shour = 12.0
emonth = 7
edate = 15
ehour = 13.0

sdate_inp = sdate + shour/24.0
edate_inp = edate + ehour/24.0

start = date_to_jd(year, smonth, sdate_inp)-2328381
end = date_to_jd(year, emonth, edate_inp)-2328381

print('start', start, 'end', end)

#Julian days since the beginning of the ICOADS record, 
#which is 1662-10-15 12:00:00. Missing values of date (DD in date) are replaced by 0 and missing values in HR are filled with 0.0 in this calculation. See actual values in date, HR for reference." ;

#start ~ end
k=0
for i in range(len(time)):
    k = k + 1
    if (time[i] >= start): # and time[i+1] > start) or (time[i] <= start and time[i] == time[i+1])):
        s_index = k
        break; 
print('s_index=',s_index)

l=0
for i in range(len(time)):
    l = l + 1
    #if l <= len(time)-1: 
    if (time[i] >end): # and time[i+1] > end) or (time[i] <= end and time[i] == time[i+1])):
        e_index = l-2
        break;
#    else:
#        if ((time[i-1] == time[i])):
#            e_index = l 

print('e_index=',e_index)


var1 = nc.variables['lon'][s_index:e_index+1]
var2 = nc.variables['lat'][s_index:e_index+1]
var5 = nc.variables['II'][s_index:e_index+1]
#var6 = nc.variables['ID'][start:end]
var7 = nc.variables['W'][s_index:e_index+1]
var8 = nc.variables['SLP'][s_index:e_index+1]

########################################################################################
###経度、緯度、valの形に変換（For GMT）####################################################
varnum = 3 #Change here
wind = np.concatenate((var1,var2,var7),axis=0) #Change here
rows = int(np.size(wind)/varnum)
print('Ship numbers: ',rows)
### Lon, Lat
wind2 = np.reshape(wind,(varnum,rows))
wind2 = wind2.T
#print(np.shape(wind2))
#print(wind2)
#print(wind2[119][2])
#欠損値は消去
wind3 = []
for i in range(rows):
    if wind2[i][2] != -9999.0:
        wind3.append(wind2[i][0:3])
wind3 = np.array(wind3)
print('wind obs: ',len(wind3))
print(wind3)

###経度、緯度、valの形に変換（For GMT）####################################################
varnum = 3 #Change here
slp = np.concatenate((var1,var2,var8),axis=0) #Change here
rows = int(np.size(slp)/varnum)
slp2 = np.reshape(slp,(varnum,rows))
slp2 = slp2.T
#欠損値は消去
slp3 = []
for i in range(rows):
    if slp2[i][2] != -9999.0:
        slp3.append(slp2[i][0:3])
### Lon, Lat
slp3 = np.array(slp3)
print('press obs: ',len(slp3))
print(slp3)


###経度、緯度、valの形に変換（For GMT）####################################################
varnum = 3 #Change here
var5_2 = np.concatenate((var1,var2,var5),axis=0) #Change here
rows = int(np.size(var5_2)/varnum)
var5_2 = np.reshape(var5_2,(varnum,rows))
var5_2 = var5_2.T
#欠損値は消去
var5_3 = []
for i in range(rows):
    if var5_2[i][2] != -9999.0:
        var5_3.append(var5_2[i][0:3])
### Lon, Lat
var5_3 = np.array(var5_3)
print('II obs: ',len(var5_3))
print(var5_3)

########################################################################################

####書き出し
with open('slp.dat','w') as f:
    np.savetxt(f, slp3, newline='\n', fmt='%s')
f.close()

with open('wind.dat','w') as f:
    np.savetxt(f, wind3, newline='\n', fmt='%s')
f.close()

with open('id_indicator.dat','w') as f:
    np.savetxt(f, var5_3, newline='\n', fmt='%s')
f.close()


#with open('wind.dat','w') as f:
#    np.savetxt(f, np.array(hour[s_index:e_index+1]), newline='\n', fmt='%s')
#f.close()
#

#print(time[s_index:e_index+1])
print('done')

