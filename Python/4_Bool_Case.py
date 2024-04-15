def main():
    print("Check if value is Even")
    x = int(input("Enter a integer: "))
    if is_even(x):
        print("True")
    else:
        print("False")
    name = input("What's your name? ")
    house(name)

## Comparing
def is_even(num):
    #if num % 2 == 0:
    #    return True

    #or we can write  return True if num % 2 == 0 else False
    # or
    return num % 2 == 0 #we don't really need the else 



def house(name):
    match name:
        case "Harry" | "Hermione" | "Ron":
            print("Gryffindor")
        case "Draco":
            print("Slytherin")
        case _: # this is like default in other languages
            print("Who?")

main()
