## Printing
# Code 1
def hello_1(to="World"):
    print("Hello, " + to) # this is good to use when adding multiple strings before and after

# Code 2
def hello_2(to):
    print("Hello,", to) # when using comma, it auto creates space in string after Hello, but not good for concat strings

# Code 3
def hello_3(to):
    print("Hello, ")
    print("Hello, ", end="") #eliminates newline because default this is end="\n"
    print(to)

# Code 4
def hello_4(name):
    name = name.strip() #removes whitespace before and after the user input
    name = name.capitalize() #capializes first letter 
    name = name.title() #capitalize first letter on each word
    print(f"Hello, {name}") # we need the 'f' or format string in print for the {} to be subbed in

# Code 5
def hello_5(name):
    name = name.strip().title()
    ## OR you can do this at the input level example line 27
    ## name = input("What is your name? ").strip().titile()
    print(f"Hello, {name}")






# Like C, Python must know about the function before calling it. thats why it must be on top. We will address this at task 2

hello_1() #calling a function without parameters you can specify what it defaults too. In my case the default
            #is "World". Look at line #3

name = input("What is your name? ")
hello_1(name) #function parameter names can be anything. I used "to"
hello_2(name)
hello_3(name) #Here for example sake I used "name"
hello_4(name)