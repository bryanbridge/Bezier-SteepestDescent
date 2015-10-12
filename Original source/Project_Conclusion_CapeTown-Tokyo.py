import matplotlib.pyplot as plt
from sympy import Symbol
import numpy
import math
import sys

# These are the original guidepoints
true_x0pl = 18.6 + 45
true_y0pl = -33.9 - 4.0
true_x1mi = 139.7 + 5.5
true_y1mi = 35.7 - 35.75

# These are arrays of guidepoints estimated using our gradient descent method for 3 different sets of noisy data, the fourth set has no noise
est_x0pl = [64.3119889628517, 63.3963014464146, 64.3823119407632, 63.6083608566631]
est_y0pl = [-38.09328942375256, -38.5539151588299, -37.7291111513552, -37.8961218330307]
est_x1mi = [144.899413761824, 145.263176252190, 144.209311162730, 145.191639143337]
est_y1mi = [0.0371982641748873, 0.422845635054696, 0.296845775800325, -0.0538781669692910]


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
xNpos = [18.6000000000000, 26.5173375789, 34.0230867794, 42.3249722094, 50.9243058513, 59.7039828159, 68.3048775104, 77.5572704782, 85.660825017, 94.1471064566, 102.71416782, 109.451625526, 116.644986744, 122.83283029, 127.882775401, 132.239616515, 136.494444825, 138.976514459, 139.90286033, 139.700000000000]
yNpos = [-33.9000000000000, -33.9202450935, -34.6161283794, -32.8447017055, -31.6611714346, -28.7401065199, -26.4670136823, -23.957899998, -19.5169308683, -15.9010484585, -12.2048438697, -7.35484642885, -2.62389892089, 2.56467246679, 8.0579202611, 13.3602695021, 18.2395708738, 24.8878291464, 29.8410486972, 35.7000000000000]

# *****************************************************************
# Set up curve with estimated guidepoints from first noisy data set
x = [18.6, 139.7]
y = [-33.9, 35.7]
xpl = [64.3119889628517] 
ypl = [-38.0932894237525]
xmi = [0, 144.899413761824]    # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
ymi = [0, 0.0371982641748873]     # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
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
xpos = [18.6000000000000, 25.9913835836128, 33.8828692229188, 42.1662487243038, 50.7333138941537, 59.4758565388541, 68.2856684647908, 77.0545414783496, 85.6742673859163, 94.0366379938766, 102.033445108616, 109.556480536521, 116.497536083977, 122.748403557370, 128.200874763085, 132.746741507508, 136.277795597026, 138.685828838023, 139.862633036886, 139.700000000000]
ypos = [-33.9000000000000, -34.1902026534480, -33.8232832774457, -32.8376877095787, -31.2718617874326, -29.1642513485931, -26.5533022306459, -23.4774602711766, -19.9751713077708, -16.0848811780143, -11.8450357194926, -7.29408076979151, -2.47046216649657, 2.58737425280653, 7.84098265053214, 13.2519171890946, 18.7817320309083, 24.3919813383875, 30.0442192739466, 35.7000000000000]


# Plot noisy pings, estimated flight path, true flight path
plt.figure(1, facecolor='white');
plt.clf();
plt.plot(xpos, ypos, '-', linewidth=1.0, markersize=12, color='g', label='Actual Flight Path');
plt.plot(xEpos, yEpos, '-', linewidth=1.0, markersize=12, color='r', label = 'Estimated Flight Path');
plt.plot(xNpos, yNpos, '.', linewidth=1.0, markersize=12, color='k', label = 'Noisy Data Points');
plt.xlabel('Longitude');
plt.ylabel('Latitude');
plt.legend(loc='lower right');
plt.title("Cape Town to Tokyo");
plt.show();