from functools import lru_cache

# This was my first solution
@lru_cache()
def is_palindrome(word: str) -> bool:
    if len(word) >= 1:
        if word[0] != word[-1]:
            return False
        return is_palindrome(word[1 : -1])
    return True


# This solution might be better
@lru_cache()
def is_palindrome_2(word: str) -> bool:
    if len(word) < 2:
        return True
    if word[0] != word[-1]:
        return False
    return is_palindrome(word[1 : -1])


# This is best but without recursion
@lru_cache()
def is_palindrome_3(word: str) -> bool:
    return word == word[::-1] 


pal = "bob"
no_pal = "rob"

print(is_palindrome(pal))
# True
print(is_palindrome_2(pal))
# True
print(is_palindrome_3(pal))
# 
print(is_palindrome(no_pal))
# False
print(is_palindrome_2(no_pal))
# False
print(is_palindrome_3(no_pal))
# False