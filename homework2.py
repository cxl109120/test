
import re
import copy


infile = open('corpus.txt', 'r')
intext = infile.read().lower()
infile.close()

#wordform = re.sub(r'[:;\-,.@"()]', '', intext)
wordform = re.sub(r'[^\w\s]', ' ', intext)
tokens = wordform.split()
num_tokens = len(tokens)



# populate the vocabulary
voca = {}
for word in tokens:
    if word in voca:
        voca[word] += 1
    else:
        voca[word] = 1

num_types = len(voca)


# generate the 2 scenarios
s1 = 'Facebook announced plans to built a new datacenter in 2018'
s2 = 'Facebook is an American social networking service company in California'

token1 = s1.lower().split()
token2 = s2.lower().split()
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

for i in range(len(tokens) - 1):
    if (tokens[i] in token1) and (tokens[i + 1] in token1):
        bigram_count1[tokens[i]][tokens[i + 1]] += 1
    if (tokens[i] in token2) and (tokens[i + 1] in token2):
        bigram_count2[tokens[i]][tokens[i + 1]] += 1

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

def proba(token, table, addone = False):
    result = 1
    for k in range(len(token) - 1):
        if k == 0:
            if addone:
                result *= (voca[token[k]] + 1) / (num_tokens + num_types)
            else:
                result *= voca[token[k]]/num_tokens
        else:
            result *= table[token[k]][token[k+1]]
    return result





def print_table(dd, delimiter = ' '):
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
    p1_addone = proba(token1, bigram_addone_proba1, True)
    p2_addone = proba(token2, bigram_addone_proba2, True)
    print('bigram probability for scenario 1: {0}'.format(p1))
    print('bigram probability for scenario 2: {0}'.format(p2))
    print('bigram probability with add one smoothing for scenario 1: {0}'.format(p1_addone))
    print('bigram probability with add one smoothing for scenario 2: {0}'.format(p2_addone))



if __name__ == '__main__':
    main()