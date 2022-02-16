n = 5

#trying 12345-12345-12345-12345-12345

def repeated_entry(vector):
    set_ = set()
    for i in range(len(vector)):
        set_.add(vector[i])
    if len(set_) == len(vector):
        return 0
    #I want to return 1  
    else:
        return 1

def activation_check(serial_code):
    entries = serial_code.split("-")
    if len(entries) != n:
        return 2

    #11111-11111-11111-11111-11111 is ok to pass it

    matrix = [[0]*n for _ in range(n)]

    #print(matrix)

    # matrix = 00000-00000-00000-00000-00000
    # [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    for i in range(n):
        if len(entries[i]) != n:
            return 2
        #every section must contain 5 numbers

        for j in range(n):
            if entries[i][j] < '1' or entries[i][j] > str(n):
                return 2     

            matrix[i][j] = entries[i][j]

        #print(matrix)
        #at the end of this for matrix = entries = 11111-11111-11111-11111-11111      
    
    for i in range(n):
        vector = [matrix[i][j] for j in range(n)]
        #print(vector)
        #print(len(vector))
        if repeated_entry(vector):
            return 0

    #print(vector)
    #12345-12345-12345-12345-12345

    #12345-23451-34512-45123-51234

    #print to see if I passed the check 1
    print("passed 1")

    for j in range(n):
        vector = [matrix[i][j] for i in range(n)]
        if repeated_entry(vector):
            return 0

    #print to see if I passed the check 2
    print("passed 2")

    #12345-23451-34512-45123-51234

    vector = [matrix[i][i] for i in range(n)]
    if repeated_entry(vector):
        return 0

    #print to see if I passed the check 3
    print("passed 3")
    #12345-23451-34512-45123-51234

    # 12345
    # 23451
    # 34512
    # 45123
    # 51234

    # 12345
    # 23451
    # 34512
    # 45123
    # 51234

    #for debugging purposes:
    # for i in range(5):
    #     for j in range(5):
    #         print("indice", i, j, ":\n")
    #         print(matrix[i][j])

    vector = [matrix[i][n-1-i] for i in range(n)]
    print(vector)
    if repeated_entry(vector):
        return 0

    #print to see if I passed the check 4
    print("passed 4")

    sum__ =  0
    for i in range(n):
        for j in range(n):
            sum__ += int(matrix[i][j])
    
    if not (sum__ % 96 == 75):
        return 0

    return 1

if __name__ == '__main__':
    print("""██╗  ██╗██╗   ██╗██╗   ██╗██████╗  ██████╗ ███████╗
██║ ██╔╝██║   ██║██║   ██║██╔══██╗██╔═══██╗██╔════╝
█████╔╝ ██║   ██║██║   ██║██║  ██║██║   ██║███████╗
██╔═██╗ ██║   ██║██║   ██║██║  ██║██║   ██║╚════██║
██║  ██╗╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                                                   
    """)
    serial_code = input("Input your activation code: ")

    result = activation_check(serial_code)
    print()
    if result > 1:
        print("Your serial has an incorrect format, look at the back of your CD.\n")
    elif result:
        with open("flag", "r") as f:
            flag = f.read()
            print(flag)
    else:
        print("Stop trying, buy the license :)\n")