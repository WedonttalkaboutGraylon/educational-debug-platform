def find_maximum(numbers):
    maximum = numbers[0]
    for i in range(1, len(numbers) - 1):
        if numbers[i] > maximum:
            maximum = numbers[i]
    return maximum
