# -*- coding: utf-8 -*-
"""
@author: YASUHARA WATARU

MIT License

"""
import numpy as np

def freq_analysis_1D(data):
    """
    Parameters
    ----------
    data : 1D-array
        1D-array Data.

    Raises
    ------
    Exception
        If Data is not 1D-array, raises error

    Returns
    -------
    stan_freq_num : TYPE
        Freqs value.

    """
    data = np.array(data)

    if data.flatten().shape[0] != len(list(data)):
        raise Exception('data is not 1D array.')

    if np.min(data) > 0:

        data_num = data.shape[0]
        max_freqs = int(data_num/2)+1
        freq_nums = np.zeros(max_freqs-1,dtype='f')
        
        for freq in range(1,max_freqs):
            for i in range(data_num-freq-1):
                freq_nums[freq-1] += np.min([data[i],data[i+freq+1]])

    else:
        
        data_min = np.min(data)
        data = data - data_min
        
        data_num = data.shape[0]
        max_freqs = int(data_num/2)+1
        freq_nums = np.zeros(max_freqs-1,dtype='f')
        
        for freq in range(1,max_freqs):
            for i in range(data_num-freq-1):
                freq_nums[freq-1] += np.min([data[i],data[i+freq+1]])

        freq_nums = freq_nums + data_min
        
    # normalize
    bin_nums = np.arange(data_num-1,data_num-max_freqs,-1)
    stan_freq_num = freq_nums/bin_nums

    return stan_freq_num
    

def freq_analysis_2D(data):
    """
    Parameters
    ----------
    data : 2D-array
        2D-array Data.

    Raises
    ------
    Exception
        If Data is not 2D-array, raises error

    Returns
    -------
    stan_freq_num : TYPE
        Freqs value.

    """

    data = np.array(data)

    if np.array(data.shape).shape[0] != 2:
        raise Exception('data is not 2D array.')

    if np.min(data) > 0:

        data_dim1 = data.shape[0]
        data_dim2 = data.shape[1]
    
        freqs_rank1 = int(data_dim1/2)+1
        freqs_rank2 = int(data_dim2/2)+1
        freq_nums = np.zeros((freqs_rank1,freqs_rank2),dtype='f')
        
    
        for freq1 in range(freqs_rank1):
            for freq2 in range(freqs_rank2):            
                for i in range(data_dim1-freq1-1):
                    for j in range(data_dim2-freq2-1):
                        interest1_data = data[i,j]
                        interest2_data = data[i+freq1,j+freq2]
                        interest3_data = data[i,j+freq2]
                        interest4_data = data[i+freq1,j+freq2]
                        interest_data = [interest1_data,
                                            interest2_data,
                                            interest3_data,
                                            interest4_data]
                        freq_nums[freq1,freq2] += np.min(interest_data)
    else:
        
        data_min = np.min(data)
        data = data - data_min
        
        data_dim1 = data.shape[0]
        data_dim2 = data.shape[1]

        freqs_rank1 = int(data_dim1/2)+1
        freqs_rank2 = int(data_dim2/2)+1
        freq_nums = np.zeros((freqs_rank1,freqs_rank2),dtype='f')
        
        for freq1 in range(freqs_rank1):
            for freq2 in range(freqs_rank2):            
                for i in range(data_dim1-freq1-1):
                    for j in range(data_dim2-freq2-1):
                        interest1_data = data[i,j]
                        interest2_data = data[i+freq1,j+freq2]
                        interest3_data = data[i,j+freq2]
                        interest4_data = data[i+freq1,j+freq2]
                        interest_data = [interest1_data,
                                            interest2_data,
                                            interest3_data,
                                            interest4_data]
                        freq_nums[freq1,freq2] += np.min(interest_data)

        freq_nums = freq_nums - data_min

    # normalize
    rank1_nums = np.arange(data_dim1,data_dim1-freqs_rank1,-1).reshape((freqs_rank1,1))
    rank2_nums = np.arange(data_dim2,data_dim2-freqs_rank2,-1).reshape((1,freqs_rank2))
    bin_nums = np.dot(rank1_nums,rank2_nums)
        
    stan_freq_num = freq_nums/bin_nums

    return stan_freq_num

