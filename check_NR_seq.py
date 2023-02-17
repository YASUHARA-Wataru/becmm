# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np

digs = np.arange(3,6)

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
    NR_seq_bases = []
    NR_seq_signs = []
    R_seq_bases = []
    R_seq_signs = []
    for base in bases:
        for signal in signals:
            if str(base) == str(signal[:dig]):
                auto_cor = becmm.any_base_analysis_1D(signal, base)[0]
            else:
                cross_cor = np.sum(becmm.any_base_analysis_1D(signal, base))            
                if cross_cor == 0:
                    NR_seq_bases.append(base)
                    NR_seq_signs.append(signal[:dig])
                else:
                    R_seq_bases.append(base)
                    R_seq_signs.append(signal)
    
    # print and save txt
    f = open('NR_seq_dig'+str(dig).zfill(3)+'.txt','w')
    f.write('base,signal\n')
    for NR_seq_base,NR_seq_sign in zip(NR_seq_bases,NR_seq_signs):
        print('base:'+str(NR_seq_base)+' sign:'+str(NR_seq_sign))
        f.write(str(NR_seq_base)+','+str(NR_seq_sign)+'\n')
    f.close()
    
    # check rotate
    for R_seq_base,R_seq_sign in zip(R_seq_bases,R_seq_signs):
        if str(R_seq_base)[1:-1] in str(R_seq_sign)[1:-1]:
            print('true')
            print('base:'+str(R_seq_base)+' signal:'+str(R_seq_sign))
        else:
            print('false')
            print('base:'+str(R_seq_base)+' signal:'+str(R_seq_sign))
    