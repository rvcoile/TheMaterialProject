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
import shutil

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

	# list of temperatures to evaluate
	Tlist=[100,200,300,400,500,600,700,800] # [°C]

	############
	## OUTPUT ##
	############

	## Handling ##
	##############
	## read dataset
	data=pd.read_excel(file,sheet)

	## select sub-set
	grouping=data.groupby('Temp')


	## MaxEnt run for temperature field ##
	######################################

	for T in Tlist:

		Tspecific_data=grouping.get_group(T)

		## arranging kfc values as pd.Series
		name='kfc [-]'
		s_local=Tspecific_data[name];s_local.name=name # pd.Series format
		s_local=s_local*100 # dim change : retention ratio => retention percentage (better for MaxEnt evaluation)

		## printing of MaxEnt input file
		# target folder
		print("\n## MaxEnt results will be saved in folder created in local worker directory. ##")
		u=input("Press ENTER to confirm, or provide path to alternative directory: ")
		if u!='': 
			if u[0]=="\"": targetdir=u[1:-1] # strips quotes from path
			else: targetdir=u
		else: targetdir=os.getcwd() # target directory MaxEnt input *.xlsx -- for current working directory use : os.getcwd()
		# creation of subdir
		subdir=str(T); dirpath=targetdir+'\\'+subdir
		if os.path.exists(dirpath) and os.path.isdir(dirpath): # remove path and all its contents if it exists
			 shutil.rmtree(dirpath)
		os.mkdir(dirpath) # creates dir
		print("\nMaxEnt output will be saved in ", dirpath)


		# target filename
		targetfilename='inputMaxEnt2018'
		PrintMaxEnt(s_local,dirpath,targetfilename)
		Print_DataFrame([Tspecific_data],dirpath+'/'+'RawData',[str(T)])

		# MaxEnt calculation
		# default values
		SW_Gaussian=False
		xmax_default=300
		xmax_printing=300
		x_deltaprint=1
		nProc=2
		mlist=[4]
		samples_rAlpha=10**3
		# function evaluation
		MaxEnt2018(dirpath,dirpath+'/'+targetfilename+'.xlsx',SW_Gaussian,nProc,mlist,samples_rAlpha,xmax_default,xmax_printing,x_deltaprint)

	#############
	## TESTING ##
	#############

	# print(Tspecific_data)

	# Print_DataFrame([Tspecific_data],'Test',['400'])
