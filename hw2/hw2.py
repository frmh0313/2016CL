#-*- coding: utf-8 -*-
import re

f = open('BROWN_A1.txt', 'rU')

data = f.read()
# data: one string.
# paragraphs: paragraph단위로 분할된 것들의 리스트
# paragraph: paragraphs 리스트 안에 들어있는 각각의 paragraph string
# words: paragraph string안의 한 단어 단어들을 분할한 리스트
# word: words 리스트 안에 있는 각각의 단어

paragraphs = []
paragraphs = data.split('\n')

words = []

f.close()
w = open('out.txt', 'w')

for paragraph in paragraphs:
    words = paragraph.split()
    for word in words:
        prepunctuation = re.match(r'[\W_]+', word)
        postpunctuation = re.search(r'[\W_]+$', word)

# 공백으로 구분된 단어 앞뒤에 붙어있는 특수문자 저장 후 단어에서 삭제. 
        if prepunctuation:
            word = re.sub(r'^[\W]+', '', word)
        if postpunctuation:
            word = re.sub(r'[\W]+$', '', word)

        quword = re.match(r'[qQ][uU][^\W\daeiouAEIOU_]*', word) # qu로 시작되는 경우
        consonants = re.match(r'[^\W\daeiouAEIOU_]+', word) # 자음으로 시작되는 경우 
        qu_and_consonants = re.match(r'[^\W\daeiouAEIOU_]+[qQ][uU][^\W\daeiouAEIOU_]*', word) # 자음+qu(+자음)인 경우 

        if qu_and_consonants:
            word = re.sub(r'^[^\W\daeiouAEIOU_]+[qQ][uU][^\W\daeiouAEIOU_]*', '', word)
            word = word+qu_and_consonants.group()+'ay'
        elif quword:
            word = re.sub(r'^[qQ][uU][^\W\daeiouAEIOU_]*', '', word)
            word = word+quword.group()+'ay'
        elif consonants:
            word = re.sub(r'^[^\W\daeiouAEIOU_]+', '', word)
            word = word+consonants.group()+'ay'
        else:
            word = word+'ay'

# 단어 앞뒤에 특수문자가 있을 경우 붙여줌. 
        if prepunctuation:
            word = prepunctuation.group()+word
        if postpunctuation:
            word = word+postpunctuation.group()
        w.write(word+' ')
    w.write("\n")
