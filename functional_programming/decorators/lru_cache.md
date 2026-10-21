# LRU Cache

[`lru_cache` from the `functools` module](https://docs.python.org/3/library/functools.html#functools.lru_cache) is both a decorator and an example of memoization.

LRU stands for "[least recently used](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_(LRU))." It's a type of cache that stores items up to a certain size limit. When it gets full, it makes space for new items by discarding the least recently used items first. The cache can be effective because items that are used a lot – like frequently repeated calls to the same function – are less likely to be discarded. They stay in-cache.

The `lru_cache` decorator memoizes the inputs and outputs of the decorated function. It speeds up repeated calls to a slow function with the same inputs. A function that reads from disk, makes network requests, or requires a lot of computation could be a good candidate for LRU caching if it also sees many identical calls.

Here's an example from the Python docs that perfectly illustrates how and why to use `lru_cache`:

```Python
from functools import lru_cache


@lru_cache()
def factorial_r(x: int) -> int:
    if x == 0:
        return 1
    else:
        return x * factorial_r(x - 1)


factorial_r(10)  # no cached results; makes 11 recursive calls
# 3628800
factorial_r(5)  # just looks up cached result value
# 120
factorial_r(12)  # makes 2 new recursive calls; the other 11 are cached
# 479001600
```

Because the `factorial` function is recursive and the inputs are sequential numbers, it does get called repeatedly with the same inputs. Without caching, the function would be called 30 times in the code above. With `lru_cache`, the function is only called 13 times. You don't often need to compute factorials, but this example ties together how to use a decorator and memoization and recursion.

## Assignment

The creator of Doc2Doc is a huge fan of [palindromes](https://en.wikipedia.org/wiki/Palindrome) for some nerdy reason. Add a feature to check if a word is a palindrome.

- [ ] Import the `lru_cache` function from the `functools` module and use it to decorate the incomplete `is_palindrome` function.
- [ ] Complete the `is_palindrome` function. It takes as input a `word` string and returns `True` if the word is a palindrome (such as "racecar"), or `False` otherwise.

Try to use recursion. Check the outer characters first, then move inwards until you reach the base case or find that the word is not a palindrome.
