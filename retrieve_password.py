from ssss import *

if __name__ == "__main__" :

    while(True):
        print("-------------------------------Retrieve Password-------------------------------")
        username = str(input("Username : "))
        total_fragments = int(input("Total shares you have : "))

        fragments = []
        secret_found = False

        for i in range(total_fragments):
            
            x = int(input(f"X{i+1} : "))
            y = int(input(f"Y{i+1} : "))
            print()
            
            fragment = [x, y]
            fragments.append(fragment)

        status = find_secret(username, fragments)

        break