# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np

digs = range(6,7)
pair_nums= range(2,3)

for pair_num in pair_nums:
    print('pair num:'+str(pair_num))
    for dig in digs:
        print('dig:'+str(dig))
        max_number = np.power(2,dig)
        numbers = np.arange(3,max_number-1)
        
        # remove no pattern
        remove_numbers = np.power(2,range(2,dig))
        for remove_number in remove_numbers:
            numbers = np.delete(numbers, numbers==remove_number)
                
        # save txt
        f = open('I_seq_'+str(pair_num)+'pair_dig'+str(dig).zfill(3)+'.txt','w')
        # write header
        f.write('base1')
        for i in range(1,pair_num):
            f.write(',base'+str(i+1))
        f.write('\n')
        numbers_num = numbers.shape[0]
        bit_array = np.zeros(numbers_num)
        i = 0
        while np.sum(bit_array)!=numbers_num:
            cnt = int('0b'+str(bit_array.astype('i'))[-17:-1].replace(' ',''),2)
            print("\r"+str(cnt),end="")
            if np.sum(bit_array) == pair_num:
                pair_base = numbers[np.array(bit_array,dtype=bool)]
                #print(pair_base)
                # transform
                pair_bases_sig_temp = []
                for base in pair_base:
                    seq = '{:b}'.format(base).zfill(dig)
                    base_temp = np.zeros(dig,dtype=np.uint8)
                    for i,bit in enumerate(seq):
                        base_temp[i]=bit
    
                    pair_bases_sig_temp.append(base_temp)
    
                pair_bases_sig = np.array(pair_bases_sig_temp,dtype=np.uint8)
                # calc correlation
                cor_signal = np.sum(pair_bases_sig,axis=0)
                cor_signal = np.concatenate([cor_signal,cor_signal])
                
                auto_cor_flag = np.zeros(pair_num)
                cross_cor_flag = np.zeros(pair_num)
    
                for i,a_base in enumerate(pair_bases_sig):
                    cross_cor_sig = becmm.any_base_analysis4I_seq(cor_signal, a_base)
               
                    auto_cor_flag[i] = cross_cor_sig[0] == 1
                    cross_cor_flag[i] = np.sum(cross_cor_sig[1:]) < 0.001
            
                if np.sum(auto_cor_flag) == pair_num and np.sum(cross_cor_flag) == pair_num:
                    f.write(str(pair_bases_sig[0]))
                    for a_base in pair_bases_sig:
                        if str(a_base) == str(pair_bases_sig[0]):
                            continue
                        f.write(','+str(a_base))
                    f.write('\n')
            # bit add
            bit_array[0] = (bit_array[0] + 1)%2
            if bit_array[0] == 1:
                move_up_flag = False
            else:
                move_up_flag = True
                
            for i,bit in enumerate(bit_array):
                if move_up_flag and i != 0:
                    bit_array[i] = (bit_array[i]+1)%2
                    if bit_array[i] == 0:
                        move_up_flag = True
                    else:                        
                        move_up_flag = False
        f.close()

