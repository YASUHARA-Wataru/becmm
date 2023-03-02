# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import base_extract_correlation_minimum_method as becmm
import numpy as np
import glob
import os

I_path = glob.glob('encrypt_I_seq\\*.txt')
I_path = [os.path.basename(x)[:-6] for x in I_path]

for path in glob.glob('encrypt_seq_c3\\*.txt'):
    
    file_name = os.path.basename(path)

    if '008' not in file_name:
        print('skip1')
        continue

    if file_name[:-4] in I_path:
        print('skip2')
        continue

    
    dig = int(file_name[20:23])
    base_str = file_name[24:24+dig]
    base1 = np.zeros(dig)
    for i,bit in enumerate(base_str):
        base1[i] = int(bit)

    input_f = open(path,'r')
    encrypt_I_seq = []
    print(base_str)
    
    for line in input_f:
        data = line[:-1].split(',')
        base2 = np.zeros(dig)
        for i,bit in enumerate(data):
            base2[i] = int(bit)
        
        # search other seq
        pair_num = 2
        max_number = np.power(2,dig)
        numbers = np.arange(3,max_number-1)
        
        # remove no pattern
        remove_numbers = np.power(2,range(2,dig))
        for remove_number in remove_numbers:
            numbers = np.delete(numbers, numbers==remove_number)
        
        # transform
        app_flag = True
        for c_base1 in numbers:
            seq = '{:b}'.format(c_base1).zfill(dig)
            comp_base1 = np.zeros(dig)
            for i,bit in enumerate(seq):
                comp_base1[i]=int(bit)
            
            for c_base2 in numbers:
                seq = '{:b}'.format(c_base1).zfill(dig)
                comp_base2 = np.zeros(dig)
                for i,bit in enumerate(seq):
                    comp_base2[i]=int(bit)
                
                if str(base1) == str(comp_base1):
                    continue
    
                main_sig_true = becmm.any_base_analysis_1D(np.concatenate([base1,[0]]), comp_base1)
                main_sig_false = becmm.any_base_analysis_1D(np.concatenate([base2,[0]]), comp_base1)
                sub_sig_true = becmm.any_base_analysis_1D(np.concatenate([base1,[0]]), comp_base2)
                sub_sig_false = becmm.any_base_analysis_1D(np.concatenate([base2,[0]]), comp_base2)
                
                if ((main_sig_true == 1) and (main_sig_false == 0)) or \
                   ((sub_sig_true == 1) and (sub_sig_false == 0)) or \
                   ((main_sig_true == 1) and (sub_sig_false == 0)) or \
                   ((sub_sig_true == 1) and (main_sig_false == 0)) :
                    app_flag = False
                
        if app_flag:
            encrypt_I_seq.append(base2)


    if len(encrypt_I_seq) != 0:
        output_f = open('encrypt_I_seq\\'+file_name[:-4]+'_I.txt','w')
        for data in encrypt_I_seq:
            write_str = ''
            
            for bit in data:
                write_str+=str(int(bit)) + ','
    
            write_str = write_str[:-1] + '\n'
            output_f.write(write_str)
        
        output_f.close()
    input_f.close()
                            