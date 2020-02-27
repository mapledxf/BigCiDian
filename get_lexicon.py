import pypinyin as ppy
import jieba

freq = 'freq.txt'

in_file = open('trans.txt', 'r')
split_file = open('split.txt', 'w')
out_file = open('lexicon.txt', 'w')
freq_file = open('freq.txt', 'r')

split_result = []
out_result = []

for f in freq_file:
    jieba.suggest_freq(f,tune=True)

for line in in_file:
    key,trans = line.strip().split(' ',1)
    words = jieba.cut(trans.replace(" ",""), HMM=False)
    split_result.append(" ".join(words) + "\n")

    for word in words:
        if word not in out_result:
            out_result.append(word + "\n")

split_result.sort()
split_file.writelines(split_result)
split_file.flush()
split_file.close()

out_result.sort()
out_file.writelines(out_result)
out_file.flush()
out_file.close()
