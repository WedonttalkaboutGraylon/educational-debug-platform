def all_positive(numbers):
    for num in numbers:
        if num >= 0:
            continue
        else:
            return False
    return True