def continuous_analisys_1D(data):
    """
    Parameters
    ----------
    data : TYPE
        1D-array Data.

    Raises
    ------
    Exception
        If Data is not 1D-array, raises error
        If Data contains negative value, raises error

    Returns
    -------
    stan_continuous_num : TYPE
        continuous num.

    """
    
    if np.min(data) < 0:
        raise Exception('data contains negative.')

    data = np.array(data)
    if data.flatten().shape[0] != len(list(data)):
        raise Exception('data is not 1D array.')

    data_num = data.shape[0]
    continuous_num = np.zeros_like(data)
    
    for continuous in range(0,data_num):
        for i in range(data_num-continuous):
            continuous_num[continuous] += np.min(data[i:i+continuous+1])
            

    # normalize
    bin_nums = np.arange(data_num,0,-1)
    stan_continuous_num = continuous_num/bin_nums

    return stan_continuous_num

def continuous_analisys_2D(data):
    """
    Parameters
    ----------
    data : 2D-array
        2D-array Data.
        If Data contains negative value, raises error

    Raises
    ------
    Exception
        If Data is not 2D-array, raises error
        If Data contains negative value, raises error

    Returns
    -------
    stan_continuous_num : TYPE
        continuous num.

    """
    data = np.array(data)

    if np.min(data) < 0:
        raise Exception('data contains negative.')

    if np.array(data.shape).shape[0] != 2:
        raise Exception('data is not 2D array.')

    data_dim1 = data.shape[0]
    data_dim2 = data.shape[1]
    continuous_num = np.zeros_like(data)

    for continuous1 in range(0,data_dim1):
        for continuous2 in range(0,data_dim2):
            for i in range(data_dim1-continuous1):
                for j in range(data_dim2-continuous2):
                    continuous_num[continuous1,continuous2] += np.min(data[i:i+continuous1+1,j:j+continuous2+1])

    # normalize
    rank1_nums = np.arange(data_dim1,0,-1).reshape((data_dim1,1))
    rank2_nums = np.arange(data_dim2,0,-1).reshape((1,data_dim2))
    bin_nums = np.dot(rank1_nums,rank2_nums)
    stan_continuous_num = continuous_num/bin_nums

    return stan_continuous_num

