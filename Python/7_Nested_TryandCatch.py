def main():
    try:
        h = int(input("Enter height: "))
        w = int(input("Enter width: "))
    except ValueError:
        print("x is not an integer")
    else: #do this if try works
        loops(h, w) 


def loops(h, w):
    for i in range(h):
        for j in range(w):
            print("#", end="")
        print(" ")

def get_int():
    while True: # keep prompting for int until you receive it
        try:
            return int(input("What's x? ")) #return int when truly int
        except ValueError:
            print("x is not an integer") #gives user what the warning is


def get_int():
    while True: # keep prompting for int until you receive it
        try:
            return int(input("What's x? ")) #return int when truly int
        except ValueError:
            pass #gives user no warnings and just prompts to enter a value again

main()