#-*- coding: utf-8 -*-
import re
#WordCount1.py
#WordCount using Dictionary

#open system modules
import sys

#initialize list
word=[]

#initialize dictionary
vowel_consonant_dict={}
ab_ba_dict={}
consecutive_consonant_dict={}

#file open direclty
f = open('BROWN_A1.txt', 'rU')
vowel_consonant_write = open('vowel_consonant.txt', 'w') # 모음으로 시작하고 자음으로 시작하는 경우 
ab_ba_write = open('ab_ba.txt', 'w') # a와 b가 이웃한 경우 
consecutive_consonant_write = open('consecutive_consonant.txt', 'w') # 두 개의 연속된 자음으로 시작하는 단어

#to read whole file using read()

data = f.read()

# pre-processing
data = data.lower() # case insensitve하게. 대소문자 차이만 나는 것은 같은 단어로 간주하여 count하기 위해 전부 소문자로 바꿈. 고유명사 구분에 문제가 생길 수 있지만, 고유명사가 아닌 단어들이 더 많고, 고유명사의 경우 일반명사들이 고유명사화 된 경우가 아니면 대소문자가 바뀌어서 의미가 달라지는 경우는 없을 것으로 생각되어 대소문자의 구분을 없는 것으로 하고 시작. 
data = re.sub(r'[\W_]', ' ', data) # 특수문자를 공백으로 치환. 

word = data.split()

f.close()

# making dictionary
for num in word:
    vowel_consonant = re.search(r'\b^[aeiouAEIOU].*[^\W\daeiouAEIOU_]$', num)
    ab_ba = re.search(r'[aA][bB]|[bB][aA]',num)
    consecutive_consonant = re.search(r'^[^\W\daeiouAEIOU_][^\W\daeiouAEIOU_][\W\daeiouAEIOU_]*',num)

    if vowel_consonant:
	vowel_consonant_dict[num] = (vowel_consonant_dict[num] + 1) if num in vowel_consonant_dict.keys() else 1
	
    if ab_ba:
        ab_ba_dict[num] = (ab_ba_dict[num]+1) if num in ab_ba_dict.keys() else 1

    if consecutive_consonant:
        consecutive_consonant_dict[num] = (consecutive_consonant_dict[num]+1) if num in consecutive_consonant_dict.keys() else 1


#making output file
for key, value in sorted(vowel_consonant_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True): 
     vowel_consonant_write.write("%r : %r" % (key, value))
     vowel_consonant_write.write("\n")

vowel_consonant_write.write(str(len(vowel_consonant_dict.keys())))

for key, value in sorted(ab_ba_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    ab_ba_write.write("%r : %r" % (key, value))
    ab_ba_write.write("\n")

ab_ba_write.write(str(len(ab_ba_dict.keys())))

for key, value in sorted(consecutive_consonant_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    consecutive_consonant_write.write("%r : %r" % (key, value))
    consecutive_consonant_write.write("\n")

consecutive_consonant_write.write(str(len(consecutive_consonant_dict.keys())))
