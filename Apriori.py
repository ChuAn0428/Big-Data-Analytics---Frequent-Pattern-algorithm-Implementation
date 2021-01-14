# -*- coding: utf-8 -*-
###########################
# CSCI 590 Big Data Analytics 
# Assignment #1 - Part 1
# Author: Chu-An Tsai
# 02/13/2020
###########################

import numpy as np
import math
from itertools import combinations
import sys
from time import process_time

def load_file(filename):
    
    f = open(filename,'r')
    all_lines = f.readlines()
    data = []
    for line in all_lines:
        remove_last_Space = line.rstrip()
        list_arr = remove_last_Space.split(' ')
        newline = [];
        for i in range(len(list_arr)):
            newline.append(int(list_arr[i]))
        
        data.append(set(newline))  
    #print(data[1])
    return data

def gen_C1_L1_tables(dataset, min_support, f_itemsets):
    
    C1_candidates = []
    for each_transaction in dataset:
        for each_item in each_transaction:
        # if the item is not in the candidate set, then add it in
            if C1_candidates.count(each_item) == 0:
                C1_candidates.append(each_item)
    C1_candidates.sort()
        
    C1_table = np.zeros((len(C1_candidates), 2))
    
    for i in range(len(C1_candidates)):
        C1_table[i][0] = C1_candidates[i]    
    
    C1_table_count = [0]*len(C1_candidates)    
    for each_transaction in dataset:
        for each_item in C1_candidates:
            if each_item in each_transaction:
                index = C1_candidates.index(each_item)
                C1_table_count[index] = C1_table_count[index] + 1
    
    L1_table = []
    L1_table_count =[]
    for i in range(len(C1_candidates)):
        if C1_table_count[i] >= min_support:
            L1_table.append(C1_candidates[i])
            f_itemsets[C1_candidates[i]] = C1_table_count[i]
            L1_table_count.append(C1_table_count[i])
            
    return C1_candidates, C1_table, L1_table, L1_table_count, C1_table_count, f_itemsets        

def gen_can_list(C1_candidates, C1_table, Lx_table, num_round): 
        
    Cx_candidates_precount = (C1_table.copy())

    for i in range(len(Lx_table)):
        for j in range(len(Lx_table[0])):
            if Lx_table[i][j] in C1_candidates:
                index = C1_candidates.index(Lx_table[i][j])
                Cx_candidates_precount[index,1] = Cx_candidates_precount[index,1] +1
            
    Cx_candidate_list = []
    for i in range(len(Cx_candidates_precount)):
        if Cx_candidates_precount[i,1] > 0:
            Cx_candidate_list.append(int(Cx_candidates_precount[i][0]))

    return Cx_candidate_list

def gen_Cx_Lx_tables(dataset, min_support, Cx_candidate_list, L_table, num_round, f_itemsets):
 
    Cx_temp = [item for item in combinations(Cx_candidate_list, num_round)]
    Cx_candidates = []
    if num_round > 2:
        for sample in Cx_temp:
            for j in range(len(L_table)):
                if set(sample).issuperset(set(L_table[j])):
                    if not sample in Cx_candidates:
                        #print(sample,'is not in candidates set')
                        Cx_candidates.append(sample)
    else:
        Cx_candidates = [item for item in combinations(Cx_candidate_list, num_round)]
    
    #print('C',num_round,':\n',Cx_candidates)       
    
    Cx_table_count = [0]*len(Cx_candidates)
    for each_transaction in dataset:
        for each_item in Cx_candidates:
            if set(each_item).issubset(set(each_transaction)):
                index = Cx_candidates.index(each_item)
                Cx_table_count[index] = Cx_table_count[index] + 1
        
    for i in range(len(Cx_table_count)):
        Cx_table_count[i] = int(Cx_table_count[i])   
        
    #print('C',num_round,':\n',Cx_table_count)       
        
    Lx_table = []
    Lx_table_count = []
    for i in range(len(Cx_candidates)):
        if Cx_table_count[i] >= min_support:
            Lx_table.append(Cx_candidates[i])
            f_itemsets[Cx_candidates[i]] = Cx_table_count[i]
            Lx_table_count.append(Cx_table_count[i])
    #print('L',num_round,':\n',Lx_table)       
    
    return Cx_candidates, Lx_table, Lx_table_count, Cx_table_count, f_itemsets

