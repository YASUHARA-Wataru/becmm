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
    ND_seq_bases = []
    ND_seq_signs = []
    D_seq_bases = []
    D_seq_signs = []
    for base in bases:
        for signal in signals:
            if str(base) == str(signal[:dig]):
                auto_cor = becmm.any_base_analysis_1D(signal, base)[0]
            else:
                cross_cor = np.sum(becmm.any_base_analysis_1D(signal, base))            
                if cross_cor == 0:
                    ND_seq_bases.append(base)
                    ND_seq_signs.append(signal[:dig])
                else:
                    D_seq_bases.append(base)
                    D_seq_signs.append(signal)
    
    # print and save txt
    f = open('ND_seq_dig'+str(dig).zfill(3)+'.txt','w')
    f.write('base,signal\n')
    for ND_seq_base,ND_seq_sign in zip(ND_seq_bases,ND_seq_signs):
        print('base:'+str(ND_seq_base)+' sign:'+str(ND_seq_sign))
        f.write(str(ND_seq_base)+','+str(ND_seq_sign)+'\n')
    f.close()
    
    # check rotate
    for D_seq_base,D_seq_sign in zip(D_seq_bases,D_seq_signs):
        if str(D_seq_base)[1:-1] in str(D_seq_sign)[1:-1]:
            print('true')
            print('base:'+str(D_seq_base)+' signal:'+str(D_seq_sign))
        else:
            print('false')
            print('base:'+str(D_seq_base)+' signal:'+str(D_seq_sign))
    