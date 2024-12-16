def sort(list):
    if list.length() < 1:
        return []
    elif list.length() == 1:
        return list
    pivot = list[0]
    lower_list = []
    upper_list = []
    middle_list = []
    
    for item in list:
        if item < pivot:
            lower_list.append(item)
        elif item > pivot:
            upper_list.append(item)
        else:
            middle_list.append(item)
    sorted_lower_list = sort(lower_list)
    sorted_upper_list = sort(upper_list)

    return sorted_lower_list + middle_list + sorted_upper_list

a = [4, 3, 1, 2]
result = sort(a)

print(result)
