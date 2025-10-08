#В консоли
input_file = open('word.in', 'r')
output_file = open('word.out', 'w')


words =  input_file.readline().split()
# print(lst)
n = int(words[0])
k = int(words[1])

def format_essay(n, k, words):
    line = []
    char = 0


    for word in words:
        if char + len(word) + (1 if line else 0) <= k:
            line.append(word)
            char += len(word) + (1 if line else 0)
        else:
            # Word doesn't fit, so print the current line and start a new one
            print(" ".join(line))
            line = [word]
            char = len(word)


    with open("word.out", "w") as f:
            # Redirect standard output to the file
            import sys
            old_stdout = sys.stdout
            sys.stdout = f

    format_essay(n, k, input_file)



output_file.close()
input_file.close()