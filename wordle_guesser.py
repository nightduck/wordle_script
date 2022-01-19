import numpy as np
import math
import random

EXTENDED = True
HARD_MODE = False

guessing_list = []
answer_list = set()

class DecisionTreeNode:
    def __init__(word, bins):
        self.word = word
        self.masks = bins


if EXTENDED:
    with open("wordle_occurrence_list.txt", 'r') as fin:
        for line in fin:
            w, o = line.split(' ')
            guessing_list.append(w)
            answer_list.add((w, int(o)))
else:
    with open("wordle_dictionary.txt", 'r') as fin:
        for line in fin:
            guessing_list.append(line[:5])

    size = len(guessing_list)
    answer_list = set([(w, 1) for w in guessing_list])


def get_mask(guess, answer):
    # Mask defaults to all wrong and convert strings to lists
    guess = list(guess)
    answer = list(answer)
    mask = [0,0,0,0,0]

    # If exact match
    for i in range(5):
        if guess[i] == answer[i]:
            mask[i] = 2
            guess[i] = 'X'     # Make sure it doesn't get double counted in next step
            answer[i] = 'Y'

    # Find anything in wrong spot
    for i,l in enumerate(guess):
        try:
            j = answer.index(l)
            mask[i] = 1
            answer[j] = 'Y'
        except ValueError as err:
            pass
    
    # Convert to base3 number (big-endian)
    return sum([(3**i)*v for i,v in enumerate(mask)])
    #return "".join([str(x) for x in mask])

def compute_entropy(int_list):
    total = sum(int_list)
    entropy = 0.0

    for i in int_list:
        p = i / total
        entropy -= math.log(p) * p

    return entropy

def make_guess(guessing_list, answer_list):
    # Restructure guessing list as dictionary, with words mapping to sub-dictionaries, explained later
    max_entropy = -1
    best_guess = "idk"
    best_bins = {}
    remaining_entropy = compute_entropy([p for a, p in answer_list])

    if len(answer_list) == 1:
        a, o = answer_list[0]
        best_bins = {get_mask(a[0],a) : [a]}
        return a, best_bins

    for guess in guessing_list:
        bins = {}
        for a, p in answer_list:
            mask = get_mask(guess, a)
            if not mask in bins.keys():
                bins[mask] = [(a, p)]
            else:
                bins[mask].append((a, p))

        # Replace best guess if there's a word with better entropy.a
        # Or: if there's a word with less entropy, but enough to ascertain the answer on the next
        #    guess, and that's in the answer list, use that instead. Maybe we'll get lucky
        new_entropy = compute_entropy([sum([p for a, p in mask_list]) for mask_list in bins.values()])
        if new_entropy > max_entropy or (guess in [a for a, p in answer_list]
                and best_guess not in [a for a, p in answer_list]
                and new_entropy >= remaining_entropy):
            max_entropy = new_entropy
            best_guess = guess
            best_bins = bins

    return best_guess, best_bins

# Start guess of base list: raise, H = 4.074
# Start guess of exte list: soare, H = 4.079

# def guesses_to_get(answer, guessing_list, answer_list):
#     guesses = 0
#     while True:
#         if guesses == 0:
#             if EXTENDED:
#                 best_guess = 'soare'
#             else:
#                 best_guess = 'raise'
#         else:
#             best_guess, bins = make_guess(guessing_list, answer_list)

#         guesses += 1

#         if best_guess == answer:
#             return guesses
        
#         mask = get_mask(best_guess, answer)

#         answer_list = list(filter(lambda a : get_mask(best_guess, a) == mask, answer_list))
        
#         if HARD_MODE:
#             guessing_list = answer_list     # Only guess things that might actually be the answer now (hard mode)
            
#         if len(answer_list) == 0:
#             print("One of us messed up somewhere cause there's no more possible words")
#             return -1

def build_tree(guessing_list, answer_list):
    # Define tree here
    for a in answer_list:
        temp_list = answer_list
        # Lookup in tree, going as far down as we can go
        
        # If we haven't guessed the answer, start making calls to make_guess(guessing_list, temp_list)
        # and build out the tree using the resulting best_guess and the previous mask

if EXTENDED:
    first_guess = 'tares'
else:
    first_guess = 'raise'

# first_guess = random.choice(['stare', 'arise', 'trace', 'irate', 'crate', 'slate', 'raise'])
# first_guess = 'slept'

print('Try', first_guess)
mask = input("What was the result? (in 0,1,2s): ")
mask = sum([(3**i)*int(v) for i,v in enumerate(mask)])
answer_list = list(filter(lambda a : get_mask(first_guess, a[0]) == mask, answer_list))
print("Possible words:", len(answer_list))
if len(answer_list) < 20:
    print(answer_list)

if HARD_MODE:
    guessing_list = [a[0] for a in answer_list]

stop = False
while not stop:
    best_guess, bins = make_guess(guessing_list, answer_list)
    print('Try', best_guess)
    
    mask = input("What was the result? (in 0,1,2s): ")
    
    mask = sum([(3**i)*int(v) for i,v in enumerate(mask)])
    answer_list = bins[mask]
    print("Possible words:", len(answer_list))
    if len(answer_list) < 20:
        print(answer_list)
    
    if HARD_MODE:
        guessing_list = [a[0] for a in answer_list]     # Only guess things that might actually be the answer now (hard mode)
         
    if len(answer_list) == 0:
        print("One of us messed up somewhere cause there's no more possible words")
        stop = True
    elif len(answer_list) == 1:
        print("Answer is", answer_list[0])
        stop = True
