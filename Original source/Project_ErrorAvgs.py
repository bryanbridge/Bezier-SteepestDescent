# Code to find average errors
LANYavg = 0
CTTKavg = 0
RMPSavg = 0

LANYvals = [0.019858756105, 0.572533801182, 0.0593832470548, 0.927702652504, 0.613911447159, 0.0927638280969, 0.57184639794, 0.433150488485, 0.031849631692, 0.10213714128, 0.356760600545, 0.701202606188]

RMPSvals = [0.669230291293, 0.0237809302593, 0.682438387137, 0.0749348289548, 0.0202154598654, 0.390782480148, 0.0198839762212, 0.802029940062, 0.459613890743, 0.808646041422, 0.215459981154, 0.456602631774]

CTTKvals = [0.711988962852, 0.193289423753, 0.300586238176, 0.0871982641749, 0.203698553585, 0.65391515883, 0.06317625219, 0.472845635055, 0.782311940763, 0.170888848645, 0.99068883727, 0.3468457758]

for i in range (0, len(LANYvals)):
    LANYavg += LANYvals[i]
LANYavg = LANYavg/(len(RMPSvals))

for i in range (0, len(RMPSvals)):
    RMPSavg += RMPSvals[i]
RMPSavg = RMPSavg/(len(RMPSvals))

for i in range (0, len(CTTKvals)):
    CTTKavg += CTTKvals[i]
CTTKavg = CTTKavg/(len(CTTKvals))

avg = (LANYavg + CTTKavg + RMPSavg)/3

print "\n\nAverage Absolute Error for Los Angeles to New York Guidepoints:"
print str(LANYavg)

print "\nAverage Absolute Error for Rome to Paris Guidepoints:"
print str(RMPSavg)

print "\nAverage Absolute Error for Cape Town to Tokyo Guidepoints:"
print str(CTTKavg)

print "\nOverall Average Absolute Error for Guidepoints:"
print str(avg)