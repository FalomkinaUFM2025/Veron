#В консоли
input_file = open('word.in', 'r')
output_file = open('word.out', 'w')

words =  input_file.readline().split()
# print(lst)
n = int(words[0])
k = int(words[1])

line = ''
char = 0

for word in words:
#     with open('word.in', 'r', encoding='utf-8') as f:
#         file_content = f.read()  # Читаем все содержимое файла в одну строку
#
#         # Удаляем все пробелы из строки
#     content_without_spaces = file_content.replace(' ', '')
#
#     # Подсчитываем количество оставшихся символов
#     char = len(content_without_spaces)
#     if char <= 100:
#         output_file.write(input_file.read())
# print(f"Количество символов без пробелов: {char}")
# в переменную char записываем ею саму + len(word)
#проверяем чиcло символов в строке если
# оно меньше или равно к то мы берем переменную line и line + переменную word + пробел


output_file.close()
input_file.close()