from sympy import Symbol
import math

# -METHOD-
# stepGradient:
# xNpos, yNpos is the coordinate arrays for our errored data (don't forget the first and last coordinates of each array have no error)
# step is the step size to each new set of guidepoints (x0+, y0+, x1-, y1-) to be tested
# q_current is the current array of guidepoints being tested (x0+, y0+, x1-, y1-, in that order)
# prnt_gr - if this value is 1 the gradient values print
# Output is an array of updated guidepoints and the sum of the derivatives (for stopping the loop): [x0+, y0+, x1-, y1-, number we want to be close to zero]

def stepGradient(xNpos, yNpos, step, q_current, prnt_gr):
    q_gradient = [0 for i in range (4)]         # This array will hold derivatives of error function w.r.t. x0+, y0+, x1-, y1-, respectively
    q_new = [0 for i in range (4)]              # This array will hold the output for guidepoints
    n = len(xNpos)                              # Get number of plot points to be compared
    t = Symbol('t')                             # Now we'll set up the Bezier curve for variable t, notice each coefficient is a function of guidepoints
    a0 = xNpos[0]
    b0 = yNpos[0]
    a1 = 3*(q_current[0] - xNpos[0])
    b1 = 3*(q_current[1] - yNpos[0])
    a2 = 3*(xNpos[0] + q_current[2] - 2*q_current[0])
    b2 = 3*(yNpos[0] + q_current[3] - 2*q_current[1])
    a3 = xNpos[n-1] - xNpos[0] + 3*q_current[0] - 3*q_current[2]
    b3 = yNpos[n-1] - yNpos[0] + 3*q_current[1] - 3*q_current[3]
    X = a0 + a1*t + a2*(t**2) + a3*(t**3)                           # x-coordinate function of current Bezier function
    Y = b0 + b1*t + b2*(t**2) + b3*(t**3)                           # y-coordinate function of current Bezier function
    time = [0 for i in range (n)]                                   # Create array to hold ping times (between 0 and 1) note this array starts at 0 and ends at (n-1)
    for i in range (1, n):
        time[i] = time[i-1] + ((1.0)/(n-1))
    for i in range(0, n):                                           # This loop finds the q_gradient values - the derivatives mentioned above (it is a loop because the values are sums)
        q_gradient[0] += -(2.0/n) * (xNpos[i] - X.subs(t, time[i])) * (3*(time[i]) - 6*((time[i])**2) + 3*((time[i])**3))
        q_gradient[1] += -(2.0/n) * (yNpos[i] - Y.subs(t, time[i])) * (3*(time[i]) - 6*((time[i])**2) + 3*((time[i])**3))
        q_gradient[2] += -(2.0/n) * (xNpos[i] - X.subs(t, time[i])) * (3*((time[i])**2) - 3*((time[i])**3))
        q_gradient[3] += -(2.0/n) * (yNpos[i] - Y.subs(t, time[i])) * (3*((time[i])**2) - 3*((time[i])**3))
    q_new[0] = q_current[0] - (step * q_gradient[0])
    q_new[1] = q_current[1] - (step * q_gradient[1])
    q_new[2] = q_current[2] - (step * q_gradient[2])
    q_new[3] = q_current[3] - (step * q_gradient[3])
    if (prnt_gr == 1):
        print "grad x0+: " + str(q_gradient[0])
        print "grad y0+: " + str(q_gradient[1])
        print "grad x1-: " + str(q_gradient[2])
        print "grad y1-: " + str(q_gradient[3])
    grad_abs_sum = math.fabs(q_gradient[0]) + math.fabs(q_gradient[1]) + math.fabs(q_gradient[2]) + math.fabs(q_gradient[3]) # This nears zero --> we're nearing minimum of error function
    return [q_new[0], q_new[1], q_new[2], q_new[3], grad_abs_sum]



# -MAIN-
# Below q[0:4], the first four slots, are initial guesses for guidepoints (shouldn't matter we'll use zero),
#         q[4], the fifth slot, is more garbage but must be > thresh (this is the value that will be used to check how close we are to the minimum error)
#         thresh is the value that stops the while loop from running: in the stepGradient method, once they've been evaluated, we add up the absolute values of
#         the partial derivatives of the error function - the method outputs this value and if it is less than thresh, the loop ends
q = [0, 0, 0, 0, 10.0]
thresh = 0.001

