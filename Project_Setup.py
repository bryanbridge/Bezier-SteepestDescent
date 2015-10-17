#    Code for cubic Bezier curve, currently has only one left endpoint and one
# right endpoint (with their accompanying guidepoints) but is written to be
# expandable to many curves - uses the algorithm in Burden and Faires Numerical
# Analysis. Generates array of points along the curve, plus another array
# of the same data with Gaussian noise added. Plots the curve and noisy data.
#
#    Make sure working directory is set to the folder enclosing this file
#
#    The data is meant to be imagined as longitude and latitude points along a
# flight path:
#              x[] is starting and ending x coordinate (longitude)
#              y[] is starting and ending y coordinate (latitude)
#              (x/y)(pl/mi)[] are guideline points - notice these are set
#                  relative to the starting and ending coordinates

import matplotlib.pyplot as plt
from sympy import Symbol
import numpy as np
import sys
import csv
import re

# =============================================================
# Temporary garbage.

def getTextInput(prompt, regex, default = False):
    while True:
        text = raw_input(prompt)
        if text == "" and default is not False:
            out = default
            print "Used default: " + out
            break
        if re.match(regex, text):
            out = text
            break
    return out

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

# ==============================================================

#    Setup of values for different curves... Note that for xMinus and yMinus,
# because of the way the algorithm is written these have 0 in index [0], as
# they start at i = 1. This isn't as important for the script as it is now, but
# if we want to iterate over many curves the algorithm accounted for that, and
# conforming to its style makes things easier to understand
class preset:
    x = None
    y = None
    xPlus = None
    yPlus = None
    xMinus = None
    yMinus = None

# "Los Angeles to New York"
la_ny = preset()
la_ny.x = [-118.2, -74.0]
la_ny.y = [34.1, 40.7]
la_ny.xPlus = [(la_ny.x[0] + 3.0)] 
la_ny.yPlus = [(la_ny.y[0] - 4.0)]
la_ny.xMinus = [0, (la_ny.x[1] - 18.5)]
la_ny.yMinus = [0, (la_ny.y[1] + 5.75)]

# "Rome to Paris"
rm_pa = preset()
rm_pa.x = [12.5, 2.4]
rm_pa.y = [41.9, 48.9]
rm_pa.xPlus = [(rm_pa.x[0] + 0.4)] 
rm_pa.yPlus = [(rm_pa.y[0] - 2.0)]
rm_pa.xMinus = [0, (rm_pa.x[1] + 3.5)]
rm_pa.yMinus = [0, (rm_pa.y[1] + 0.0)] 

# "Cape Town to Tokyo
ct_tk = preset()
ct_tk.x = [18.6, 139.7]
ct_tk.y = [-33.9, 35.7]
ct_tk.xPlus = [(ct_tk.x[0] + 45.0)] 
ct_tk.yPlus = [(ct_tk.y[0] - 4.0)]
ct_tk.xMinus = [0, (ct_tk.x[1] + 5.5)]
ct_tk.yMinus = [0, (ct_tk.y[1] - 35.75)]


if input1 == "1":
    route = la_ny
elif input1 == "2":
    route = rm_pa
else:
    route = ct_tk

x = route.x
y = route.y
xpl = route.xPlus
ypl = route.yPlus
xmi = route.xMinus
ymi = route.yMinus

a = [ 0 for i in range (4) ]
b = [ 0 for i in range (4) ]

for i in range (0, 1):
    a[0] = x[i]
    b[0] = y[i]
    a[1] = 3*(xpl[i] - x[i])
    b[1] = 3*(ypl[i] - y[i])
    a[2] = 3*(x[i] + xmi[i+1] - 2*xpl[i])
    b[2] = 3*(y[i] + ymi[i+1] - 2*ypl[i])
    a[3] = x[i+1] - x[i] + 3*xpl[i] - 3*xmi[i+1]
    b[3] = y[i+1] - y[i] + 3*ypl[i] - 3*ymi[i+1]

# Set an array of time increments, time starts at 0.0 and ends at 1.0, n is
# the number of pings we want to use
n = 20
time = [0 for i in range (n)]
for i in range (1, n):
    time[i] = time[i-1] + ((1.0)/(n-1))

# Input coefficients for our Bezier function and set it up...
t = Symbol('t')
X = a[0] + a[1]*t + a[2]*(t**2) + a[3]*(t**3)
Y = b[0] + b[1]*t + b[2]*(t**2) + b[3]*(t**3)

# Create arrays of true x and y positions at time t
xpos = [0 for i in range (n)]
ypos = [0 for i in range (n)]
for i in range (0, n):
    xpos[i] = X.subs(t, time[i])
    ypos[i] = Y.subs(t, time[i])
    
# Save those arrays to a file to be used by another script
writer = csv.writer(open("pings", "w"), delimiter='|')
writer.writerow(xpos)
writer.writerow(ypos)

#    Finally, generate new position arrays with noise - we'll keep the
# take-off/landing coordinates the same, since those are known. These are
# saved to be used later as well. Only the last arrays generated are kept, in
# the lists xNpos and yNpos
for i in range (0,3):
    xNpos = [0 for i in range (n)]
    yNpos = [0 for i in range (n)]
    xNpos[0]   = xpos[0]
    xNpos[n-1] = xpos[n-1]
    yNpos[0]   = ypos[0]
    yNpos[n-1] = ypos[n-1]
    for i in range (1, n-1):
        xNpos[i] = np.random.normal(xpos[i], 0.4)
        yNpos[i] = np.random.normal(ypos[i], 0.4)
    writer.writerow(xNpos)
    writer.writerow(yNpos)

#    If requested, plot curve of the true flight path and show noisy pings.
# This will only show the last set of noisy pings generated, but it gives
# the general idea.
if input2 == "y":
    plt.figure(1, facecolor='white')
    plt.clf()
    plt.plot(xpos, ypos, '-', linewidth=1.0, color='g', label='Actual Flight Path')
    plt.plot(xNpos, yNpos, '.', linewidth=1.0, color='k', label='Noisy Data Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(loc='lower right')
    plt.title("Testing Conditions")
    plt.show()



# PRINT SOME STUFF

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
       % (x[0], y[0], x[1], y[1], xpl[0], ypl[0], xmi[1], ymi[1])

print "\n\nCoefficients for Bezier polynomial..."
print "\"A\" Coefficients:\n" + str(a)
print "\"B\" Coefficients:\n" + str(b)