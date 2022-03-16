# I know this isn't very fast/efficient, but it only needed to be run once so
# oh well

# Opens files
with open('wiki-100k.txt') as file:
    df = file.read()
    english = df.split('\n')

with open('words.txt') as file:
    df = file.read()
    colemak = df.split('\n')

removed = 1
# print(len(colemak))
for i in range(len(english)):
    for j in range(len(colemak) - removed):
        if english[i] == colemak[j]:
            colemak.pop(j)

            # Adds 1 to the amount that has been removed, so it doesn't look
            # for elements outside the new length of the array
            removed += 1

# Turns the list into an array, with the elements seperated by a newline
colemak_str = '\n'.join(colemak)
# print(colemak_str)
print("hello")

# Writes new string to the file
with open('words.txt', "w") as file:
    file.write(colemak_str)

print("DONE!")