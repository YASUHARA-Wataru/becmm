# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np

digs = np.arange(6,17)

for dig in digs:
    print('dig:'+str(dig))
    max_number = np.power(2,dig)
    numbers = np.arange(0,max_number-1)
    bases = []
    
    # get all base
    for number in numbers:
        seq = '{:b}'.format(number).zfill(dig)
        base_temp = np.zeros(dig)
        for i,bit in enumerate(seq):
            base_temp[i] = int(bit)

        # select base
        if sum(base_temp) >= 2:
            bases.append(base_temp)
            
    bases = np.array(bases,dtype=np.int8)
    
    # make all signal and base
    bases1 = bases.copy()
    bases2 = bases.copy()

    # cross correlation
    I_seq_bases1 = []
    I_seq_bases2 = []

    for base1 in bases1:
        for base2 in bases2:
            if (str(base1) == str(base2)):
                cor_signal = np.concatenate([base1,base1]) + np.concatenate([base2,base2])
                auto_cor1 = becmm.any_base_analysis_1D(cor_signal, base1)[0]
                auto_cor2 = becmm.any_base_analysis_1D(cor_signal, base2)[0]
                
            else:
                cor_signal = np.concatenate([base1,base1]) + np.concatenate([base2,base2])
                cross_cor_sig1 = becmm.any_base_analysis_1D(cor_signal, base1)
                cross_cor_sig2 = becmm.any_base_analysis_1D(cor_signal, base2)
               
                auto_cor_flag = (cross_cor_sig1[0] == 1) and (cross_cor_sig2[0] == 1)
                cross_cor_sum = np.sum(cross_cor_sig1[1:]) + np.sum(cross_cor_sig2[1:])
                if auto_cor_flag and (cross_cor_sum == 0):
                    I_seq_bases1.append(base1)
                    I_seq_bases2.append(base2)

    # remove overlap
    I_bases_temp = np.concatenate([np.array(I_seq_bases1).reshape((len(I_seq_bases1),dig)),np.array(I_seq_bases2).reshape((len(I_seq_bases2),dig))],axis=1)
    I_bases = I_bases_temp.copy()
    I_bases_hist = []
    
    for I_base_temp in I_bases_temp:
        comp_base = np.concatenate([I_base_temp[dig:],I_base_temp[:dig]])
        I_bases_hist.append(str(comp_base))
        
        if str(I_base_temp) in np.array(I_bases_hist):
            continue
            
        if comp_base in I_bases:
            ind_cnt = 0
            for I_base in I_bases:
                if str(I_base) == str(comp_base):
                    del_ind = ind_cnt
                    continue
                ind_cnt+=1
            I_bases = np.delete(I_bases,del_ind,axis=0)

    if I_bases.shape[0] == 0:
        continue
    
    # print and save txt
    f = open('I_seq_2pair_dig'+str(dig).zfill(3)+'.txt','w')
    f.write('base1,base2\n')
    for I_seq_base in I_bases:
        #print('base1:'+str(I_seq_base[:dig])+' base2:'+str(I_seq_base[dig:]))
        f.write(str(I_seq_base[:dig])+','+str(I_seq_base[dig:])+'\n')
    f.close()
    
