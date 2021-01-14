###########################
# CSCI 590 Big Data Analytics - Frequent Pattern algorithm Implementation
# Author: Chu-An Tsai
# 02/13/2020
###########################
 1. The "Apriori.zip" contains 4 files: 
	Apriori.py , Dataset1.dat , Dataset2.dat , README.txt
 2. The library imported in the Apriori.py file: 
	numpy, math, itertools, sys, time
 3. This program supports command line argument input. Please follow the syntax to input arguments: 
	python3 filename dataset min-support min-confidence	
 4. Note that Min-support and Min-confidence are input as decimals. For example: 
	python3 Apriori.py Dataset1.dat 0.8 0.7
 5. This program impliments Apriori algorithm, which is a relatively slower approach. Here are the run time tested for operations with different parameters using Ubuntu 18.04 LTS:

     Dataset          Min-support	Min-confidence      Run Time(s)
------------------------------------------------------------------------------------------
 Dataset1.dat	0.8	         0.7                         30 
 Dataset1.dat              0.7	         0.7	  	  854
 Dataset1.dat  	0.69	         0.7		1346 
 Dataset1.dat  	0.67	         0.7		2959
 Dataset1.dat  	0.65	         0.7		6169
 Dataset2.dat	0.2	         0.4	                      13 
 Dataset2.dat	0.19	         0.4		    15 
 Dataset2.dat	0.09	         0.4		  126
 Dataset2.dat              0.05	         0.4		  802