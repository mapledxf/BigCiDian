#!/usr/bin/env python

# This script processes DaCiDian
# FROM:
# 	layer-1 mapping: DaCiDian/word_to_pinyin.txt
# 	layer-2 mapping: DaCiDian/pinyin_to_phone.txt
# TO: 
# 	lexicon.txt

import sys

syllable_to_phones={}

word_to_syllable_file  = sys.argv[1]  # layer-1 mapping
words_to_add = sys.argv[2]
words_to_remove = sys.argv[3]
syllable_to_phone_file = sys.argv[4]  # layer-2 mapping

for l in open(syllable_to_phone_file):  # "ZHENG	zh eng"
    cols = l.strip().split('\t')
    assert(len(cols) == 2)
    syllable = cols[0]
    phones   = cols[1].split()
    syllable_to_phones[syllable] = phones

with open(word_to_syllable_file) as f:
    words = f.readlines()
    words = [x.strip() for x in words]

if words_to_add:
    with open(words_to_add) as f:
        add_words = f.readlines()
        add_words = [x.strip() for x in add_words]
        words = words + add_words

if words_to_remove:
    with open(words_to_remove) as f:
        remove_words = f.readlines()
        remove_words = [x.strip() for x in remove_words]

for l in words: # "15	YI_1 WU_3;YAO_1 WU_3"
    cols = l.strip().split('\t')
    if len(cols) != 2:
        print(l)
        sys.exit(-1)
    word  = cols[0]
    if word in remove_words:
        continue
    prons = cols[1].split(';')
    for pron in prons:
        phone_seq = []
        for syllable in pron.split():
            base,tone = syllable.split('_')
            phones = [phn for phn in syllable_to_phones[base]]
            phones[-1] = phones[-1]+'_'+tone
            phone_seq.extend(phones)
        sys.stdout.write(word + '\t' + ' '.join(phone_seq) + '\n')