def max_closed_f_set(f_itemsets, Ls_table, Ls_table_count):
    
    max_f_itemsets = []
    clo_f_itemsets = []
    k = len(Ls_table)
    for m in range(k-1,-1,-1):
        if m == k-1:
            for item in reversed(Ls_table[m]):
                    max_f_itemsets.append(item)
                    clo_f_itemsets.append(item)
        else:          
            for item1 in reversed(Ls_table[m]):
                counter1 = 0
                counter2 = 0
                for item2 in reversed(Ls_table[m+1]):
                    if len(str(item1)) <= 2 and not ',' in str(item1):
                        temp_item1 = {item1}
                        if not temp_item1.issubset(set(list(item2))):
                            counter1 = counter1 + 1
                        else:
                            index1 = Ls_table[m].index(item1)
                            index2 = Ls_table[m+1].index(item2)
                            if Ls_table_count[m][index1] <= Ls_table_count[m+1][index2]:
                                counter2 = counter2 + 1    
                    else:
                        if not set(list(item1)).issubset(set(list(item2))):
                            counter1 = counter1 + 1
                        else:
                            index1 = Ls_table[m].index(item1)
                            index2 = Ls_table[m+1].index(item2)
                            if Ls_table_count[m][index1] <= Ls_table_count[m+1][index2]:
                                counter2 = counter2 + 1 
                if counter1 == len(Ls_table[m+1]):
                    max_f_itemsets.append(item1)
                if counter2 == 0:
                    clo_f_itemsets.append(item1)

    return max_f_itemsets, clo_f_itemsets

######### Main ###########################
'''    
dataset = load_file('Dataset2.dat')
min_support = math.ceil((0.19)*len(dataset))
min_confidence = 0.4
#print('Dataset = test.dat')
print('Min-support =>',min_support)
print('Min-confidence =', min_confidence)
time_start = process_time()
'''
script = sys.argv[0]
filename = sys.argv[1]
min_supp = float(sys.argv[2])
min_conf = float(sys.argv[3])

time_start = process_time()

dataset = load_file(filename)
min_support = math.ceil((min_supp)*len(dataset))
min_confidence = min_conf
print('Dataset =', filename)
print('Min-support =', min_supp,'==>',min_support)
print('Min-confidence =', min_confidence)
print('\nWorking on it... ')

f_itemsets = dict()

C1_candidates, C1_table, L1_table, L1_table_count, C1_support, f_itemsets = gen_C1_L1_tables(dataset, min_support, f_itemsets)
C2_candidates, L2_table, L2_table_count, C2_support, f_itemsets = gen_Cx_Lx_tables(dataset, min_support, L1_table, L1_table, 2, f_itemsets) 

Cs_table = [C1_candidates, C2_candidates]
Ls_table = [L1_table, L2_table]
Ls_table_count =[L1_table_count, L2_table_count]
# Continue to find Cx and Lx until there is none
for i in range(3,len(C1_candidates)+1):
    if len(Ls_table[-1]) > 0:
        Cx_candidate_list = gen_can_list(C1_candidates, C1_table, Ls_table[i-2], i)    
        Cx_candidates, Lx_table, Lx_table_count, Cx_support, f_itemsets = gen_Cx_Lx_tables(dataset, min_support, Cx_candidate_list, Ls_table[i-2], i, f_itemsets) 
        Cs_table.append(Cx_candidates)
        Ls_table.append(Lx_table)
        Ls_table_count.append(Lx_table_count)
    else:
        break

if len(Ls_table[-1]) == 0:
    Ls_table.remove(Ls_table[-1])
if len(Ls_table_count[-1]) == 0:
    Ls_table_count.remove(Ls_table_count[-1])

##################  Q1  #######################
# find frequent itemsets
F_keys = []
F_values = []
print('\nQuestion 1: (find frequent itemsets)')
if len(f_itemsets) == 0:
    print('None')