def any_base_analysis_1D(data,base):
    """
    Parameters
    ----------
    data : TYPE
        1D-array Data
    base : TYPE
        1D-array base

    Raises
    ------
    Exception
        If Data is not 1D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base not zero value absoulte min is not 1 , raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        DESCRIPTION.

    """
    data = np.array(data)
    base = np.array(base)


    if data.flatten().shape[0] != len(list(data)) :
        raise Exception('data is not 1D array.')

    if np.min(data) < 0:
        raise Exception('data can\'t contain negative values.')

    if np.min(base) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(base)[np.abs(base) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    data_num = data.shape[0]
    base_num = base.shape[0]
    
    if data_num < base_num:
        raise Exception('base is too large.')

    if 1 not in np.abs(base):
        raise Exception('base must contain 1.')
    
    cor_result = np.zeros(data_num - base_num,dtype='f')
    for i in range(data_num-base_num):
        data_cut = data[i:i+base_num]
        calc_index = base > 0.001
        cor_result[i] = np.min(data_cut[calc_index]/base[calc_index])
        
    return cor_result

def any_base_analysis4I_seq(data,base):
    """
    Parameters
    ----------
    data : TYPE
        1D-array Data
    base : TYPE
        1D-array base

    Raises
    ------
    Exception
        If Data is not 1D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base not zero value absoulte min is not 1 , raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        DESCRIPTION.

    """
    data = np.array(data)
    base = np.array(base)


    if data.flatten().shape[0] != len(list(data)) :
        raise Exception('data is not 1D array.')

    if np.min(data) < 0:
        raise Exception('data can\'t contain negative values.')

    if np.min(base) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(base)[np.abs(base) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    data_num = data.shape[0]
    base_num = base.shape[0]
    
    if data_num < base_num:
        raise Exception('base is too large.')

    if 1 not in np.abs(base):
        raise Exception('base must contain 1.')
    
    cor_result = np.zeros(data_num - base_num,dtype=np.uint8)
    for i in range(data_num-base_num):
        data_cut = data[i:i+base_num]
        calc_index = base > 0.001
        cor_result[i] = np.min(data_cut[calc_index]/base[calc_index])
        
    return cor_result

            
def any_base_analysis_2D(data,base):
    """
    Parameters
    ----------
    data : TYPE
        2D-array Data
    base : TYPE
        2D-array base

    Raises
    ------
    Exception
        If Data is not 2D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base not zero value absoulte min is not 1 , raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        cor_result

    """
    data = np.array(data)
    base = np.array(base)

    if np.array(data.shape).shape[0] != 2:
        raise Exception('data is not 2D array.')

    if np.min(data) < 0:
        raise Exception('data can\'t contains negative values.')

    if np.min(base) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(base)[np.abs(base) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
    
    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    data_num_dim1 = data.shape[0]
    data_num_dim2 = data.shape[1]
    base_num_dim1 = base.shape[0]
    base_num_dim2 = base.shape[1]
    
    if data_num_dim1 < base_num_dim1:
        raise Exception('base Dim1 is too large.')
    if data_num_dim2 < base_num_dim2:
        raise Exception('base Dim2 is too large.')

    if 1 not in np.abs(base):
        raise Exception('base must contain 1.')
    
    cor_result = np.zeros((data_num_dim1 - base_num_dim1,data_num_dim2 - base_num_dim2),dtype='f')
    for i in range(data_num_dim1-base_num_dim1):
        for j in range(data_num_dim2-base_num_dim2):
            data_cut = data[i:i+base_num_dim1,j:j+base_num_dim2]
            calc_index = base > 0.001
            cor_result[i,j] = np.min(data_cut[calc_index]/base[calc_index])
        
    return cor_result

def any_base_analysis4img(data,base):
    """
    Parameters
    ----------
    data : TYPE
        2D-array Data
    base : TYPE
        2D-array base

    Raises
    ------
    Exception
        If Data is not 2D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        cor_result

    """
    data = np.array(data)
    base = np.array(base)

    if np.array(data.shape).shape[0] != 2:
        raise Exception('data is not 2D array.')

    if np.min(data) < 0:
        raise Exception('data can\'t contains negative values.')

    if np.min(base) < 0:
        raise Exception('base can\'t contain negative values.')
   
    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    data_num_dim1 = data.shape[0]
    data_num_dim2 = data.shape[1]
    base_num_dim1 = base.shape[0]
    base_num_dim2 = base.shape[1]
    
    if data_num_dim1 < base_num_dim1:
        raise Exception('base Dim1 is too large.')
    if data_num_dim2 < base_num_dim2:
        raise Exception('base Dim2 is too large.')

    cor_result = np.zeros((data_num_dim1 - base_num_dim1,data_num_dim2 - base_num_dim2),dtype='f')
    for i in range(data_num_dim1-base_num_dim1):
        for j in range(data_num_dim2-base_num_dim2):
            data_cut = data[i:i+base_num_dim1,j:j+base_num_dim2]
            calc_index = base > 0.001
            cor_result[i,j] = np.min(data_cut[calc_index]/base[calc_index])
        
    return cor_result

        
def any_base_analysis_1D_with_negative(data,base):
    """
    Warnings:
        Recommend to use "any_base_analysis_1D()".  
        this function result is difficult to analyize.  
        You should plus minimum value of data to data and 
        use "any_base_analysis_1D()",
        and after calc plus minimum value.

    Parameters
    ----------
    data : TYPE
        1D-array Data
    base : TYPE
        1D-array base

    Raises
    ------
    Exception
        If Data is not 1D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base not zero value absoulte min is not 1 , raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        DESCRIPTION.

    """
    data = np.array(data)
    base = np.array(base)

    if data.flatten().shape[0] != len(list(data)) :
        raise Exception('data is not 1D array.')
        
    data_num = data.shape[0]
    base_num = base.shape[0]
    
    if data_num < base_num:
        raise Exception('base is too large.')
    
    if np.min(np.abs(base)[np.abs(base) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')

    if 1 not in np.abs(base):
        raise Exception('base must contain 1 or -1.')

    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')
    
    cor_result = np.zeros(data_num - base_num,dtype='f')
    for i in range(data_num-base_num):
        data_cut = data[i:i+base_num]
        calc_index = base != 0 # maybe no problem using float
        temp_cor = data_cut[calc_index]/base[calc_index]
        ex_cor = temp_cor[temp_cor>=0] # reject negative value
        if len(ex_cor) > 0:
            cor_result[i] = np.min(ex_cor)
        
    return cor_result
            
def any_base_analysis_2D_with_negative(data,base):
    """
    Warnings:
        Recommend to use "any_base_analysis_2D()".  
        this function result is difficult to analyize.  
        You should plus minimum value of data to data and 
        use "any_base_analysis_2D()",
        and after calc plus minimum value.

    Parameters
    ----------
    data : TYPE
        2D-array Data
    base : TYPE
        2D-array base

    Raises
    ------
    Exception
        If Data is not 2D-array, raises error
        If Data contains negative value, raises error
        If base contains negative value, raises error
        If base is lager than Data, raises error
        If base not zero value absoulte min is not 1 , raises error
        If base do not contain more than 2 values without 0 , raises error
        cause there is no pattern.

    Returns
    -------
    cor_result : TYPE
        cor_result

    """
    data = np.array(data)
    base = np.array(base)
 
    if np.array(data.shape).shape[0] != 2:
        raise Exception('data is not 2D array.')
 
    data_num_dim1 = data.shape[0]
    data_num_dim2 = data.shape[1]
    base_num_dim1 = base.shape[0]
    base_num_dim2 = base.shape[1]
    
    if data_num_dim1 < base_num_dim1:
        raise Exception('base Dim1 is too large.')
    if data_num_dim2 < base_num_dim2:
        raise Exception('base Dim2 is too large.')

    if np.min(np.abs(base)[np.abs(base) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')

    if 1 not in np.abs(base):
        raise Exception('base must contain 1 or -1.')

    if np.sum(np.abs(base) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')
    
    cor_result = np.zeros((data_num_dim1 - base_num_dim1,data_num_dim2 - base_num_dim2),dtype='f')
    for i in range(data_num_dim1-base_num_dim1):
        for j in range(data_num_dim2-base_num_dim2):
            data_cut = data[i:i+base_num_dim1,j:j+base_num_dim2]
            calc_index = base != 0 # maybe no problem using float
            temp_cor = data_cut[calc_index]/base[calc_index]
            ex_cor = temp_cor[temp_cor>=0] # reject negative value
            if len(ex_cor) > 0:
                cor_result[i,j] = np.min(ex_cor)
        
    return cor_result

def any_base_analysis_1D_with_negative_add_min(data,base):
    """
    Parameters
    ----------
    data : TYPE
        2D-array Data
    base : TYPE
        2D-array base

    Raises
    ------
    Exception

    Returns
    -------
    cor_result : TYPE
        cor_result

    """
    raise Exception('maybe do not defined every case. developing....')

    return 

def any_base_analysis_2D_with_negative_add_min(data,base):
    """
    Parameters
    ----------
    data : TYPE
        1D-array Data
    base : TYPE
        1D-array base

    Raises
    ------
    Exception

    Returns
    -------
    cor_result : TYPE
        DESCRIPTION.

    """
    raise Exception('maybe do not defined every case.developing...')

    return 

def encrypt_bainary_mod(main_key,sub_key,binary_data):
    """
    Parameters
    ----------
    main_key : TYPE
        DESCRIPTION.
    sub_key : TYPE
        DESCRIPTION.
    binary_data : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    mod_data : TYPE
        DESCRIPTION.

    """
    
    main_key = np.array(main_key,dtype=bool)
    sub_key = np.array(sub_key,dtype=bool)
    binary_data = np.array(binary_data,dtype=bool)
    
    if main_key.flatten().shape[0] != len(list(main_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(main_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(main_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(main_key)[np.abs(main_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(main_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if sub_key.flatten().shape[0] != len(list(sub_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(sub_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(sub_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(sub_key)[np.abs(sub_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(sub_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if main_key.shape[0] != sub_key.shape[0]:
        raise Exception('main key and sub key must be same length.')
    
    mod_data = np.zeros(binary_data.shape[0]*main_key.shape[0],dtype=bool)
    for i,bit in enumerate(binary_data):
        if bit == 1:
            mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]] = main_key
        elif bit == 0:
            mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]] = sub_key
        else:
            raise Exception('data is not binary.')
    
    return mod_data

def encrypt_bainary_demod(main_key,sub_key,mod_data):
    
    main_key = np.array(main_key)
    sub_key = np.array(sub_key)
    mod_data = np.array(mod_data)
    
    if main_key.flatten().shape[0] != len(list(main_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(main_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(main_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(main_key)[np.abs(main_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(main_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if sub_key.flatten().shape[0] != len(list(sub_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(sub_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(sub_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(sub_key)[np.abs(sub_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(sub_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if main_key.shape[0] != sub_key.shape[0]:
        raise Exception('main key and sub key must be same length.')
    
    demod_data = np.zeros(int(mod_data.shape[0]/main_key.shape[0]),dtype=bool)
    for i in range(0,int(mod_data.shape[0]/main_key.shape[0])):
        cut_data = mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]]
        main_ex_index = main_key == True
        sub_ex_index = sub_key == True
        main_bit =  cut_data[main_ex_index].flatten().all()
        sub_bit = cut_data[sub_ex_index].flatten().all()

        if main_bit and (not sub_bit):
            demod_data[i] = True
        else:
            demod_data[i] = False
            
    return demod_data


def encrypt_bainary_mod_add_rand_bit(main_key,sub_key,binary_data):
    """
    Parameters
    ----------
    main_key : TYPE
        DESCRIPTION.
    sub_key : TYPE
        DESCRIPTION.
    binary_data : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    mod_data : TYPE
        DESCRIPTION.

    """
    
    main_key = np.array(main_key,dtype=bool)
    sub_key = np.array(sub_key,dtype=bool)
    binary_data = np.array(binary_data,dtype=bool)
    
    if main_key.flatten().shape[0] != len(list(main_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(main_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(main_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(main_key)[np.abs(main_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(main_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if sub_key.flatten().shape[0] != len(list(sub_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(sub_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(sub_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(sub_key)[np.abs(sub_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(sub_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if main_key.shape[0] != sub_key.shape[0]:
        raise Exception('main key and sub key must be same length.')
    
    mod_data = np.zeros(binary_data.shape[0]*main_key.shape[0],dtype=bool)
    for i,bit in enumerate(binary_data):
        if bit == 1:
            mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]] = main_key
        elif bit == 0:
            mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]] = sub_key
        else:
            raise Exception('data is not binary.')
    
    return mod_data

def encrypt_bainary_mod_add_rand_bit(main_key,sub_key,mod_data):
    
    main_key = np.array(main_key)
    sub_key = np.array(sub_key)
    mod_data = np.array(mod_data)
    
    if main_key.flatten().shape[0] != len(list(main_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(main_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(main_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(main_key)[np.abs(main_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(main_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if sub_key.flatten().shape[0] != len(list(sub_key)) :
        raise Exception('main_key is not 1D array.')

    if np.min(sub_key) < 0:
        raise Exception('main_key can\'t contain negative values.')

    if np.min(sub_key) < 0:
        raise Exception('base can\'t contain negative values.')

    if np.min(np.abs(sub_key)[np.abs(sub_key) > 0]) != 1:
        raise Exception('base not zero value absolute min must be 1.')
        
    if np.sum(np.abs(sub_key) > 0) < 2:
        raise Exception('base must contain 2 values which is not 0.')

    if main_key.shape[0] != sub_key.shape[0]:
        raise Exception('main key and sub key must be same length.')
    
    demod_data = np.zeros(int(mod_data.shape[0]/main_key.shape[0]),dtype=bool)
    for i in range(0,int(mod_data.shape[0]/main_key.shape[0])):
        cut_data = mod_data[i*main_key.shape[0]:(i+1)*main_key.shape[0]]
        main_ex_index = main_key == True
        sub_ex_index = sub_key == True
        main_bit =  cut_data[main_ex_index].flatten().all()
        sub_bit = cut_data[sub_ex_index].flatten().all()

        if main_bit and (not sub_bit):
            demod_data[i] = True
        else:
            demod_data[i] = False
            
    return demod_data


def main():

    # test freq_analysis_1D
    value = np.zeros(100)
    value[::5] = 1
    freq_nums = freq_analysis_1D(value)
    print('freq_nums:\n' + str(freq_nums))
    
    # test_freq_analysis_2D
    value = np.zeros((40,30))
    value[::5,:] = 1
    value[:,::5] = 1
    freq_nums = freq_analysis_2D(value)
    print(freq_nums)

    # test_continuous_analysis_1D
    value = np.zeros(50)
    value[10:30] = 1
    continuous_num = continuous_analisys_1D(value)
    print(continuous_num)

    # test_continuous_analysis_2D
    value = np.zeros((50,50))
    value[0:40,0:20] = 1
    value[0:50,0:20] += 1
    continuous_num = continuous_analisys_2D(value)
    print(continuous_num)

    # test any_base_analysis_1D
    value = np.zeros(100)
    base = np.array([1,0,0,1,0,1])
    value[::5] = 1
    value[::3] += 1
    cor_result = any_base_analysis_1D(value,base)
    print('any_1D_cor_result:\n' + str(cor_result))
    # test any_base_analysis_2D
    value = np.zeros((100,100),dtype='f')
    base = np.array([[1,0,1,0],
                     [0,0,0,0],
                     [1,0,2,0],
                     [0,0,0,1]],dtype='f')
    value[:4,:4] = base
    value[2:6,2:6] += base
    print('base:\n'+str(base))
    print('value:\n'+str(value))
    cor_result = any_base_analysis_2D(value,base)
    print('any_2d_cor_result:\n' + str(cor_result))
    
    # test any_base_analysis4img
    value = np.zeros((100,100),dtype='f')
    base = np.array([[1,0,1,0],
                     [0,0,0,0],
                     [1,0,2,0],
                     [0,0,0,1]],dtype='f')
    value[:4,:4] = base
    value[2:6,2:6] += base
    print('base:\n'+str(base))
    print('value:\n'+str(value))
    cor_result = any_base_analysis4img(value,base)
    print('any_2d_cor_result:\n' + str(cor_result))

    # test any_base_analysis_1D
    value = np.zeros(100)
    base = np.array([1,0,0,-1,0,1])
    value[:6] = base
    print(value)
    print(base)
    cor_result = any_base_analysis_1D_with_negative(value,base)
    print('wn_cor_result:\n' + str(cor_result))
    
    # test any_base_analysis_2D
    value = np.zeros((100,100))
    base = np.array([[1,0,1,0],
                     [0,0,0,0],
                     [1,0,-5,0],
                     [0,0,0,1]])
    value[:4,:4] = base
    #value[2,2] = 1
    value[2:6,2:6] += base
    value[1:5,2:6] += base
    print('base:\n'+str(base))
    print('value:\n'+str(value))
    cor_result = any_base_analysis_2D_with_negative(value,base)
    np.savetxt('test.txt',cor_result)
    print('wn_cor_result:\n' + str(cor_result))


if __name__ == "__main__":
    main()
