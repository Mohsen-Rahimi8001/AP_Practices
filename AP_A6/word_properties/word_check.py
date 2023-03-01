import os
import concurrent.futures
from multiprocessing import Barrier


def is_palindrome(word:str, work_complete:"_BarrierType"=None):
    """Check for palindrome."""
    if word == word[::-1]:
        if work_complete is not None:
            work_complete.wait()
        return True
    else:
        if work_complete is not None:
            work_complete.wait()
        return False

def is_two_word_palindrome(word:str, work_complete:"_BarrierType"=None):
    """Check if the word is palindrome and the left part and the right part are meaningful."""
    if is_palindrome(word) and len(word) % 2 == 0 and is_meaningful(word[:len(word)//2]):
        if work_complete is not None:
            work_complete.wait()
        return True
    else:
        if work_complete is not None:
            work_complete.wait()
        return False

def is_meaningful(word:str, work_complete:"_BarrierType"=None):
    """Check for meaningfulness of the word and it's reverse. output --> [word(T, F), reverse_word(T, F)]"""
    res = [False, False]
    with open(os.path.dirname(__file__) + '\\words.txt', 'r') as f:
        for line in f.readlines():
            if word == line.strip():
                res[0] = True
            if word[::-1] == line.strip():
                res[1] = True
            if res[0] and res[1]:
                if work_complete is not None:
                    work_complete.wait()
                return res

    if work_complete is not None:
        work_complete.wait()
    
    return res

def check_word(word:str):
    
    work_complete = Barrier(4)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        fut_pal = executor.submit(is_palindrome, word, work_complete)
        fut_two_pal = executor.submit(is_two_word_palindrome, word, work_complete)
        fut_meaning = executor.submit(is_meaningful, word, work_complete)

        work_complete.wait()

        print(f"Result for the word {word}: \n---------------------------------")

        if fut_pal.result():
            print(f"the word <{word}> is palindrome.")
        else:
            print(f"the word <{word}> is not palindrome.")
        
        if fut_two_pal.result():
            print(f"the word <{word}> is two word palindrome.")
        else:
            print(f"the word <{word}> is not two word palindrome.")
        
        if fut_meaning.result()[0]:
            print(f"the word <{word}> is meaningful.")
        else:
            print(f"the word <{word}> is not meaningful.")
        
        if fut_meaning.result()[1]:
            print(f"the reverse of the word <{word}> is meaningful.")
        else:
            print(f"the reverse of the word <{word}> is not meaningful.")

        print('process done.\n')
