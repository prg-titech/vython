
for i in range(10):
    print(i)
    if i == 5:
        break
else:
    "have not been breaked"

print("--------------------")

for i in range(10):
    if i < 6:
        continue
    print(i)
else:
    "have not been breaked"
