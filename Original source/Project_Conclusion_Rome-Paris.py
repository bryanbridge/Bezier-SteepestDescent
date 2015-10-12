import matplotlib.pyplot as plt
from sympy import Symbol
import numpy
import math
import sys

# These are the original guidepoints
true_x0pl = 12.5 + 0.4
true_y0pl = 41.9 - 2.0
true_x1mi = 2.4 + 3.5
true_y1mi = 48.9 + 0.0

# These are arrays of guidepoints estimated using our gradient descent method for 3 different sets of noisy data, the fourth set has no noise
est_x0pl = [13.5692302912927, 12.8797845401346, 12.4403861092572, 12.8947283851556]
est_y0pl = [39.8762190697407, 39.5092175198523, 39.0913539585784, 39.9067777905142]
est_x1mi = [5.21756161286349, 5.91988397622119, 6.11545998115440, 5.90527161484442]
est_y1mi = [48.9749348289548, 49.7020299400622, 49.3566026317743, 48.8932222094857]


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
xNpos = [12.5000000000000, 13.4502831792, 12.4210281428, 12.0234383473, 12.5546764332, 11.4617787494, 11.6591154847, 10.1291092688, 10.3825282357, 9.23646912719, 8.22005117813, 7.15798637267, 6.45306321884, 6.6532687506, 5.8876800247, 5.18341500189, 3.98913405595, 3.74617146523, 2.82797351406, 2.40000000000000]
yNpos = [41.9000000000000, 41.7101401465, 41.0399601612, 41.6581650372, 42.1432651854, 42.3110838241, 42.3653619872, 43.3776884323, 44.1568313356, 44.5298175829, 44.9869242658, 45.4898806886, 46.2752643235, 46.1165516167, 47.1704137554, 48.421236568, 48.2926636052, 48.9752476462, 49.0710745724, 48.9000000000000]

# *****************************************************************
# Set up curve with estimated guidepoints from first noisy data set
x = [12.5, 2.4]
y = [41.9, 48.9]
xpl = [13.5692302912927] 
ypl = [39.876219069740]
xmi = [0, 5.21756161286349]    # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
ymi = [0, 48.9749348289548]     # 0 slot is always 0 (starts at position 1 in more general Bezier algorithm)
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
xpos = [12.5000000000000, 12.5032512027992, 12.3930456334743, 12.1789182096516, 11.8704038489576, 11.4770374690188, 11.0083539874617, 10.4738883219128, 9.88317538999854, 9.24575010934539, 8.57114739757982, 7.86890217232833, 7.14854935121738, 6.41962385187345, 5.69166059192302, 4.97419448899256, 4.27676046070856, 3.60889342469747, 2.98012829858580, 2.40000000000000]
ypos = [41.9000000000000, 41.6727073917481, 41.6107450065607, 41.6966175827380, 41.9128298585800, 42.2418865723866, 42.6662924624581, 43.1685522670943, 43.7311707245954, 44.3366525732614, 44.9675025513923, 45.6062253972882, 46.2353258492492, 46.8373086455752, 47.3946785245663, 47.8899402245225, 48.3055984837440, 48.6241580405307, 48.8281236331827, 48.9000000000000]


# Plot noisy pings, estimated flight path, true flight path
plt.figure(1, facecolor='white');
plt.clf();
plt.plot(xpos, ypos, '-', linewidth=1.0, markersize=12, color='g', label='Actual Flight Path');
plt.plot(xEpos, yEpos, '-', linewidth=1.0, markersize=12, color='r', label = 'Estimated Flight Path');
plt.plot(xNpos, yNpos, '.', linewidth=1.0, markersize=12, color='k', label = 'Noisy Data Points');
plt.xlabel('Longitude');
plt.ylabel('Latitude');
plt.legend(loc='lower left');
plt.title("Rome to Paris");
plt.show();