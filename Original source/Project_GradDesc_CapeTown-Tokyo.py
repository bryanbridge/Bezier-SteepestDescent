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

listX = [18.6000000000000, 25.9913835836128, 33.8828692229188, 42.1662487243038, 50.7333138941537, 59.4758565388541, 68.2856684647908, 77.0545414783496, 85.6742673859163, 94.0366379938766, 102.033445108616, 109.556480536521, 116.497536083977, 122.748403557370, 128.200874763085, 132.746741507508, 136.277795597026, 138.685828838023, 139.862633036886, 139.700000000000]
listY = [-33.9000000000000, -34.1902026534480, -33.8232832774457, -32.8376877095787, -31.2718617874326, -29.1642513485931, -26.5533022306459, -23.4774602711766, -19.9751713077708, -16.0848811780143, -11.8450357194926, -7.29408076979151, -2.47046216649657, 2.58737425280653, 7.84098265053214, 13.2519171890946, 18.7817320309083, 24.3919813383875, 30.0442192739466, 35.7000000000000]

#listX = [18.6000000000000, 26.5173375789, 34.0230867794, 42.3249722094, 50.9243058513, 59.7039828159, 68.3048775104, 77.5572704782, 85.660825017, 94.1471064566, 102.71416782, 109.451625526, 116.644986744, 122.83283029, 127.882775401, 132.239616515, 136.494444825, 138.976514459, 139.90286033, 139.700000000000]
#listY = [-33.9000000000000, -33.9202450935, -34.6161283794, -32.8447017055, -31.6611714346, -28.7401065199, -26.4670136823, -23.957899998, -19.5169308683, -15.9010484585, -12.2048438697, -7.35484642885, -2.62389892089, 2.56467246679, 8.0579202611, 13.3602695021, 18.2395708738, 24.8878291464, 29.8410486972, 35.7000000000000]

#listX = [18.6000000000000, 25.4596680175, 33.4944248476, 41.5704510268, 51.1396976527, 58.8572966883, 67.9150322768, 77.3083004024, 86.3755994664, 94.1989244547, 102.034147199, 109.990687243, 115.6468263, 123.26773396, 127.899878742, 132.219533999, 136.194298342, 138.459370526, 140.44372484, 139.700000000000]
#listY = [-33.9000000000000, -33.9743369481, -33.7125499695, -33.1245944003, -31.2292156562, -29.4263338146, -26.7197800206, -23.9613476224, -20.0578706256, -16.1828059005, -11.880250753, -7.27554451125, -2.08701762279, 1.90736054318, 7.80464916359, 13.3559392734, 19.2834316286, 24.7254303538, 30.7545707142, 35.7000000000000]

#listX = [18.6000000000000, 26.6199652588, 34.778490824, 41.9989900112, 51.6917291688, 59.3315575796, 67.7665755293, 76.7408930218, 85.8454375711, 94.1541236583, 101.748988175, 109.461050398, 116.714643353, 122.323122888, 128.033664092, 132.284153148, 135.967515479, 138.301498051, 140.137641261, 139.700000000000]
#listY = [-33.9000000000000, -33.8242828002, -33.5546642277, -32.4622395071, -31.3704612682, -29.1000011415, -26.2886429638, -22.8259026779, -19.834797289, -16.5488618274, -11.8701335623, -7.12089433006, -2.01363613645, 2.49254485223, 7.36346359958, 13.867014824, 19.3429767298, 24.6690604201, 30.903435593, 35.7000000000000]


while (stepGradient(listX, listY, 0.5, q[0:4], 0)[4] > thresh):
    q = stepGradient(listX, listY, 0.5, q[0:4], 1)
    print "x0+: " + str(q[0])
    print "y0+: " + str(q[1])
    print "x1-: " + str(q[2])
    print "y1-: " + str(q[3])
print q