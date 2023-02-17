# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np

digs = np.arange(8,17)

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
    bases3 = bases.copy()

    # cross correlation
    I_seq_bases1 = []
    I_seq_bases2 = []
    I_seq_bases3 = []

    for base1 in bases1:
        for base2 in bases2:
            for base3 in bases3:
                if (str(base1) == str(base2)) or \
                   (str(base1) == str(base3)) or \
                   (str(base2) == str(base3)):
                       
                    cor_signal = np.concatenate([base1,base1]) + np.concatenate([base2,base2]) + np.concatenate([base3,base3])
                    auto_cor1 = becmm.any_base_analysis_1D(cor_signal, base1)[0]
                    auto_cor2 = becmm.any_base_analysis_1D(cor_signal, base2)[0]
                    auto_cor3 = becmm.any_base_analysis_1D(cor_signal, base3)[0]
                    
                else:
                    cor_signal = np.concatenate([base1,base1]) + np.concatenate([base2,base2]) + np.concatenate([base3,base3])
                    cross_cor_sig1 = becmm.any_base_analysis_1D(cor_signal, base1)
                    cross_cor_sig2 = becmm.any_base_analysis_1D(cor_signal, base2)
                    cross_cor_sig3 = becmm.any_base_analysis_1D(cor_signal, base3)
                    
                    auto_cor_flag = (cross_cor_sig1[0] == 1) and (cross_cor_sig2[0] == 1) and (cross_cor_sig3[0] == 1)
                    cross_cor_sum = np.sum(cross_cor_sig1[1:]) + np.sum(cross_cor_sig2[1:]) + np.sum(cross_cor_sig3[1:])
                    if auto_cor_flag and (cross_cor_sum == 0):
                        I_seq_bases1.append(base1)
                        I_seq_bases2.append(base2)
                        I_seq_bases3.append(base3)

        
    # print and save txt
    f = open('I_seq_3pair_dig'+str(dig).zfill(3)+'.txt','w')
    f.write('base1,base2,base3\n')
    for I_seq_base1,I_seq_base2,I_seq_base3 in zip(I_seq_bases1,I_seq_bases2,I_seq_bases3):
        print('base1:'+str(I_seq_base1)+' base2:'+str(I_seq_base2) + ' base3:' + str(I_seq_base3))
        f.write(str(I_seq_base1)+','+str(I_seq_base2)+','+str(I_seq_base3)+'\n')
    f.close()
    
