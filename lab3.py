import string

def is_palindrome(text: str) -> bool:
    result = False
    text=text.lower().replace(" ","")
    length = len(text)
    left = ""
    right = ""

    if(length%2 == 1):
        left = text[:length//2]
        right = text[length//2 + 1:]
    else:
        left = text[:length//2]
        right = text[length//2:]

    right = right[::-1]
    
    if(left == right):
        result = True

    return result 

def fibonacci(n: int) -> int:
    if(n<0):
        raise ValueError("Nieprawidłowa wartość")
    
    first = 0
    second = 1

    for i in range(n):
        first, second = second, second+first

    return first

def count_vowels(text: str) -> int:
    vowels = ("a","e","i","o","u","y","ą","ę","ó")
    text=text.lower()
    counter=0

    for letter in text:
        if letter in vowels:
            counter+=1

    return counter

def calculate_discount(price: float, discount: float) -> float:
    if not (0<=discount<=1):
        raise ValueError("Zniżka musi być w przedziale <0,1>")

    return (price - (price*discount))

def flatten_list(nested_list: list) -> list:
    result = []

    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)

    return result


def word_frequencies(text: str) -> dict:
    text = text.lower()
    words = text.split()
    dictionary = {}

    for word in words:
        word = word.strip(string.punctuation)
        if word == "":
            continue
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    return dictionary


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1

    return True


def main():
    pass

if __name__ == "__main__":
    main()
