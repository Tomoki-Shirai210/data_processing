gmtset BASEMAP_TYPE = plain
gmtset ANNOT_FONT_SIZE_PRIMARY 11p

makecpt -Cpolar -Z -T0/14/2 > wind.cpt
makecpt -Ccool -Z -T980/1020/5 > press.cpt
makecpt -Csplit -T1/12/1 > id_indicator.cpt


pscoast -R-179/179/-85/85 -JQ18 -W1 -P -Di -Ggray -Swhite -Ba20f20g20WseN -K > mapwind.ps
pscoast -R-179/179/-85/85 -JQ18 -W1 -P -Di -Ggray -Swhite -Ba20f20g20WseN -K > mapslp.ps
pscoast -R-179/179/-85/85 -JQ18 -W1 -P -Di -Ggray -Swhite -Ba20f20g20WseN -K > mapid_indicator.ps


psxy wind.dat -R-179/179/-85/85 -JQ18 -Sc0.1 -Cwind.cpt -K -O >> mapwind.ps
psxy slp.dat -R-179/179/-85/85 -JQ18 -Sc0.1 -Cpress.cpt -K -O >> mapslp.ps
psxy id_indicator.dat -R-179/179/-85/85 -JQ18 -Sc0.05 -Cid_indicator.cpt -K -O >> mapid_indicator.ps

psscale -D6/10.5/10/0.3h -Cwind.cpt -B2/:[m/s]: -O >>mapwind.ps
psscale -D6/10.5/10/0.3h -Cpress.cpt -B5/:[hpa]: -O >>mapslp.ps
psscale -D6/10.5/10/0.3h -Cid_indicator.cpt -B1 -O >>mapid_indicator.ps


psconvert -P mapwind.ps
psconvert -P mapslp.ps
psconvert -P mapid_indicator.ps
pause