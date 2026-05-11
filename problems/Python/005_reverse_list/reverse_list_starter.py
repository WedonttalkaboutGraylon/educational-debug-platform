def reverse_list(items):
    result = []
    for i in range(len(items) - 2, -1, -1):
        result.append(items[i])
    return result
