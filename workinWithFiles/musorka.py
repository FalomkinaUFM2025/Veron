#В консоли
input_file = open('word.in', 'r')
output_file = open('word.out', 'w')

words =  input_file.readline().split()
# print(lst)
n = 12
k = 14

line = ''
char = 0

for word in words:

   if char + len(words) <= n:
      line = line + word + ' '
      char = char + len(words)
   else:
      line = word + ' '
      char = len(words)
   output_file.write(line[:-1] + '\n')
output_file.close()
input_file.close()
