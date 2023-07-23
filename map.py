from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math


# latitude, longitude and station names are as headers rows(rows starting with "#", in plot_file.txt. 
# read all the lines and make lists for latitude and longitude

##inputfile =  open('data-por-IN/plot_file.txt', 'r')   
##for i, line in enumerate(inputfile):    
##    if line.startswith('#'):
##        lattd.append(int(line[56:62])/10000)
##        lngtd.append(int(line[65:71])/10000)

##fake coordinates and labels
lattd, lngtd, labels = zip(*[
    (20.6, 79.0, 'point 1'),
    (21.3, 77.5, 'point 2'),
    (13.0, 77.6, 'point 3'),
])

##a list for keeping track of all annotations
annotations = [None for label in labels]

##defining size of markers:
markersize = 5
markersize_inches = markersize/72.

##setting up figure
fig, ax = plt.subplots()
m = Basemap(
    width=4000000,height=4000000,projection='lcc',
    resolution='c',lat_1=45.,lat_2=55,lat_0=20,lon_0=80.,
    ax = ax,
)
m.drawcountries()
m.drawcoastlines(linewidth=0.50)
m.bluemarble()

##data coordinates
xdata, ydata = zip(*[m(lon,lat) for lon,lat in zip(lngtd,lattd)])
ax.plot(xdata,ydata,'bo', mec='k', ms = markersize)

##figure coordinates in inches
trans = ax.transData+fig.dpi_scale_trans.inverted()

##function for checking mouse coordinates and annotating
def on_move(event):
    if event.inaxes:
        x0, y0 = trans.transform((event.xdata, event.ydata))
        xfig, yfig = zip(*[trans.transform((x,y)) for x,y in zip(xdata,ydata)])
        dists = [math.sqrt((x-x0)**2+(y-y0)**2) for x,y in zip(xfig, yfig)]

        for n,(x,y,dist,label) in enumerate(zip(xdata,ydata,dists, labels)):
            if dist < markersize_inches and annotations[n] is None:
                annotations[n]=ax.annotate(
                    label,
                    [x,y], xycoords='data',
                    xytext = (10,10), textcoords='offset points',
                    ha='left', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'),
                    zorder=10,
                )
                fig.canvas.draw()

            elif dist > markersize_inches and annotations[n] is not None:
                annotations[n].remove()
                annotations[n] = None
                fig.canvas.draw()

##connecting the event handler
cid = fig.canvas.mpl_connect('motion_notify_event', on_move)


plt.show()