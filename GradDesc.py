from sympy import Symbol
import math
import csv
from Shared import makeTimeList
import os

#    GradDesc.py: Loads plot coordinates and does gradient (steepest) descent
# on the Mean Squared Error (specific to a 2-point/2-guidepoint Bezier curve)
# equation.Contains a method for a single step of the gradient descent, and
# loops it until the combined gradient for the guidepoint variables of the 
# function made from MSE and Bezier is close enough to zero. Dumps estimated
# guidepoints to data/computed_guidepoints.

# Automatically sets working directory to the folder enclosing this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# stepGradient:
#
# * xNpos, yNpos are the coordinate arrays for our errored data (don't forget
#     the first and last coordinates of each array have no error)
# * step is the step size to each new set of guidepoints that will be tested
#     (x0+, y0+, x1-, y1-)
# * q_current is the current set of guidepoints being tested
#    (x0+, y0+, x1-, y1-, in that order)
# * prnt_gr - if this value is 1 the gradient values print
# 
#     The method returns an array of updated guidepoints and the sum of the
# derivatives (for stopping the loop):
#    [x0+, y0+, x1-, y1-, number we want to be approach zero]

def stepGradient(xNpos, yNpos, step, q_current, prnt_gr):
    # q_gradient will hold derivatives of error function w.r.t.
    # x0+, y0+, x1-, y1-, respectively. q_new will hold the output for
    # guidepoints
    q_gradient = [0]*4
    q_new = [0]*4
    n = len(xNpos)
    
    # Now to set up the Bezier curve for variable t, notice each coefficient
    # is a function of guidepoints
    t = Symbol('t')
    a0 = xNpos[0]
    b0 = yNpos[0]
    a1 = 3*(q_current[0] - xNpos[0])
    b1 = 3*(q_current[1] - yNpos[0])
    a2 = 3*(xNpos[0] + q_current[2] - 2*q_current[0])
    b2 = 3*(yNpos[0] + q_current[3] - 2*q_current[1])
    a3 = xNpos[n-1] - xNpos[0] + 3*q_current[0] - 3*q_current[2]
    b3 = yNpos[n-1] - yNpos[0] + 3*q_current[1] - 3*q_current[3]
    
    # x-coordinate function of current Bezier function
    X = a0 + a1*t + a2*(t**2) + a3*(t**3)
    
    # y-coordinate function of current Bezier function
    Y = b0 + b1*t + b2*(t**2) + b3*(t**3)
    
    # Create array to hold ping times (between 0 and 1) note this array starts
    # at 0 and ends at (n-1)
    time = makeTimeList(n)
        
    # This loop finds the q_gradient values - the derivatives mentioned above
    # (it is a loop because the values are sums)
    for i in range(0, n):
        q_gradient[0] += -(2.0/n) * (xNpos[i] - X.subs(t, time[i])) * \
                            (3*(time[i]) - 6*((time[i])**2) + 3*((time[i])**3))
        q_gradient[1] += -(2.0/n) * (yNpos[i] - Y.subs(t, time[i])) * \
                            (3*(time[i]) - 6*((time[i])**2) + 3*((time[i])**3))
        q_gradient[2] += -(2.0/n) * (xNpos[i] - X.subs(t, time[i])) * \
                            (3*((time[i])**2) - 3*((time[i])**3))
        q_gradient[3] += -(2.0/n) * (yNpos[i] - Y.subs(t, time[i])) * \
                            (3*((time[i])**2) - 3*((time[i])**3))
    
    q_new[0] = q_current[0] - (step * q_gradient[0])
    q_new[1] = q_current[1] - (step * q_gradient[1])
    q_new[2] = q_current[2] - (step * q_gradient[2])
    q_new[3] = q_current[3] - (step * q_gradient[3])
    
    # Print changing gradient values if requested
    if (prnt_gr == 1):
        print "grad x0+: " + str(q_gradient[0])
        print "grad y0+: " + str(q_gradient[1])
        print "grad x1-: " + str(q_gradient[2])
        print "grad y1-: " + str(q_gradient[3])
    
    # As grad_abs_sum nears zero, we approach the minimum of the error function
    grad_abs_sum = math.fabs(q_gradient[0]) + math.fabs(q_gradient[1]) + \
                    math.fabs(q_gradient[2]) + math.fabs(q_gradient[3])
    
    return [q_new[0], q_new[1], q_new[2], q_new[3], grad_abs_sum]


#     Below q[0:4], the first four slots, are initial guesses for guidepoints
# (shouldn't matter we'll use zero). q[4], the fifth slot, also doesn't matter
# yet, but must be > thresh (this slot is the value that will be used to check
# how close we are to the minimum error). thresh is the value that stops the
# while loop from running: in the stepGradient method, once they've been
# evaluated, we add up the absolute values of the partial derivatives of the
# error function - the method outputs this value and if it is less than thresh,
# the loop ends
q = [0, 0, 0, 0, 10.0]
thresh = 0.001

pings = open("data/pings", "r")
gls = open("data/computed_guidepoints", "wb")
reader = csv.reader(pings, delimiter='|')
writer = csv.writer(gls, delimiter='|')

for i in range (0, 4):
    listX = map(lambda x: float(x), reader.next())
    listY = map(lambda x: float(x), reader.next())
    while (stepGradient(listX, listY, 0.5, q[0:4], 0)[4] > thresh):
        q = stepGradient(listX, listY, 0.5, q[0:4], 0)
        # ...Uncomment the print statements for some feedback while the
        # script is running
        #print "x0+: " + str(q[0])
        #print "y0+: " + str(q[1])
        #print "x1-: " + str(q[2])
        #print "y1-: " + str(q[3])
    print q
    writer.writerow(q[0:4])

pings.close()
gls.close()