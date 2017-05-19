#-*- coding: utf-8 -*-
import re
import random

# initialize list
word = []

# initialize dictionary
unigram_count = {}
bigram_count = {}
bigram_probability = {}


# file open directly
f = open('BROWN_A1.txt', 'rU')

data = f.read()
data = data.lower()
data = re.sub(r'"', '', data)
data = re.sub(r'[#~\-\\\{\}\(\)\<>;\[\]\:\*_]', ' ', data)
word = data.split()

f.close()
w = open('out.txt', 'w')

# unigram count
for num in word:
    unigram_count[num] = (unigram_count[num] + 1) if num in unigram_count.keys() else 1

# bigram count
for i in range(len(word) - 1):
    bigram_str = str(word[i]) + ' ' + str(word[i+1])
    bigram_count[bigram_str] = bigram_count[bigram_str] + 1 if bigram_str in bigram_count.keys() else 1

# bigram probability
for i in range(len(word) - 1):
    bigram_str = str(word[i]) + ' ' + str(word[i+1])
    bigram_probability[bigram_str] = float(bigram_count[bigram_str])/unigram_count[str(word[i])]

# extract
# 문장이 시작되는 부분만 추출해서 dictionary로 만듦. 
head_of_sentences_sorted = []
contain_start_of_sentence_regex = re.compile(r'\w+\. ([\w\',]+)') # 문장이 시작되는 부분을 추출하기 위한 정규표현식. bigram들 중에서 .으로 문장이 끝나는 부분과 그 다음 부분이 이어지는 것들을 골라서, .으로 끝나는 부분 뒷부분만 추출해내면 문장이 시작되는 부분을 추출해낼 수 있음. 
for key, value in sorted(bigram_probability.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    contain_head_of_sentence = contain_start_of_sentence_regex.match(key)
    if contain_head_of_sentence and contain_head_of_sentence.group(1) not in head_of_sentences_sorted:
        head_of_sentences_sorted.append(contain_head_of_sentence.group(1))

sentence_count = 1
for start in head_of_sentences_sorted:
    if sentence_count > 10:
        break
    word = start
    result = start
    end_of_sentence = re.compile(r'.+\.')

    while not end_of_sentence.match(word):
        # word로 시작하는 bigram들 중에서 빈도수가 높은 것들 5개를 추려내고 그 안에서 무작위 추출을 시행해서 다음 단어를 선택함. 문장의 끝, .으로 끝나는 부분을 만날 때까지 반복. 이러한 과정을 총 10번 반복함. 
        word_regex = re.compile(r''+re.escape(word)+r' (.+)')
        highest_ten = {}
        count = 0
        for key, value in sorted(bigram_probability.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
            word_key_match = word_regex.match(key)
            if word_key_match and count < 5:
                highest_ten[key] = value
                count += 1
            if count >= 5:
                break

        random_select_key = random.choice(highest_ten.keys())
        next_word = word_regex.match(random_select_key).group(1)
        result += ' '+ next_word
        word = next_word
    w.write(result + '\n')
    w.write('\n')
    sentence_count += 1
