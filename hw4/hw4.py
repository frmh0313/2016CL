#-*- coding: utf-8 -*-
import re
import math

# 알파벳과 blank를 카운트함.
def count_alphabets_blanks(letters_list):
    alphabet_regex = re.compile(r'[A-Z]')
    blank_regex = re.compile(r' ')
    letters_count_dict = {}
    for ch in letters_list:
        alphabet = alphabet_regex.match(ch)
        blank = blank_regex.match(ch)
        if alphabet:
            letters_count_dict[ch] = letters_count_dict[ch]+1 if ch in letters_count_dict.keys() else 1
        elif blank:
            letters_count_dict['blank'] = letters_count_dict['blank']+1 if 'blank' in letters_count_dict.keys() else 1
        else:
            pass
    return letters_count_dict

# 글자별 엔트로피 계산
def calc_letters_entropy(letters_count_dict, data_length):
    entropy_letters = {}
    for ch in letters_count_dict.keys():
        entropy_letters[ch] = (float(letters_count_dict[ch])/data_length)*math.log(data_length/float(letters_count_dict[ch]), 2)
    return entropy_letters

# 글자별 cross entropy 계산
def calc_letters_cross_entropy(training_letters_count_dict, cross_letters_count, training_data_length, cross_data_length):
    cross_entropy_dict = {}
    for ch in training_letters_count_dict.keys():
        if ch not in cross_letters_count:
            cross_entropy_dict[ch] = 0
        else:
            cross_entropy_dict[ch] = (float(cross_letters_count[ch])/cross_data_length)*math.log(training_data_length/float(training_letters_count_dict[ch]), 2)
    return cross_entropy_dict

# entropy의 합을 구함
def calc_entropy_sum(entropy_letters):
    entropy = 0
    for key, value in entropy_letters.items():
        entropy += value
    return entropy

training_corpus = open('./brown/training/BROWN1_A1.txt', 'rU')
brown_l1_to_r1_corpus = open('./brown/training/BROWN1_B1.txt', 'rU')
reuter_corpus = open('./Reutertest/acq/0009613', 'rU')

w = open('./out.txt', 'w')

# BROWN_A1 to BROWN_K1(training corpus)
training_data = training_corpus.read().upper()
training_letters_list = list(training_data)
len_training_data = len(training_data)

# BROWN_L1 to BROWN_R1
brown_l1_to_r1_data = brown_l1_to_r1_corpus.read().upper()
brown_l1_to_r1_letters_list = list(brown_l1_to_r1_data)
len_brown_l1_to_r1_data = len(brown_l1_to_r1_data)

# Reuter test corpus
reuter_data = reuter_corpus.read().upper()
reuter_letters_list = list(reuter_data)
len_reuter_data = len(reuter_data)

# letters counting in training corpus
training_letters_count = count_alphabets_blanks(training_letters_list)
# calculate the entropy of each letters in the training corpus
entropy_training_letters = calc_letters_entropy(training_letters_count, len_training_data)
# calculate the entropy of training corpus
entropy_training = calc_entropy_sum(entropy_training_letters)
# calculate the cross entropy of each letters in the training corpus
cross_entropy_training_letters = calc_letters_cross_entropy(training_letters_count, training_letters_count, len_training_data, len_training_data)
# calculate corss entropy of the training corpus
cross_entropy_training = calc_entropy_sum(cross_entropy_training_letters)

# letters counting in the BROWNL1-R1
brown_l1_to_r1_letters_count = count_alphabets_blanks(brown_l1_to_r1_letters_list)
# calculate the entropy of each letters in the BROWNL1-R1
entropy_brown_l1_r1_letters = calc_letters_entropy(brown_l1_to_r1_letters_count, len_brown_l1_to_r1_data)
# calculate the entropy of the BROWNL1-R1
entropy_brown_l1_r1 = calc_entropy_sum(entropy_brown_l1_r1_letters)
# calculate the cross entropy of each lettersin the BROWNL1-R1
cross_entropy_brown_l1_r1_letters = calc_letters_cross_entropy(training_letters_count, brown_l1_to_r1_letters_count, len_training_data, len_brown_l1_to_r1_data)
# calculate the cross entropy of the BROWNL1-R1
cross_entropy_brown_l1_r1 = calc_entropy_sum(cross_entropy_brown_l1_r1_letters)

# letters counting in Reuter test corpus
reuter_letters_count = count_alphabets_blanks(reuter_letters_list)
# calculate the entropy of each letters in the Reuter test corpus
entropy_reuter_letters = calc_letters_entropy(reuter_letters_count, len_reuter_data)
# calculate the entropy of the Reuter test corpus
entropy_reuter = calc_entropy_sum(entropy_reuter_letters)
# calculate the cross entropy of each letters in the Reuter test corpus
cross_entropy_reuter_letters = calc_letters_cross_entropy(training_letters_count, reuter_letters_count, len_training_data, len_reuter_data)
# calculate the cross entropy of the Reuter test corpus
cross_entropy_reuter = calc_entropy_sum(cross_entropy_reuter_letters)

w.write('Training\n')
w.write('Entropy: '+str(entropy_training)+'\n')
w.write('Cross Entropy: '+str(cross_entropy_training)+'\n')
w.write('Difference: '+str(abs(entropy_training-cross_entropy_training))+'\n\n') # 차의 절대값을 구함

w.write('BROWN1L1-R1\n')
w.write('Entropy: '+str(entropy_brown_l1_r1)+'\n')
w.write('Cross Entropy: '+str(cross_entropy_brown_l1_r1)+'\n')
w.write('Difference: '+str(abs(entropy_brown_l1_r1-cross_entropy_brown_l1_r1))+'\n\n')

w.write('Reuter Test Corpus\n')
w.write('Entropy: '+str(entropy_reuter)+'\n')
w.write('Cross Entropy: '+str(cross_entropy_reuter)+'\n')
w.write('Difference: '+str(abs(entropy_reuter - cross_entropy_reuter))+'\n\n')
