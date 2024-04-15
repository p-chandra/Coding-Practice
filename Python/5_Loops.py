def main():
    w_loop()
    f1_loop()
    f2_loop()
    print("talk\n" * 3, end="")
    both_loop()

def w_loop():
    i = 3
    while i != 0:
        print("Meow")
        i -= 1

def f1_loop():
    for i in [0, 1, 2]:
        print("Bark")

def f2_loop():
    for _ in range(3): #as opposed to for i in range(3): because we don't care what i equals and we don't use it later
        print("Moo")

def both_loop():
    while True:
        n = int(input("Enter value for N: "))
        if n > 0:
            break

    for _ in range(n):
        print("Quack")

main()