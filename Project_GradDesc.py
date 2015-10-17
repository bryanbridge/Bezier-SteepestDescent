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

listX = [-118.200000000000, -117.566088351072, -116.625659717160, -115.399620935997, -113.908878845313, -112.174340282840, -110.216912086310, -108.057501093454, -105.717014142003, -103.216358069689, -100.576439714244, -97.8181659133984, -94.9624435048841, -92.0301793264324, -89.0422802157749, -86.0196530106429, -82.9832045487680, -79.9538416678816, -76.9524712057151, -74.0000000000000]
listY = [34.1000000000000, 33.6313456772124, 33.4637848082811, 33.5601837002479, 33.8834086601545, 34.3963259950430, 35.0618020119551, 35.8427030179326, 36.7018953200175, 37.6022452252515, 38.5066190406765, 39.3778830733343, 40.1789036302668, 40.8725470185158, 41.4216795451232, 41.7891675171308, 41.9378772415804, 41.8306750255139, 41.4304271759732, 40.7000000000000]

#listX = [-118.200000000000, -117.142258884, -117.160259171, -114.893315684, -113.806066532, -112.863935086, -109.932471834, -108.098789192, -105.747928153, -103.127487548, -100.984835519, -97.4896160152, -94.6028710916, -92.0535035888, -89.2239243443, -86.3181185942, -82.6285557715, -80.8264218159, -76.2012005572, -74.0000000000000]
#listY = [34.1000000000000, 33.4965140021, 33.5642093302, 33.8550425118, 34.2209409025, 33.6891437677, 34.6823422372, 36.0656097502, 36.7925181942, 37.1183832159, 38.3269302351, 40.1067050874, 40.9696005429, 40.8472499131, 41.7061077523, 42.4107875664, 42.1777288134, 41.9828250695, 41.2114247865, 40.7000000000000]

#listX = [-118.200000000000, -118.108324557, -117.000023642, -115.206155379, -114.087421499, -112.369065431, -110.722978645, -108.704863573, -105.137429451, -103.347146051, -100.114484454, -97.7228598003, -94.7478172021, -92.078024665, -88.58186261, -86.4001375773, -82.9936763674, -79.8435510446, -76.9062696089, -74.0000000000000]
#listY = [34.1000000000000, 33.5564342364, 33.3171574201, 33.7723524742, 33.7337537763, 34.5137833902, 34.6888123481, 36.0737361122, 36.656322321, 36.8109871817, 38.9700903265, 38.8586081547, 40.7540027706, 40.6466586249, 41.2405023273, 41.3674622994, 41.3061382058, 41.9813863524, 41.5171502075, 40.7000000000000]

#listX = [-118.200000000000, -117.884413234, -117.067070976, -115.920355055, -113.548287018, -112.170960286, -110.150277258, -108.200238709, -105.220475617, -103.578155389, -100.998212757, -97.6192153235, -95.4727554627, -92.2525593757, -89.1941170896, -86.6278075983, -82.7957308667, -79.8682709354, -76.8346712526, -74.0000000000000]
#listY = [34.1000000000000, 34.0802059468, 33.7732765297, 33.4600246366, 33.7288249484, 33.9630619601, 35.5713935011, 35.610298978, 36.5381400211, 37.348711427, 38.0774402111, 38.9635229884, 39.5940083016, 40.4473830202, 41.6026391559, 41.6925652857, 42.1433824068, 41.0228428645, 41.7347667182, 40.7000000000000]


while (stepGradient(listX, listY, 0.5, q[0:4], 0)[4] > thresh):
    q = stepGradient(listX, listY, 0.5, q[0:4], 1)
    print "x0+: " + str(q[0])
    print "y0+: " + str(q[1])
    print "x1-: " + str(q[2])
    print "y1-: " + str(q[3])
print q



#
#with open("output", "rb") as input:
#    reader = csv.reader(input, delimiter='|')
#    blarg = np.array(reader.next()).astype(np.float)