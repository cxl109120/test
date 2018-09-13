
import sys
import re

#for i in range(len(sys.argv)):
#    print(i, sys.argv[i])
if len(sys.argv) > 1:
    infile_name = sys.argv[1]
else:
    infile_name = 'CSfaculty.txt'

if len(sys.argv) > 2:
    outfile_name = sys.argv[2]
else:
    outfile_name = 'output.txt'


# read in text
infile = open(infile_name, 'r')
intext = infile.read()
infile.close()

p_person = re.compile('\<td\>\s*.*\s*.*\s*</td\>\s*\<td\>\s*.*\s*.*')

p_name = re.compile('[a-zA-Z. -]+, [a-zA-Z. -]+')
p_title = re.compile('\<br /\>\s[a-zA-Z. ]+')
p_email = re.compile('[0-9a-zA-Z.]+\@\w+.\w+')
p_phone = re.compile('-\d{4}')


# write out result
outfile = open(outfile_name, 'w')
index = 0
for person in re.findall(p_person, intext):
    name = re.findall(p_name, person)
    title = re.findall(p_title, person)
    email = re.findall(p_email, person)
    phone = re.findall(p_phone, person)
    if len(name)>0 and len(email)>0:
        index += 1

        outfile.write('{:<4}'.format(index))
        #outfile.write(f'{name[0]:25}')
        #outfile.write(f'{title[0][7:]:50}')
        #outfile.write(f'{email[0]:40}')
        outfile.write('{:25}'.format(name[0]))
        outfile.write('{:50}'.format(title[0]))
        outfile.write('{:40}'.format(email[0]))
        if len(phone)>0:
            outfile.write(phone[0][1:])
        outfile.write('\n')
outfile.close()