# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np
import itertools

digs = range(8,9)
pair_nums= range(4,5)

for pair_num in pair_nums:
    print('pair num:'+str(pair_num))
    for dig in digs:
        print('dig:'+str(dig))
        max_number = np.power(2,dig)
        numbers = np.arange(3,max_number-1)
        
        del max_number
        # remove no pattern
        remove_numbers = np.power(2,range(2,dig))
        for remove_number in remove_numbers:
            numbers = np.delete(numbers, numbers==remove_number)
                
        del remove_numbers
        # get all base patterns
        #pair_bases_num = np.array(list(itertools.combinations(numbers,pair_num)))
        pair_bases_num = itertools.combinations(numbers,pair_num)

        del numbers
        # transform
        pair_bases_sig = []
        for pair_base in pair_bases_num:
            pair_bases_sig_temp = []
            for base in pair_base:
                seq = '{:b}'.format(base).zfill(dig)
                base_temp = np.zeros(dig,dtype=np.uint8)
                for i,bit in enumerate(seq):
                    base_temp[i]=bit

                pair_bases_sig_temp.append(base_temp)

            pair_bases_sig.append(np.array(pair_bases_sig_temp,dtype=np.uint8))
        
        pair_bases_sig = np.array(pair_bases_sig,dtype=np.uint8)

        del pair_bases_num,pair_bases_sig_temp
        # calc correlation
        I_seq = []
        for pair_base in pair_bases_sig:
            cor_signal = np.sum(pair_base,axis=0)
            cor_signal = np.concatenate([cor_signal,cor_signal])
            
            auto_cor_flag = np.zeros(pair_num)
            cross_cor_flag = np.zeros(pair_num)
            for i,a_base in enumerate(pair_base):
                cross_cor_sig = becmm.any_base_analysis4I_seq(cor_signal, a_base)
           
                auto_cor_flag[i] = cross_cor_sig[0] == 1
                cross_cor_flag[i] = np.sum(cross_cor_sig[1:]) < 0.001
        
            if np.sum(auto_cor_flag) == pair_num and np.sum(cross_cor_flag) == pair_num:
                I_seq.append(pair_base)
        
        del pair_bases_sig,auto_cor_flag,cross_cor_flag
        # print and save txt
        f = open('I_seq_'+str(pair_num)+'pair_dig'+str(dig).zfill(3)+'.txt','w')
        f.write('base1')
        # write header
        for i in range(1,pair_num):
            f.write(',base'+str(i+1))
        f.write('\n')
        # wite data
        write_string = ''
        for seq in I_seq:
            for data in seq:
                write_string += str(data)+','
            write_string = write_string[:-1]+'\n'
        
        f.write(write_string)

        del write_string        
        f.close()

        