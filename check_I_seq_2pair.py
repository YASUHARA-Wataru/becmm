# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np

digs = np.arange(3,9)

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
    signals = np.concatenate([bases,bases],axis=1)

    # cross correlation
    I_seq_bases = []
    I_seq_signs = []
    for base in bases:
        for signal in signals:
            if str(base) == str(signal[:dig]):
                auto_cor = becmm.any_base_analysis_1D(signal, base)[0]
            else:
                cor_signal = signal + np.concatenate([base,base])
                #print('sig:'+str(cor_signal))
                cross_cor_sig = becmm.any_base_analysis_1D(cor_signal, base)
                #print('cor:'+str(cross_cor_sig))
                cross_cor_sum = np.sum(cross_cor_sig[1:])
                if (cross_cor_sig[0] == 1) and (cross_cor_sum == 0):
                    I_seq_bases.append(base)
                    I_seq_signs.append(signal[:dig])
    
    # print and save txt
    f = open('I_seq_2pair_dig'+str(dig).zfill(3)+'.txt','w')
    f.write('base,signal\n')
    for I_seq_base,I_seq_sign in zip(I_seq_bases,I_seq_signs):
        print('base:'+str(I_seq_base)+' sign:'+str(I_seq_sign))
        f.write(str(I_seq_base)+','+str(I_seq_sign)+'\n')
    f.close()
    
