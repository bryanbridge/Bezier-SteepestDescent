import re
from sympy import Symbol

#   Shared.py: Methods and data used across scripts

# Code for cubic Bezier curve, currently has only one left endpoint and one
# right endpoint (with their accompanying guidepoints) but is written to be
# expandable to many curves - uses the algorithm in Burden and Faires Numerical
# Analysis. * Outputs list of coordinates along the curve. *
def genBezierPlot(x, y, xpl, ypl, xmi, ymi, n):
    a = [None]*4
    b = [None]*4
    time = makeTimeList(n)
    
    # Burden and Faires coefficient algorithm
    for i in range (0, 1):
        a[0] = x[i]
        b[0] = y[i]
        a[1] = 3*(xpl[i] - x[i])
        b[1] = 3*(ypl[i] - y[i])
        a[2] = 3*(x[i] + xmi[i+1] - 2*xpl[i])
        b[2] = 3*(y[i] + ymi[i+1] - 2*ypl[i])
        a[3] = x[i+1] - x[i] + 3*xpl[i] - 3*xmi[i+1]
        b[3] = y[i+1] - y[i] + 3*ypl[i] - 3*ymi[i+1]
    
    # Input coefficients for Bezier function to polynomial handled by SymPy
    t = Symbol('t')
    X = a[0] + a[1]*t + a[2]*(t**2) + a[3]*(t**3)
    Y = b[0] + b[1]*t + b[2]*(t**2) + b[3]*(t**3)
    
    # Create list of coordinates along curve
    xpos = [None]*n
    ypos = [None]*n
    for i in range (0, n):
        xpos[i] = X.subs(t, time[i])
        ypos[i] = Y.subs(t, time[i])
    
    return [xpos, ypos]


# Set an array of equal time increments, time starts at 0.0 and ends at 1.0
def makeTimeList(n):
    time = [0]*n
    for i in range (1, n):
        time[i] = time[i-1] + ((1.0)/(n-1))
    return time


# Method for getting input through the console
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


#    Setup of values for different curves... Note that for xMinus and yMinus,
# because of the way the algorithm is written these have 0 in index [0], as
# they start at i = 1. This isn't as important for the program as it is now, but
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