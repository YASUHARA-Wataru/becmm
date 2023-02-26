# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np
import itertools

digs = range(3,9)
pair_num = 2

print('pair num:'+str(pair_num))
for dig in digs:
    print('dig:'+str(dig))
    max_number = np.power(2,dig)
    numbers = np.arange(3,max_number-1)
    
    # remove no pattern
    remove_numbers = np.power(2,range(2,dig))
    for remove_number in remove_numbers:
        numbers = np.delete(numbers, numbers==remove_number)
    
    # get all base patterns
    pair_bases_num = np.array(list(itertools.permutations(numbers,pair_num)))
    
    # transform
    pair_bases_sig = []
    for base in numbers:
        seq = '{:b}'.format(base).zfill(dig)
        base_temp = np.zeros(dig)
        for i,bit in enumerate(seq):
            base_temp[i]=int(bit)

        pair_bases_sig.append(base_temp)

    # calc correlation
    encrypt_seq = []
    for main_base in pair_bases_sig:
        encrypt_seq_temp = []
        
        for sub_base in pair_bases_sig:
            if str(main_base) == str(sub_base):
                continue
            
            false_sig = becmm.any_base_analysis_1D(np.concatenate([sub_base,[0]]), main_base)
            rev_false_sig = becmm.any_base_analysis_1D(np.concatenate([main_base,[0]]), sub_base)
            
            if (false_sig == 0) and (rev_false_sig == 0):
                encrypt_seq_temp.append(sub_base)

        encrypt_seq.append(encrypt_seq_temp)
    
    # write data
    for number,base_sig,seq in zip(numbers,pair_bases_sig,encrypt_seq):
        # print and save txt
        f = open('encrypt_seq\\encrypt_seq_pair_dig'+str(dig).zfill(3)+'_'+'{:b}'.format(number).zfill(dig)+'.txt','w')
        
        if len(seq) == 0:
            continue

        for data in seq:
            write_str = ''
            for bit in data:
                write_str += str(int(bit))+','

            f.write(write_str[:-1]+'\n')
            
        f.close()

    