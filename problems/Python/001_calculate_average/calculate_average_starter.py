def calculate_average(numbers):
    total = 0
    count = len(numbers)
    for num in numbers:
        total += num
    average = total / count
    return total
