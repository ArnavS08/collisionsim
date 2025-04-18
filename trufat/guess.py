ATTEMPTS = 3

import random


def make_rand():
    answer = random.randint(1, 100)
    return answer

def make_guess():
    while True:
        guess = input("Guess a number in between 1 and 100: ")
        guess = int(guess)
        return guess
didYouWin = False
answer = make_rand()
for i in range(ATTEMPTS):
    guess = make_guess()
    if guess == answer:
        print(f"You win. The Correct Number Was {answer}.")
        didYouWin = True
        break
    elif guess > answer:
        print(f"Too high, To Further Elaborate, Or, In A More Colloquial Manner, You're Off By {guess - answer} Units, My Friend")
    else:
        print(f"Too low, To Further Elaborate, Or, In A More Colloquial Manner, You're Off By {answer - guess} Units, My Friend")
if didYouWin == False:
    print(f"You did NOT win LOL!!! The Number Was {answer}")






