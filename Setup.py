import matplotlib.pyplot as plt
import numpy as np
import csv
import Shared as pre
from Shared import getTextInput, genBezierPlot, makeTimeList
import os

#     Setup.py: Gets list of points along the true Bezier curve that was
# requested, plus another list of the same data with Gaussian noise added.
# Plots the curve and noisy data if requested.

# Automatically sets working directory to the folder enclosing this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Get input deciding which preset flight path to use and whether or not to
# show plot of true flight path and a set of noisy data points
input1 = getTextInput("\nThis file will save sample data to file \"pings\"\n\n"\
                        "Enter a number to choose path data:\n"\
                        "1: Los Angeles to New York\n"\
                        "2: Rome to Paris\n"\
                        "3: Cape Town to Tokyo\n"\
                        "...Leaving blank will default to 1.\n",\
                     "^[1-3]$", "1")

input2 = getTextInput("Show sample plot? [y/n]\n"\
                        "...Leaving blank will default to n.\n",\
                     "^[yn]$", "n")

if input1 == "1":
    rt = pre.la_ny
elif input1 == "2":
    rt = pre.rm_pa
else:
    rt = pre.ct_tk


# Generate list of coordinates on Bezier curve polynomial, n is number of
# coordinates
n = 20
xpos, ypos = \
        genBezierPlot(rt.x, rt.y, rt.xPlus, rt.yPlus, rt.xMinus, rt.yMinus, n)

# Generate new coordinate lists with noise - keep the
# take-off/landing coordinates the same, since those are known. These are
# saved to be used later in data/pings. The first noisy coordinate list pair
# generated is stored for use in the plot, it will be plotted again in another
# script for comparison
xNpos = [None]*n
yNpos = [None]*n
pings = open("data/pings", "wb")
writer = csv.writer(pings, delimiter='|')
for i in range (0,3):
    xNpos[0]   = xpos[0]
    xNpos[n-1] = xpos[n-1]
    yNpos[0]   = ypos[0]
    yNpos[n-1] = ypos[n-1]
    for j in range (1, n-1):
        xNpos[j] = np.random.normal(xpos[j], 0.4)
        yNpos[j] = np.random.normal(ypos[j], 0.4)
    if i == 0:
        xNpos1 = list(xNpos)
        yNpos1 = list(yNpos)
    writer.writerow(xNpos)
    writer.writerow(yNpos)
    
# Save the true coordinate lists to the file as well
writer.writerow(xpos)
writer.writerow(ypos)
pings.close()


#    If requested, plot curve of the true flight path and show noisy pings.
# This will only show the first set of noisy pings generated, but it gives
# the general idea.
if input2 == "y":
    plt.figure(1, facecolor='white')
    plt.clf()
    plt.plot(xpos, ypos, '-', linewidth=1.0, \
             color='g', label='Actual Flight Path')
    plt.plot(xNpos1, yNpos1, '.', linewidth=1.0, \
             color='k', label='Noisy Data Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(loc='lower right')
    plt.title("Testing Conditions")
    plt.show()


# PRINT SOME STUFF

time = makeTimeList(n)

print "\n\nTrue values:"
print "************"
for i in range(0, n):
    print "At time[%s] (%0.2f)\tposition: (%0.3f, %0.3f)"\
           %(i, time[i], xpos[i], ypos[i])

print "\n\nValues with noise:"
print "******************"
for i in range (0, n):
    print "At time[%s] (%0.2f)\tposition: (%0.3f, %0.3f)"\
           %(i, time[i], xNpos[i], yNpos[i])

print "\n\nCoordinates:\nTake-off longitude: %s\nTake-off latitude:  %s\n"\
        "Landing longitude:  %s\nLanding latitude:   %s\n\n"\
        "Guidepoint coordinates:\nx_0_plus:  %s\ny_0_plus:  %s\n"\
        "x_1_minus: %s\ny_1_minus: %s"\
       % (rt.x[0], rt.y[0], rt.x[1], rt.y[1], rt.xPlus[0],\
          rt.yPlus[0], rt.xMinus[1], rt.yMinus[1])