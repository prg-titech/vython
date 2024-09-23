
for i in range(10):
    print(i)
    if i == 5:
        break
else:
    print("have not been breaked")

for i in range(10):
    if i < 6:
        continue
    print(i)
else:
    print("have not been breaked")
