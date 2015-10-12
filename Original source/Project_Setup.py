# Code for Bezier with only 2 points, plus adding noise, and testing plots
# Prints  start and end points, true guidepoints, true Bezier function coefficients as arrays,
#         formatted true and noisy points with corresponding times, and arrays of the true and noisy points (not formatted)
# Plots noisy points and true Bezier function
# x[] is starting and ending x coordinate (longitude)
# y[] is starting and ending y coordinate (latitude)
# (x/y)(pl/mi)[] are guideline points - notice these are set relative to the starting and ending coordinates
import matplotlib.pyplot as plt
from sympy import Symbol
import numpy
import sys

x = [-118.2, -74.0]
y = [34.1, 40.7]
xpl = [(x[0] + 3.0)] 
ypl = [(y[0] - 4.0)]
xmi = [0, (x[1] - 18.5)]    # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
ymi = [0, (y[1] + 5.75)]    # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
a = [ 0 for i in range (4) ]
b = [ 0 for i in range (4) ]

print "\n\nTake-off longitude: " + str(x[0])
print "Take-off latitude:  " + str(y[0])
print "Landing longitude:  " + str(x[1])
print "Landing latitude:   " + str(y[1])
print "\nx_0_plus:  " + str(xpl[0])
print "y_0_plus:  " + str(ypl[0])
print "x_1_minus: " + str(xmi[1])
print "y_1_minus: " + str(ymi[1])


for i in range (0, 1):
    a[0] = x[i]
    b[0] = y[i]
    a[1] = 3*(xpl[i] - x[i])
    b[1] = 3*(ypl[i] - y[i])
    a[2] = 3*(x[i] + xmi[i+1] - 2*xpl[i])
    b[2] = 3*(y[i] + ymi[i+1] - 2*ypl[i])
    a[3] = x[i+1] - x[i] + 3*xpl[i] - 3*xmi[i+1]
    b[3] = y[i+1] - y[i] + 3*ypl[i] - 3*ymi[i+1]

print "\n\nCopyable a array:"
print "*****************"
print str(a)
print "\nCopyable b array:"
print "*****************"
print str(b)

# Here we set an array of equal time increments, time starts at 0.0 and ends at 1.0
n = 20                             # number of pings we want to use
time = [0 for i in range (n)]      # note this array starts at 0 and ends at (n-1)
for i in range (1, n):
    time[i] = time[i-1] + ((1.0)/(n-1))

# Now to input coefficients for our Bezier function and set it up...
t = Symbol('t')
X = a[0] + a[1]*t + a[2]*(t**2) + a[3]*(t**3)
Y = b[0] + b[1]*t + b[2]*(t**2) + b[3]*(t**3)

# From here create arrays of true x and y positions at time t
xpos = [0 for i in range (n)]
ypos = [0 for i in range (n)]
print "\n\nTrue values:"
print "************"
for i in range (0, n):
    xpos[i] = X.subs(t, time[i])
    ypos[i] = Y.subs(t, time[i])
    print "At time[" + str(i) + "] (" + str("%0.2f"%time[i]) + "),\tposition: (" + str("%0.3f"%xpos[i]) + ", " + str("%0.3f"%ypos[i]) + ")"

# Finally create new position arrays with noise - we'll keep the take-off/landing coordinates the same, since those are known
xNpos = [0 for i in range (n)]
yNpos = [0 for i in range (n)]
xNpos[0]   = xpos[0]
xNpos[n-1] = xpos[n-1]
yNpos[0]   = ypos[0]
yNpos[n-1] = ypos[n-1]
print "\n\nValues with noise:"
print "******************"
for i in range (1, n-1):
    xNpos[i] = numpy.random.normal(xpos[i], 0.4)
    yNpos[i] = numpy.random.normal(ypos[i], 0.4)
for i in range (0, n):
    print "At time[" + str(i) + "] (" + str("%0.2f"%time[i]) + "),\tposition: (" + str("%0.3f"%xNpos[i]) + ", " + str("%0.3f"%yNpos[i]) + ")"

# Print easy to copy arrays of the plot points with noise and without
sys.stdout.write("\n\nValues without noise (copyable arrays x[], y[]):\n\n[")
for i in range (0, n-1):
    sys.stdout.write(str(xpos[i]) + ", ")
sys.stdout.write(str(xpos[n-1]) + "]\n\n[")
for i in range (0, n-1):
    sys.stdout.write(str(ypos[i]) + ", ")
sys.stdout.write(str(ypos[n-1]) + "]\n")

sys.stdout.write("\n\nValues with noise (copyable arrays x[], y[]):\n\n[")
for i in range (0, n-1):
    sys.stdout.write(str(xNpos[i]) + ", ")
sys.stdout.write(str(xNpos[n-1]) + "]\n\n[")
for i in range (0, n-1):
    sys.stdout.write(str(yNpos[i]) + ", ")
sys.stdout.write(str(yNpos[n-1]) + "]\n")

# Plot the results of our true flight path and the noisy pings
plt.figure(1, facecolor='white');
plt.clf();
plt.plot(xpos, ypos, '-', linewidth=1.0, markersize=12, color='g', label='Actual Flight Path');
plt.plot(xNpos, yNpos, '.', linewidth=1.0, markersize=12, color='k', label='Noisy Data Points');
plt.xlabel('Longitude');
plt.ylabel('Latitude');
plt.legend(loc='lower right');
plt.title("Testing Conditions");
plt.show();