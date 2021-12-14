from ssss import *

if __name__ == "__main__" :
    while (True):
        print("-------------------------------Request Password Recovery-------------------------------")
        username = str(input("Username : "))
        w = int(input("Number of Shares (w) : "))
        t = int(input("Minimum Shares to Recover password (t / Threshold) : "))

        if(t > w):
            print("Number of Shares must be larger than minimum threshold")
            continue

        # Initialize Secret
        status = initialize_secret(username, t, w)

        if (status):
            print(f"Password-Recovery for {username} has been Requested!")
            break

        else :
            print(f"Failed to Request Password-Recovery for {username}")
            break

        print()