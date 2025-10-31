correct=5
first_num=int(input("Guess the number:"))
if first_num==correct:
    print("Yes! You win")
elif first_num!= correct:
    sec_num=int(input("Try it again:"))

if sec_num==correct:
    print("You win chossing the second number")
elif sec_num!=correct:
    print("Oops! Lost the game")


