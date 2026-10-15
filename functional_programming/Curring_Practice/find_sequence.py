
from collections.abc import Callable
from functools import reduce


"""
# This is the version without the reduce import
def lines_with_sequence(char: str) -> Callable[[int], Callable[[str], int]]:
    def with_char(length: int) -> Callable[[str], int]:
        def with_length(doc: str) -> int:
            sequence = char * length
            lines = doc.split("\n")            
            result = 0
            for item in lines:
                if sequence in item:
                    result +=1 
            return result
        return with_length
    return with_char
"""
# this will be the version with the reduce import
def lines_with_sequence(char: str) -> Callable[[int], Callable[[str], int]]:
    def with_char(length: int) -> Callable[[str], int]:
        def with_length(doc: str) -> int:
            sequence = char * length
            lines = doc.split("\n")            
            return reduce(lambda inc, line: inc + 1 if sequence in line else inc , lines, 0)
        return with_length
    return with_char


doc = """###
@##
$$$
###"""
start = lines_with_sequence("#")
with_char = start(3)
final = with_char(doc)
print(final)



