# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 11:15:29 2023

@author: YASUHARA Wataru

MIT License
"""

import numpy as np
import base_extract_correlation_minimum_method as becmm

# encrypt test
encrypt_str = 'Hellow World. becmm encrypt test.'

print('encrypt_str: ' + encrypt_str)
bin_str = ''
for a_str in encrypt_str:
    bin_str += '{:0>7b}'.format(ord(a_str))
    #bin_str += a_str.encode('utf-8')

str_bin_array = np.zeros(len(bin_str),dtype=bool)
for i,bit in enumerate(bin_str):
    if bit == '1':
        str_bin_array[i] = True
    elif bit == '0':
        str_bin_array[i] = False

main_key = [1,1,1,1,0,0,1,0]
sub_key = [1,1,1,1,1,0,0,0]

mod_data = becmm.encrypt_bainary_mod(main_key, sub_key, str_bin_array)

demod_data = becmm.encrypt_bainary_demod(main_key, sub_key, mod_data)

de_bit_string = ''
for bit in demod_data:
    if bit:
        de_bit_string += '1'
    else:
        de_bit_string += '0'

demod_sting = ''
for i in range(0,int(len(de_bit_string)/7)):
    conbert_string = de_bit_string[i*7:(i+1)*7]
    #print(conbert_string)
    value = int(conbert_string,2)
    demod_sting += chr(value)
    
print('demod string: ' + demod_sting)

output_f = open('encrypt_research.txt','w')

digs = [6,7,8,9,10]
#digs = [8]

print(mod_data)

for dig in digs:
    print('dig: ' + str(dig))
    f = open('ND_seq\\ND_seq_2pair_dig'+str(dig).zfill(3)+'.txt','r')
    print(mod_data)
    output_f.write('dig: ' + str(dig) + '\n')
    
    for line in f:
        if line[:2] == '# ':
            continue

        data = line[:-1].split(',')
        de_main_key = np.array(data[:dig]).astype('i')
        de_sub_key = np.array(data[dig:]).astype('i')

        print(de_main_key)
        print(de_sub_key)
        
        output_f.write('de main key: ' + str(de_main_key) + ' de sub key:' + str(de_sub_key)+'\n')

        demod_data = becmm.encrypt_bainary_demod(de_main_key, de_sub_key, mod_data)
        
        de_bit_string = ''
        for bit in demod_data:
            if bit:
                de_bit_string += '1'
            else:
                de_bit_string += '0'
        
        demod_string = ''
        for i in range(0,int(len(de_bit_string)/7)):
            conbert_string = de_bit_string[i*7:(i+1)*7]
            value = int(conbert_string,2)
            demod_string += chr(value)

        print('demod string: ' + demod_string)
        output_f.write('demod string: ' + demod_string + '\n')
        if encrypt_str == demod_string:
            output_f.write('\n******************************************************************\n'+\
                             '*********************** success to demod!! ***********************\n'+
                             '******************************************************************\n\n')

output_f.close()