def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    reversed_text = cleaned[::-1]
    return reversed_text == reversed_text
