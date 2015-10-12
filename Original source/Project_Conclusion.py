import matplotlib.pyplot as plt
from sympy import Symbol
import numpy
import math
import sys

# These are the original guidepoints
true_x0pl = -115.2
true_y0pl = 30.1
true_x1mi = -92.5
true_y1mi = 46.45

# These are arrays of guidepoints estimated using our gradient descent method for 3 different sets of noisy data, the fourth set has no noise
est_x0pl = [-115.180141243895, -115.813911447159, -115.231849631692, -115.192939292246]
est_y0pl = [29.5274661988176, 30.1927638280969, 30.2021371412803, 30.1050855758498]
est_x1mi = [-92.5593832470548, -91.9281536020599, -92.8567606005445, -92.5070607077544]
est_y1mi = [47.3777026525042, 46.0168495115146, 45.7487973938119, 46.4449144241501]


# Now we compute the actual error for the three sets of estimated guidepoints we found

print "\n\n\n- Absolute Error -"
print "******************"
for i in range (0,4):
    if(i == 3):
        print "\nEst. from clean data set:"
    else:
        print "\nEst. from noisy data set " + str(i+1) + ":"
    print "x_0_plus  " + str(math.fabs(est_x0pl[i] - true_x0pl))
    print "y_0_plus  " + str(math.fabs(est_y0pl[i] - true_y0pl))
    print "x_1_minus " + str(math.fabs(est_x1mi[i] - true_x1mi))
    print "y_1_minus " + str(math.fabs(est_y1mi[i] - true_y1mi))

print "\n\n\n- Relative Error -"
print "******************"
for i in range (0,4):
    if(i == 3):
        print "\nEst. from clean data set:"
    else:
        print "\nEst. from noisy data set " + str(i+1) + ":"
    print "x_0_plus  " + str(math.fabs(est_x0pl[i] - true_x0pl)/(math.fabs(true_x0pl)))
    print "y_0_plus  " + str(math.fabs(est_y0pl[i] - true_y0pl)/(math.fabs(true_y0pl)))
    print "x_1_minus " + str(math.fabs(est_x1mi[i] - true_x1mi)/(math.fabs(true_x1mi)))
    print "y_1_minus " + str(math.fabs(est_y1mi[i] - true_y1mi)/(math.fabs(true_y1mi)))



# First noisy data set (this is the one we'll use for plotting example)
xNpos = [-118.200000000000, -117.142258884, -117.160259171, -114.893315684, -113.806066532, -112.863935086, -109.932471834, -108.098789192, -105.747928153, -103.127487548, -100.984835519, -97.4896160152, -94.6028710916, -92.0535035888, -89.2239243443, -86.3181185942, -82.6285557715, -80.8264218159, -76.2012005572, -74.0000000000000]
yNpos = [34.1000000000000, 33.4965140021, 33.5642093302, 33.8550425118, 34.2209409025, 33.6891437677, 34.6823422372, 36.0656097502, 36.7925181942, 37.1183832159, 38.3269302351, 40.1067050874, 40.9696005429, 40.8472499131, 41.7061077523, 42.4107875664, 42.1777288134, 41.9828250695, 41.2114247865, 40.7000000000000]

# *****************************************************************
# Set up curve with estimated guidepoints from first noisy data set
x = [-118.2, -74.0]
y = [34.1, 40.7]
xpl = [-115.180141243895] 
ypl = [29.5274661988176]
xmi = [0, -92.5593832470548]    # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
ymi = [0, 47.3777026525042]     # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
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
    
# Here we set an array of equal time increments, time starts at 0.0 and ends at 1.0
n = 20                             # number of pings we want to use
time = [0 for i in range (n)]      # note this array starts at 0 and ends at (n-1)
for i in range (1, n):
    time[i] = time[i-1] + ((1.0)/(n-1))

# Now to input coefficients for our estimated Bezier function and set it up...
t = Symbol('t')
X = a[0] + a[1]*t + a[2]*(t**2) + a[3]*(t**3)
Y = b[0] + b[1]*t + b[2]*(t**2) + b[3]*(t**3)

# From here create arrays of estimated x and y positions at time t
xEpos = [0 for i in range (n)]
yEpos = [0 for i in range (n)]
for i in range (0, n):
    xEpos[i] = X.subs(t, time[i])
    yEpos[i] = Y.subs(t, time[i])
# *****************************************************************

# Coordinates from original function
xpos = [-118.200000000000, -117.566088351072, -116.625659717160, -115.399620935997, -113.908878845313, -112.174340282840, -110.216912086310, -108.057501093454, -105.717014142003, -103.216358069689, -100.576439714244, -97.8181659133984, -94.9624435048841, -92.0301793264324, -89.0422802157749, -86.0196530106429, -82.9832045487680, -79.9538416678816, -76.9524712057151, -74.0000000000000]
ypos = [34.1000000000000, 33.6313456772124, 33.4637848082811, 33.5601837002479, 33.8834086601545, 34.3963259950430, 35.0618020119551, 35.8427030179326, 36.7018953200175, 37.6022452252515, 38.5066190406765, 39.3778830733343, 40.1789036302668, 40.8725470185158, 41.4216795451232, 41.7891675171308, 41.9378772415804, 41.8306750255139, 41.4304271759732, 40.7000000000000]


# Plot noisy pings, estimated flight path, true flight path
plt.figure(1, facecolor='white');
plt.clf();
plt.plot(xpos, ypos, '-', linewidth=1.0, markersize=12, color='g', label='Actual Flight Path');
plt.plot(xEpos, yEpos, '-', linewidth=1.0, markersize=12, color='r', label = 'Estimated Flight Path');
plt.plot(xNpos, yNpos, '.', linewidth=1.0, markersize=12, color='k', label = 'Noisy Data Points');
plt.xlabel('Longitude');
plt.ylabel('Latitude');
plt.legend(loc='lower right');
plt.title("Los Angeles to New York");
plt.show();