
def Admin():
      print("ENTER NAME: ",end='')
      aname=input()
      pin=0000
      while pin!=1111:
        pin=int(input("Enter 4 digit Pin:"))
        if pin==1111:
            print ("Logged in as Admin")
            print("select a option--\n1.Book enquiry\n2.book entry\n3.customer verification")
            c=int(input("Enter option  number--"))
        else:
            print("Incorrect Pin.Try again")


