i = 2
match i:
    case 1: print(1)
    case None: print("None")
    case True: print("True")
    case _: print("other")

match i:
    case 1 | 2: print("OK")
