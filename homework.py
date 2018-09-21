import re
import sys
import copy

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'corpus.txt'

if len(sys.argv) > 3:
    s1 = sys.argv[2]
    s2 = sys.argv[3]
else:
    s1 = 'Facebook announced plans to built a new datacenter in 2018 .'
    s2 = 'Facebook is an American social networking service company in California .'



infile = open(filename, 'r')
intext = infile.read().lower()
infile.close()


# for unigram
unigram = re.sub(r'[^\w\s]', ' ', intext)
unigram = re.sub(r'\s{2,}', ' ', unigram)
tokens = unigram.split()
num_tokens = len(tokens)


# for bigram
bigram = intext.replace('u.s.', 'u.s')
bigram = bigram.replace('i.e.', 'i.e')
bigram = re.sub(r'\s{2,}', ' ', bigram)
sentences = bigram.split('. ')

for i in range(len(sentences)):
    sentences[i] = sentences[i].split()
    if len(sentences[i]) == 0:
        sentences.remove(sentences[i])
num_sentences = len(sentences)





# populate the vocabulary
voca = {}
for word in tokens:
    if word in voca:
        voca[word] += 1
    else:
        voca[word] = 1

num_types = len(voca)




# generate the 2 scenarios

token1 = s1.lower().replace('.', '').split()
token2 = s2.lower().replace('.', '').split()
len1 = len(token1)
len2 = len(token2)


table1, table2 = {}, {}

for word_i in token1:
    table1[word_i] = {}
    for word_j in token1:
        table1[word_i][word_j] = 0

for word_i in token2:
    table2[word_i] = {}
    for word_j in token2:
        table2[word_i][word_j] = 0




# bigram count tables
bigram_count1 = copy.deepcopy(table1)
bigram_count2 = copy.deepcopy(table2)

for sentence in sentences:
    for i in range(len(sentence) - 1):
        temp = re.sub(r'[^\w]', '', sentence[i + 1])
        if (sentence[i] in token1) and (temp in token1):
            bigram_count1[sentence[i]][temp] += 1
        if (sentence[i] in token2) and (temp in token2):
            bigram_count2[sentence[i]][temp] += 1


# bigram probability tables
bigram_proba1 = copy.deepcopy(bigram_count1)
bigram_proba2 = copy.deepcopy(bigram_count2)

for key_i in bigram_proba1:
    for key_j in bigram_proba1[key_i]:
        bigram_proba1[key_i][key_j] /= voca[key_i]

for key_i in bigram_proba2:
    for key_j in bigram_proba2[key_i]:
        bigram_proba2[key_i][key_j] /= voca[key_i]


# bigram (add one) count tables
bigram_addone_count1 = copy.deepcopy(bigram_count1)
bigram_addone_count2 = copy.deepcopy(bigram_count2)

for key_i in bigram_addone_count1:
    for key_j in bigram_addone_count1[key_i]:
        bigram_addone_count1[key_i][key_j] += 1

for key_i in bigram_addone_count2:
    for key_j in bigram_addone_count2[key_i]:
        bigram_addone_count2[key_i][key_j] += 1


# bigram (add one) probability tables
bigram_addone_proba1 = copy.deepcopy(bigram_addone_count1)
bigram_addone_proba2 = copy.deepcopy(bigram_addone_count2)

for key_i in bigram_addone_proba1:
    for key_j in bigram_addone_proba1[key_i]:
        bigram_addone_proba1[key_i][key_j] /= (voca[key_i] + num_types)

for key_i in bigram_addone_proba2:
    for key_j in bigram_addone_proba2[key_i]:
        bigram_addone_proba2[key_i][key_j] /= (voca[key_i] + num_types)


# calculate probability for the two scenarios

def proba_begin_sentence(word):
    # this function returns the probability of the given word
    # as the beginning of sentences
    count = 0
    for sentence in sentences:
        if word == sentence[0]:
            count += 1
    return count/num_sentences


def proba(token, table):
    result = (1/num_sentences) * proba_begin_sentence(token[0])
    #result = proba_begin_sentence(token[0])
    for k in range(len(token) - 1):
        result *= table[token[k]][token[k+1]]
    return result



# define function to format the tables

def print_table(dd, delimiter=' '):
    # print the header
    print(' '*10, end=delimiter)
    for key in dd:
        print('{:<10}'.format(key), end=delimiter)
    print()
    # print the content
    for key_i in dd:
        print('{:<10}'.format(key_i), end=delimiter)
        for key_j in dd[key_i]:
            temp = dd[key_i][key_j]
            if isinstance(temp, int):
                print('{:<10}'.format(temp), end=delimiter)
            else:
                print('{:<10.6f}'.format(temp), end=delimiter)
        print()
    print()




def main():
    print('bigram count table for scenario 1')
    print_table(bigram_count1)

    print('bigram probability table for scenario 1')
    print_table(bigram_proba1)

    print('bigram count table with add one smoothing for scenario 1')
    print_table(bigram_addone_count1)

    print('bigram probability table with add one smoothing for scenario 1')
    print_table(bigram_addone_proba1)


    #######################################################
    print('bigram count table for scenario 2')
    print_table(bigram_count2)

    print('bigram probability table for scenario 2')
    print_table(bigram_proba2)

    print('bigram count table with add one smoothing for scenario 2')
    print_table(bigram_addone_count2)

    print('bigram probability table with add one smoothing for scenario 2')
    print_table(bigram_addone_proba2)

    #######################################################
    p1 = proba(token1, bigram_proba1)
    p2 = proba(token2, bigram_proba2)
    p1_addone = proba(token1, bigram_addone_proba1)
    p2_addone = proba(token2, bigram_addone_proba2)
    print('bigram probability for scenario 1: {0}'.format(p1))
    print('bigram probability for scenario 2: {0}'.format(p2))
    print('bigram probability with add one smoothing for scenario 1: {0}'.format(p1_addone))
    print('bigram probability with add one smoothing for scenario 2: {0}'.format(p2_addone))



if __name__ == '__main__':
    main()