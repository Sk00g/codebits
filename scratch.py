source = "This is a\nMultiline statement"

lines = source.split('\n')
words = []
for line in lines:
    words.extend(line.split(' '))

print(source)
print(lines)
print(words)