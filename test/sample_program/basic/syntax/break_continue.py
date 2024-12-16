for i in [0,1,2,3,4,5,6,7,8,9]:
    print(i)
    if i == 5:
        break
else:
    print("have not been breaked")

for i in [0,1,2,3,4,5,6,7,8,9]:
    if i < 6:
        continue
    print(i)
else:
    print("have not been breaked")
