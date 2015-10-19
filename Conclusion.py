import matplotlib.pyplot as plt
import math
import Shared as pre
from Shared import getTextInput, genBezierPlot
import csv
import os

#     Conclusion.py: Loads lists of guidepoints computed with the gradient
# descent method and checks absolute and relative errors againts real
# guidepoints. Plots real curve, a noisy data example, and a curve generated
# from guidepoints found using gradient descent on that noisy example.

# Automatically sets working directory to the folder enclosing this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Get input to make sure data matches what was chosen when Setup.py ran
input1 = getTextInput("\nMake sure you've already run Setup.py, then "\
                        "GradDesc.py.\n\nWhich preset did you use?\n\n"\
                        "Enter a number to choose path data:\n"\
                        "1: Los Angeles to New York\n"\
                        "2: Rome to Paris\n"\
                        "3: Cape Town to Tokyo\n"\
                        "...Leaving blank will default to 1.\n",\
                     "^[1-3]$", "1")

if input1 == "1":
    rt = pre.la_ny
elif input1 == "2":
    rt = pre.rm_pa
else:
    rt = pre.ct_tk


#     Lists for the guidepoints estimated using the gradient descent
# method are loaded below. [0],[1], and [2] are different sets of noisy
# data, [4] had no noise.
est_x0pl=[None]*4; est_y0pl=[None]*4; est_x1mi=[None]*4; est_y1mi=[None]*4;
gls = open("data/computed_guidepoints", "r")
reader = csv.reader(gls, delimiter='|')
for i in range (0, 4):
    temp = reader.next()
    est_x0pl[i] = float(temp[0])
    est_y0pl[i] = float(temp[1])
    est_x1mi[i] = float(temp[2])
    est_y1mi[i] = float(temp[3])
gls.close()


# Compute the actual and relative error for the four sets of estimated
# guidepoints found. The first three estimates were found with the gradient
# descent method from noisy data plot points. The last estimate was found
# with plot points that lay on the Bezier curve exactly. Take note the relative
# error doesn't mean much because we are dealing with coordinates on a map, not
# magnitudes.
print "\n\n\n- Absolute Error -"
print "******************"
for i in range (0,4):
    if(i == 3):
        print "\nEst. from clean data set:"
    else:
        print "\nEst. from noisy data set " + str(i+1) + ":"
    print "x_0_plus  " + str(math.fabs(est_x0pl[i] - rt.xPlus[0]))
    print "y_0_plus  " + str(math.fabs(est_y0pl[i] - rt.yPlus[0]))
    print "x_1_minus " + str(math.fabs(est_x1mi[i] - rt.xMinus[1]))
    print "y_1_minus " + str(math.fabs(est_y1mi[i] - rt.yMinus[1]))

print "\n\n\n- Relative Error -"
print "******************"
for i in range (0,4):
    if(i == 3):
        print "\nEst. from clean data set:"
    else:
        print "\nEst. from noisy data set " + str(i+1) + ":"
    print "x_0_plus  " + \
        str(math.fabs(est_x0pl[i] - rt.xPlus[0])/(math.fabs(rt.xPlus[0])))
    print "y_0_plus  " + \
        str(math.fabs(est_y0pl[i] - rt.yPlus[0])/(math.fabs(rt.yPlus[0])))
    print "x_1_minus " + \
        str(math.fabs(est_x1mi[i] - rt.xMinus[1])/(math.fabs(rt.xMinus[1])))
    print "y_1_minus " + \
        str(math.fabs(est_y1mi[i] - rt.yMinus[1])/(math.fabs(rt.yMinus[1])))


# Grab the first noisy points data set and the true points data set (the fourth
# set) to be used in the plotting example
pings = open("data/pings", "r")
reader = csv.reader(pings, delimiter='|')
xNpos = map(lambda x: float(x), reader.next())
yNpos = map(lambda x: float(x), reader.next())
for i in range (0, 4): reader.next()
xpos = reader.next()
ypos = reader.next()
pings.close()

# Set up curve with guidepoints estimated from first noisy data set
n = 20
xEpos, yEpos = genBezierPlot(rt.x, rt.y, [est_x0pl[0]], [est_y0pl[0]], \
                             [0, est_x1mi[0]], [0, est_y1mi[0]], n)

# Plot noisy pings, estimated flight path, true flight path
plt.figure(1, facecolor='white');
plt.clf();
plt.plot(xpos, ypos, '-', linewidth=1.0, \
         color='g', label='Actual Flight Path')
plt.plot(xEpos, yEpos, '-', linewidth=1.0, \
         color='r', label = 'Estimated Flight Path')
plt.plot(xNpos, yNpos, '.', linewidth=1.0, \
         color='k', label = 'Noisy Data Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(loc='lower right')
if input1 == "1":
    plt.title("Los Angeles to New York")
elif input1 == "2":
    plt.title("Rome to Paris")
else:
    plt.title("Cape Town to Tokyo")
plt.show()