else:
    for key, value in f_itemsets.items():
        F_keys.append(key)
        F_values.append(value)
        if len(str(key)) <= 2:
            if not ',' in str(key):
                key = {key}
                print(key,'------->',value)
            else:
                print(set(key),'------->',value)
        else:
            print(set(key),'------->',value) 
print('Total:',len(f_itemsets))
##################  Q2  #######################
# output all the maximal frequent itemsets and closed frequent itemsets
        
max_f_itemsets,  clo_f_itemsets =  max_closed_f_set(f_itemsets, Ls_table, Ls_table_count) 
    
print('\nQuestion 2: (output all the maximal frequent itemsets and closed frequent itemsets)')
print('Maximal frequent itemsets:')
if len(max_f_itemsets) == 0:
    print('None')
else:
    
    for i in reversed(max_f_itemsets):
        if len(str(i)) <= 2:
            if not ',' in str(i):
                i = {i}
                print(i, end=' ')
            else:
                print(set(i), end=' ')
        else:
            print(set(i), end=' ')
    
print('\nTotal:',len(max_f_itemsets))
print('Closed frequent itemsets:')
if len(clo_f_itemsets) == 0:
    print('None')
else:
    for i in reversed(clo_f_itemsets):
        if len(str(i)) <= 2:
            if not ',' in str(i):
                i = {i}
                print(i, end=' ')
            else:
                print(set(i), end=' ')
        else:
            print(set(i), end=' ')
print('\nTotal:',len(clo_f_itemsets))

   
##################  Q3  #######################
# output all the association rules. Min-Confidence should be a user 
# input parameter. For all the association rules, output measures
# include confidence, lift, all-confidence and cosine similarity.
freq_sets = []
freq_count = []        
for i in range(len(F_keys)):
    if len(str(F_keys[i])) <= 2:
        if not ',' in str(F_keys[i]):
            temp = {F_keys[i]}
            freq_sets.append(temp)
            freq_count.append(F_values[i])
        else:
            freq_sets.append(set(F_keys[i]))
            freq_count.append(F_values[i])
    else:
        freq_sets.append(set(F_keys[i]))
        freq_count.append(F_values[i])
    
asso_body = []
asso_head = []
x_conf = []
x_lift = []
x_all_conf = []
x_cosine =[]
temp_conf = 0
temp_lift = 0
temp_all_conf = 0
temp_cosine = 0
for i in range(len(freq_sets)):
    if len(freq_sets[i]) >= 2:
        for j in range(len(freq_sets[i])):
            for k in range(1, len(freq_sets[i])):
                A = freq_sets[i]
                A_temp = [temp for temp in combinations(A, len(freq_sets[i])-k)]
                B = freq_sets[i] - set(A_temp[j])
                XY = freq_sets.index(A)
                X = freq_sets.index(B)
                Y = freq_sets.index(set(A_temp[j]))
                temp_conf = freq_count[XY]/freq_count[X]
                temp_lift = (freq_count[XY]/freq_count[X])/(freq_count[Y]/len(dataset))
                temp_all_conf = freq_count[XY]/max(freq_count[X],freq_count[Y])
                temp_cosine = freq_count[XY]/((freq_count[X]*freq_count[Y])**0.5)
                if temp_conf >= min_confidence:
                    asso_body.append(B)
                    asso_head.append(set(A_temp[j]))
                    x_conf.append(temp_conf)
                    x_lift.append(temp_lift)
                    x_all_conf.append(temp_all_conf)
                    x_cosine.append(temp_cosine)

print('\nQuestion 3: (output all the association rules with confidence, lift, all-confidence and cosine similarity)')
if len(asso_body) == 0:
    print('None')
else:
    for i in range(len(asso_body)):
        print(asso_body[i],'---->',asso_head[i],', Confidence =',round(x_conf[i],2),', Lift =',round(x_lift[i],2),', All-Confidence =',round(x_all_conf[i],2),', Cosine similarity =',round(x_cosine[i],2))
print('Total:',len(asso_body))

time_stop = process_time()
print('\nRun time:',(time_stop - time_start),'seconds\n')
















