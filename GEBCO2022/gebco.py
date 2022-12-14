from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
######0. User dependent definition######
#ds.close()
outf='test.asc'
ds = Dataset('../GEBCO_2022_org.nc')  # 2022 15arc grid https://www.gebco.net/data_and_products/gridded_bathymetry_data/

enable_write=1 #1: write 2: NOT write

lonmin=129.0
lonmax=130.0
latmin=34.0
latmax=35.0

###############DO NOT CHANGE BELLOW AS POSSIBLE###################
######1. calc index of lons and lats######

xmin=0; xmax=0; ymin=0; ymax=0; elvmin=0; elvmax=0

lon =ds.variables['lon'][:]
lat =ds.variables['lat'][:]

k=0;
for i in range(len(lon)):
    k = k + 1
    if  (lon[i] <= lonmin) and (lon[i+1] >= lonmin):
        xmin = k 
    elif  (lon[i] <= lonmax) and (lon[i+1] >= lonmax):
        xmax = k 
        break;

l=0;
for j in range(len(lat)):
    l = l + 1  
    if  (lat[j] <= latmin) and (lat[j+1] >= latmin):
        ymin = l 
    elif  (lat[j] <= latmax) and (lat[j+1] >= latmax):
        ymax = l
        break;

datanum=(xmax-xmin+1)*(ymax-ymin+1)

print('Lonmin',xmin,'Lonmax', xmax,'Latmin', ymin,'Latmax', ymax, 'N',datanum)

######2. Read Elevation#########    
print('2. Read Elevation')

lons =ds.variables['lon'][xmin:xmax+1]
lats =ds.variables['lat'][ymin:ymax+1]
elv =ds.variables['elevation'][ymin:ymax+1,xmin:xmax+1]

print('Lon_len',len(lons),'Lat_len',len(lats), 'Size_elv', (np.array(elv)).shape)
ds.close()

######3. Store variables######
print('3. Store variables faster') 
start = time.time()
lons_all = np.array([])
lons2 = np.array(lons)
for i in range(len(lats)):
    lons_all = np.append(lons_all, lons)

print('lons check',lons_all)
print('lons processing time: ',time.time() - start)
start2 = time.time()

lats_new = np.array([])
lats2 = np.array(lats)
for j in range(len(lats)):
    lats_fix = lats[j]
    if j%100==0:
        print(j/len(lats)*100, ' % DONE')
    for k in range(len(lons)):
        lats_new = np.append(lats_new, lats_fix)
print('lats check',lats_new)
print('lats processing time: ',time.time() - start2)

elv2 = np.array(elv)
elv2 = elv2.astype(int)
elv2 = np.reshape(elv2, (datanum,))
print('lons ',lons_all.shape,',lats ', lats_new.shape,',elvs ', elv2.shape)

con = np.array([])
con = np.concatenate((con, lons_all))
con = np.concatenate((con, lats_new))
con = np.concatenate((con, elv2))
con = con.reshape(3,len(lons)*len(lats)).T
print(con)

######4. Output######

print('4. Output')

if enable_write==1:
    np.savetxt(outf, con, fmt=["%.5f", "%.5f", "%.0f"], delimiter='   ')
    print('Output file was created')
else: 
    print('Warning: Output file was not created')

cont=plt.contourf(lons, lats, elv)
plt.colorbar(cont)
plt.savefig('elv_30-35.png')

print('Finished')

