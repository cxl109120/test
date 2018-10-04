
import sys

# the transition probability
a = {('H', 'H'): 0.7,
     ('H', 'F'): 0.3,
     ('F', 'H'): 0.5,
     ('F', 'F'): 0.5}


# the state observation likelihood
b = {('H', 'N'): 0.1,
     ('H', 'C'): 0.4,
     ('H', 'D'): 0.5,
     ('F', 'N'): 0.6,
     ('F', 'C'): 0.3,
     ('F', 'D'): 0.1}


def viterbi(observations):
    t = len(observations)
    v = [{}]
    back_pointer = [{}]
    v[0]['H'] = 0.6 * b[('H', observations[0])]
    v[0]['F'] = 0.4 * b[('F', observations[0])]
    back_pointer[0]['H'] = ''
    back_pointer[0]['F'] = ''
    for i in range(1, t):
        v.append({})
        back_pointer.append({})
        v_H_H = v[i-1]['H'] * a[('H', 'H')] * b[('H', observations[i])]
        v_F_H = v[i-1]['F'] * a[('F', 'H')] * b[('H', observations[i])]
        if v_H_H > v_F_H:
            v[i]['H'] = v_H_H
            back_pointer[i]['H'] = 'H'
        else:
            v[i]['H'] = v_F_H
            back_pointer[i]['H'] = 'F'

        v_H_F = v[i-1]['H'] * a[('H', 'F')] * b[('F', observations[i])]
        v_F_F = v[i-1]['F'] * a[('F', 'F')] * b[('F', observations[i])]
        if v_H_F > v_F_F:
            v[i]['F'] = v_H_F
            back_pointer[i]['F'] = 'H'
        else:
            v[i]['F'] = v_F_F
            back_pointer[i]['F'] = 'F'

    if v[t-1]['H'] > v[t-1]['F']:
        trace = 'H'
    else:
        trace = 'F'
    for i in range(-1, -t, -1):
        trace = back_pointer[i][trace[0]] + trace
    return trace, v


def main():
    if len(sys.argv) > 1:
        obser = sys.argv[1]
    else:
        obser = input('Please type in the observation input (D-dizzy, N-normal, C-cold): ')
    obser = obser.strip()

    trace, v = viterbi(obser)
    print(trace)
    #for p in v:
        #print(p)



if __name__ == '__main__':
    main()