# * NOTICE THE FOUR SETS OF X AND Y ARRAYS BELOW - ONLY ONE SET SHOULD BE UNCOMMENTED AT A GIVEN TIME *
# The first set is only for testing, no noise has been added
# The other sets contain noisy data created with the original Bezier function,
#         the noise is random with the same size distribution - we will test our method on all three and compare the errors

listX = [12.5000000000000, 12.5032512027992, 12.3930456334743, 12.1789182096516, 11.8704038489576, 11.4770374690188, 11.0083539874617, 10.4738883219128, 9.88317538999854, 9.24575010934539, 8.57114739757982, 7.86890217232833, 7.14854935121738, 6.41962385187345, 5.69166059192302, 4.97419448899256, 4.27676046070856, 3.60889342469747, 2.98012829858580, 2.40000000000000]
listY = [41.9000000000000, 41.6727073917481, 41.6107450065607, 41.6966175827380, 41.9128298585800, 42.2418865723866, 42.6662924624581, 43.1685522670943, 43.7311707245954, 44.3366525732614, 44.9675025513923, 45.6062253972882, 46.2353258492492, 46.8373086455752, 47.3946785245663, 47.8899402245225, 48.3055984837440, 48.6241580405307, 48.8281236331827, 48.9000000000000]

#listX = [12.5000000000000, 13.4502831792, 12.4210281428, 12.0234383473, 12.5546764332, 11.4617787494, 11.6591154847, 10.1291092688, 10.3825282357, 9.23646912719, 8.22005117813, 7.15798637267, 6.45306321884, 6.6532687506, 5.8876800247, 5.18341500189, 3.98913405595, 3.74617146523, 2.82797351406, 2.40000000000000]
#listY = [41.9000000000000, 41.7101401465, 41.0399601612, 41.6581650372, 42.1432651854, 42.3110838241, 42.3653619872, 43.3776884323, 44.1568313356, 44.5298175829, 44.9869242658, 45.4898806886, 46.2752643235, 46.1165516167, 47.1704137554, 48.421236568, 48.2926636052, 48.9752476462, 49.0710745724, 48.9000000000000]

#listX = [12.5000000000000, 12.3368613755, 12.6858792683, 11.9799543139, 12.43311685, 11.0094481476, 11.2822379775, 10.9826210125, 10.1611154857, 8.889423185, 7.74852901866, 7.39402424567, 7.28015292056, 6.26769981072, 6.03725168744, 5.02395116678, 4.96987941826, 3.48375810706, 3.27936881811, 2.40000000000000]
#listY = [41.9000000000000, 41.7964191853, 41.0791838491, 41.6481550528, 41.8016170074, 41.720043027, 43.1993913289, 43.0961243262, 44.0874390807, 44.2710519191, 45.7395978458, 45.9370441574, 46.3266477979, 46.5356741223, 47.246436982, 48.3227984517, 48.8129809621, 49.3849360352, 48.4339917556, 48.9000000000000]

#listX = [12.5000000000000, 12.2162271447, 12.5716025212, 12.7737057823, 11.7868578712, 10.6791165458, 10.4839612301, 10.4903798708, 10.2865772848, 9.10703201252, 8.21322517213, 7.64830551835, 6.82769184093, 6.76679275621, 5.66965659854, 4.76499246166, 4.61281305055, 3.65704173287, 3.64717170837, 2.40000000000000]
#listY = [41.9000000000000, 41.2917379244, 40.9730154842, 42.0656281674, 41.5874442018, 42.0592881608, 42.8040093759, 42.8690639231, 43.6298648919, 43.69514394, 44.5881725579, 45.7577125689, 46.1240327027, 46.5916949403, 47.3761141804, 48.3195391997, 48.3917575607, 49.3036414417, 48.8874025897, 48.9000000000000]


while (stepGradient(listX, listY, 0.5, q[0:4], 0)[4] > thresh):
    q = stepGradient(listX, listY, 0.5, q[0:4], 1)
    print "x0+: " + str(q[0])
    print "y0+: " + str(q[1])
    print "x1-: " + str(q[2])
    print "y1-: " + str(q[3])
print q