#В консоли
input_file = open('word.in', 'r')
output_file = open('word.out', 'w')

lst =  input_file.readline().split()
# print(lst)
n = int(lst[0])
a = int(lst[1])
words = input_file.readline().split()


w = ['d','e','n','i','s']
w[0] = 'p'
print(w[0])


output_file.close()
input_file.close()