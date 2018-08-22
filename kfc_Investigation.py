#__email__= "ruben.vancoile@gmail.com"
#__date__= "2018-08-08"


########################
## USE AND BACKGROUND ##
########################
# analysis of kfc dataset Negar Elhami Khorasani
	# 20180720_ConcreteStrength_NSCHSC_f'c_Data_NEK.xlsx


####################
## MODULE IMPORTS ##
####################

# standard module reads
import pandas as pd
import sys
import os

# distant function reads
directory="C:/Users/rvcoile/Google Drive/Research/Codes/Python3.6/REF/rvcpy"
sys.path.append(directory)
from PrintAuxiliary import Print_DataFrame,PrintMaxEnt

directory="C:/Users/rvcoile/Google Drive/Research/Codes/Python3.6/MaxEnt/MaxEnt_MultiP"
sys.path.append(directory)
from MaxEnt2018_function import MaxEnt2018


###########
## LOCAL ##
###########

if __name__ == "__main__":

	################
	## USER INPUT ##
	################

	# path to data
	file="C:/Users/rvcoile/Google Drive/Research/Projects/Materials_Fire/ConcreteStrength_DataSet.xlsx"
	sheet="Data"

	# switches ifo intended functionality
	SW_MaxEnt=True

	##############
	## HANDLING ##
	##############

	# read dataset
	data=pd.read_excel(file,sheet)

	# select sub-set
	T=400 # [°C]
	grouping=data.groupby('Temp')
	Tspecific_data=grouping.get_group(T)

	############
	## OUTPUT ##
	############

	if SW_MaxEnt:

		# arranging kfc values as pd.Series
		name='kfc [-]'
		s_local=Tspecific_data[name];s_local.name=name # pd.Series format
		s_local=s_local*100 # dim change : retention ratio => retention percentage (better for MaxEnt evaluation)

		# printing of MaxEnt input file
		# target folder
		print("\n## MaxEnt results will be saved in local worker directory. ##")
		u=input("Press ENTER to confirm, or provide path to alternative directory: ")
		if u!='': 
			if u[0]=="\"": targetdir=u[1:-1] # strips quotes from path
			else: targetdir=u
			print("\nMaxEnt output will be saved in ", targetdir)
		else: targetdir=os.getcwd() # target directory MaxEnt input *.xlsx -- for current working directory use : os.getcwd()
		# target filename
		targetfilename='inputMaxEnt2018'
		PrintMaxEnt(s_local,targetdir,targetfilename)
		Print_DataFrame([Tspecific_data],targetdir+'/'+'RawData',[str(T)])

		# MaxEnt calculation
		# default values
		SW_Gaussian=False
		xmax_default=300
		xmax_printing=300
		x_deltaprint=1
		nProc=2
		mlist=[3,4,5]
		samples_rAlpha=10**3
		# function evaluation
		MaxEnt2018(targetdir,targetdir+'/'+targetfilename+'.xlsx',SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint)

	#############
	## TESTING ##
	#############

	# print(Tspecific_data)

	# Print_DataFrame([Tspecific_data],'Test',['400'])
