import sys
import pandas as pd
import powerlaw

if len(sys.argv) > 1:
        filename = sys.argv[1]
	degDist = pd.read_csv(filename)
	PLR = powerlaw.Fit(degDist['count'])
	alpha = PLR.power_law.alpha
	print(alpha)
	if alpha > 2 and alpha < 3:
		print(filename+" is Scale Free")
	else:
		print(filename + " is not Scale Free")

else :
	print("Send filename as argument while executing")