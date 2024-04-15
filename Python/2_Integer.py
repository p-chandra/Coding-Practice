def main():
    #code_1()
    #code_2()
    #returning functions
    #x = int(input("Int x = "))
    #print("x square =", square(x))
    code_3()

## Integer Values
def code_1():
    x = input("X = ") #or you can cast right away x = int(input("X = "))
    y = input("Y = ")
    z = int(x) + int(y) #without casting into int, python takes every input as string

    print("X + Y =", z) #if you casted at x and y, then you can print(x+y)
    

## Floating Point Values
def code_2():
    x = float(input("X = "))
    y = float(input("Y = "))
    z = round(x + y)
    #z = round(x / y, 2) #round to two decimal places

    print ("X + Y =", z)
    print(f"X + Y = {z}")
    print(f"X + Y = {z:.2f}") #format/rounds to two decimal places
    #print(f"X + Y = {z:,}") #formats with commas when values > 999

## Returning
def square(n):
    return pow(n,2)


## Comparing
def code_3():
    print("Compare if two values are less than, greater than, or equal to one another")
    x = int(input("var x = "))
    y = int(input("var y = "))

    if x < y:
        print(str(x) + " is less than " + str(y)) #have to cast it back to string to print like this
    elif x > y :
        print(x,"is greater than",y)
    else:
        print(str(x) + " and " + str(y) + " are equal")


main()
