def main():
    #Code_1() #List
    #Code_2() #Dictionary
    Code_3() #List of Dictionaries


def Code_1():
    students = ["Hermione", "Harry", "Ron"]
    
    for s in students: #I can use underscore here but its not pythonic. because im using the variable
        #outside of the loop to print its better to name or use a letter 
        print(s)

    for i in range(len(students)):
        print(i + 1, students[i])


def Code_2():
        # students = ["Hermione", "Harry", "Ron", "Draco"] #list 1
        # houses = ["Gryffindor", "Gryffindor", "Gryffindor", "Slytherin"] #list 2
        #OR
        #KEYS : Values
        students = {
             "Hermione": "Gryffindor",
             "Harry":"Gryffindor",
             "Ron":"Gryffindor",
             "Draco":"Slytherin",
             }
        #print(students) prints dictionary
        for s in students:
             #print(s) # this prints our keys
             print(s, students[s], sep=", ")

def Code_3():
        #{} is one dictionary so there are 4 dictionaries here
    students = [
        {"name":"Hermione", "house": "Gryffindor", "patronus": "Otter"}, 
        {"name":"Harry", "house": "Gryffindor", "patronus": "Stag"},
        {"name":"Ron", "house": "Gryffindor", "patronus": "Jack Russell Terrier"},
        {"name":"Draco", "house":"Slytherin", "patronus": None} #None means this has no value
        ]
    
    #these dictionaires has 3 keys and 3 values 
    for s in students:
         print(s["name"], s["house"], sep=", ")

main()

#LIST = a set of multiple values 1D
#Dictionary or DICT = Words and Definitions OR Keys and Values like a hash map 2D