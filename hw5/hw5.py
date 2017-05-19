#-*- coding: utf-8 -*-

import re
import math
import os

# initialize list
word_list = []
bigram_list = []
bigram_filtered = []

# initialie dictionary
unigram_count = {}
unigram_probability = {}
bigram_count = {}
bigram_probability = {}
t_score = {}
chi_square = {}
mutual_information = {}

corpus_list = os.listdir('./brown_200_tagged/')

for filename in corpus_list:
    f = open('./brown_200_tagged/'+filename, 'rU')
    data = f.read()
    splited = data.split()
    word_list.extend(splited)
    f.close()

N = len(word_list)

w = open('out.txt', 'w')

# unigram count
print 'unigram count'
for word in word_list:
    unigram_count[word] = (unigram_count[word] + 1) if word in unigram_count.keys() else 1

# extract bigram list
print 'extract bigram list'
for i in range(len(word_list) - 1):
    bigram_str = str(word_list[i]) + ' ' + str(word_list[i+1])
    bigram_list.append(bigram_str)

for bigram in bigram_list:
    # 명사 + 형용사, 형용사 + 명사, 바이그램의 각 단어들이 대문자로 시작하는 경우(New York과 같은 고유명사를 골라내기 위해), 부사 + 형용사, 부사 + 동사, 동사 + 부사를 filtering.
    re_filter = re.compile('(\w+\/jj[rs]?\w* \w+\/nn)|\
            (\w+\/nn([sp]|ps)?\w* \w+\/jj[rs]?\w*)|\
            (\w+\/jj[rs]?\w* \w+\/nn([sp]|ps)?\w*)|\
            ([A-Z]\w+\/\w+ [A-Z]\w+)|\
            (\w+\/ql\w* \w+\/vb[dgnpz]?\w*)|\
            (\w+\/ql\w* \w+\/jj[rs]?\w*)|\
            (\w+\/rb[rt]? \w+\/jj[rs]\w*)|\
            (\w+\/rb[rt]? \w+\/vb[dgnpz]?\w*)|\
            (\w+/vb[dgnpz]?\w* \w+\/rb\w*)')
    if re_filter.match(bigram):
        bigram_filtered.append(bigram)

# bigram count
print 'bigram count'
for word in bigram_filtered:
    bigram_count[word] = (bigram_count[word] + 1) if word in bigram_count.keys() else 1

# calculate unigram probability
print 'calculate unigram probability'
for word in word_list:
    unigram_probability[word] = float(unigram_count[word])/N

# calculate bigram probability
print 'calculate bigram probability'
for word in bigram_filtered:
    bigram_probability[word] = float(bigram_count[word])/N

bigram_len = len(bigram_list)

# t score
print 't score'
w.write('t score')
w.write('\n')
for bigram in bigram_filtered:
    m = re.search('(\S+) (\S+)', bigram)
    mu = unigram_probability[m.group(1)] * unigram_probability[m.group(2)]

    x_ = bigram_probability[bigram]
    t = (x_-mu)/(math.sqrt(x_/bigram_len))
    t_score[bigram] = t

for key, value in sorted(t_score.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    w.write("%r : %r" % (key, value))
    w.write('\n')
w.write('\n\n')

# chi-square
print 'chi-square'
w.write('chi-square')
w.write('\n')

for bigram in bigram_filtered:
    m = re.search('(\S+) (\S+)', bigram)
    first_part_of_bigram = m.group(1)
    second_part_of_bigram = m.group(2)

    o_11 = bigram_count[bigram]
    o_12 = unigram_count[second_part_of_bigram] - o_11
    o_21 = unigram_count[first_part_of_bigram] - o_11
    o_22 = N - (o_12 + o_21)

    chi_square[bigram] = N*float(((o_11*o_22 - o_12*o_21))**2)/((o_11+o_12)*(o_11+o_21)*(o_12+o_22)*(o_21+o_22))

for key, value in sorted(chi_square.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    w.write("%r : %r" % (key, value))
    w.write('\n')
w.write('\n\n')

# mutual information
print 'mutual information'
w.write('mutual information')
w.write('\n')
# for bigram in bigram_list:
for bigram in bigram_filtered:
    m = re.search('(\S+) (\S+)', bigram)
    first_part_of_bigram = m.group(1)
    second_part_of_bigram = m.group(2)
    mutual_information[bigram] = math.log(bigram_count[bigram]/(unigram_probability[first_part_of_bigram]*unigram_probability[second_part_of_bigram]), 2)

for key, value in sorted(mutual_information.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    w.write("%r : %r" % (key, value))
    w.write('\n')
