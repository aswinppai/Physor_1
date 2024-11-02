"""Program to manage inventory using mysql-python connectivity"""
import mysql.connector
x=input("enter database password")
con=mysql.connector.connect(host='localhost',
                            user='root',
                            password=x)
cur=con.cursor()
cur.execute("show databases;")
d=cur.fetchall()

if ("storemanager",) in d:
    cur.execute("use storemanager;")
    cur.execute("show tables;")
    d=cur.fetchall()
    if ("supplier",) not in d:
        cur.execute("create table supplier(supid char(4) PRIMARY KEY,supname varchar(20),phone char(10),supaddress varchar(30));")
    if ("stock",) not in d:
        cur.execute("create table stock(itemid char(3) PRIMARY KEY,supid char(4),itemname varchar(10),quantity integer,FOREIGN KEY(supid)REFERENCES supplier(supid) );")
else:
    cur.execute("create database storemanager;")
    cur.execute("use storemanager;")
    cur.execute("create table supplier(supid char(4) PRIMARY KEY,supname varchar(20),phone char(10),supaddress varchar(30));")
    cur.execute("create table stock(itemid char(3) PRIMARY KEY,supid char(4),itemname varchar(10),quantity integer,FOREIGN KEY(supid)REFERENCES supplier(supid) );")

    
def inputsup():#function to input records into supplier table
    n=int(input("enter no: of suppliers to be added:"))
    for i in range(n):
        a=input("enter 4 digit supplier id:")
        b=input("enter supplier name(maximum 20 characters):")
        c=input("enter supplier phone no:")
        d=input("enter supplier address(max 30 characters):")
        cur.execute("insert into supplier values('{}','{}','{}','{}')".format(a,b,c,d))
        cur.execute("commit;")
def inputstock():#function to input records into stock table
    n=int(input("enter no: of records:"))
    for i in range(n):
        a=input("enter 3 digit item id:")
        b=input("enter 4 digit supplier id:")
        while True:
            cur.execute("select * from supplier where supid='{}'".format(b))
            s=cur.fetchall()
            if s==[]:
                print("given supplier doesn't exist\nPlease enter a valid supplier id")
                print("if user want to add details of another supplier enter 'y' else enter 'n'")
                e=input("does user want to add details of another supplier?")
                if e=='y':
                    inputsup()
                else:
                    pass    
                b=input("enter 4 digit supplier id:")
            else:
                break
        c=input("enter itemname(max of 10 characters):")
        
        f=int(input("enter stock of the item"))
        cur.execute("insert into stock values('{}','{}','{}',{})".format(a,b,c,f))
        cur.execute("commit;")

def getdetsupsid(n):#should give take value of n where n is a supplier id
    cur.execute("select * from supplier where supid='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("supplier id does not match\nsupplier doesn't exist")
    else:
        t=s[0]
        print("supplier id:",t[0],"\nsupplier name:",t[1],"\nsupplier phone number:",t[2],"\nsupplier address:",t[3])
        
def getdetsupname():#gives details of supplier by taking supplier name as input
    n=input("enter supplier name:")
    cur.execute("select * from supplier where supname='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("supplier name does not match\nsupplier doesn't exist")
    else:
        t=s[0]
        print("supplier id:",t[0],"\nsupplier name:",t[1],"\nsupplier phone number:",t[2],"\nsupplier address:",t[3])
        
def getdetsupiid():#gives details of supplier by taking item id as input
    n=input("enter item id:")
    cur.execute("select supid from stock where itemid='{}'".format(n))
    d=cur.fetchall()
    if d==[]:
        print("item id doesn't exist\nitem doesn't exist")
    else:
        s=d[0][0]
        getdetsupsid(s)
def getdetsup():#fnction to get supplier details
    #this function is a combination of the previous 3 functions
    print("To get details of the supplier by entering supplier id enter 1")
    print("To get details of the supplier by entering supplier name enter 2")
    print("To get details of the supplier by entering item id of an item supplied by the supplier enter 3")
    n=int(input("enter choice:"))
    if n==1:
        s=input("enter supplier id:")
        getdetsupsid(s)
    elif n==2:
        getdetsupname()
    elif n==3:
        getdetsupiid()
    else:
        print("please enter a valid choice")

        
def delsupdet():#function to delete supplier details
    n=input("enter supplier id:")
    cur.execute("select * from supplier where supid='{}'".format(n))
    s=cur.fetchall()
    if s!=[]:
        cur.execute("delete from stock where supid='{}'".format(n))
        cur.execute("delete from supplier where supid='{}'".format(n))
        cur.execute("commit;")
    else:
        print("given supplier id doesnt exist")
def changedetsup():#function to change details of a supplier
    while True:
        print("To change supplier name enter 1")
        print("To change supplier phone number enter 2")
        print("To change supplier address enter 3")
        print("To exit loop enter 4") 
        n=int(input("enter choice:"))
        if n==1:
            b=input("enter supplier id")
            cur.execute("select * from supplier where supid='{}'".format(b))
            d=cur.fetchall()
            if d!=[]:
                while True:
                    a=input("enter new name(maxmum of 20 characters)")
                    if len(a)<=20:
                        cur.execute("update supplier set supname='{}' where supid='{}'".format(a,b))
                        cur.execute("commit;")
                        break
                    else:
                        print("name entered is too long")
        elif n==2:
            b=input("enter supplier id")
            cur.execute("select * from supplier where supid='{}'".format(b))
            d=cur.fetchall()
            if d!=[]:
                while True:
                    c=input("enter new phone number(must be 10 integers long)")
                    if len(c)==10:
                        cur.execute("update supplier set phone='{}' where supid='{}'".format(c,b))
                        cur.execute("commit;")
                        break
                    else:
                        print("phone number entered is not valid")
        elif n==3:
            b=input("enter supplier id")
            cur.execute("select * from supplier where supid='{}'".format(b))
            d=cur.fetchall()
            if d!=[]:
                while True:
                    c=input("enter new supplier address(maximum 30 characters)")
                    if len(c)<=30:
                        cur.execute("update supplier set supaddress='{}' where supid='{}'".format(c,b))
                        cur.execute("commit;")
                        break
                    else:
                        print("address entered exceeded character limit")
        else:
            break

def dissupite():#will display all the items supplied by a given supplier
    n=input("enter supplier id:")
    if len(n)==4:
        cur.execute("select * from stock where supid='{}'".format(n))
        d=cur.fetchall()
        if d==[]:
            print("Currently none of the items in the inventory are supplied by given supplier")
        else:
            for t in d:
                print("item id:",t[0],"\nitem name:",t[2],"\nstock:",t[3])
                print('')
                print('')
    else:
        print("Invalid supplier id")

def updatquan():#function to update quantity of an item
    n=input("enter item id:")
    if len(n)==3:
        cur.execute("select * from stock where itemid='{}'".format(n))
        d=cur.fetchall()
        if d==[]:
            print("given item id does not match any of the contents of this inventory")
        else:
            t=d[0]
            print("To account addition in quantity of an item enter character 'a'")
            print("To account reduction in quantity of an item enter character 'b'")
            a=input("enter choice:")
            if a=='a':
                b=int(input("enter number of item added to the inventory:"))
                cur.execute("update stock set quantity=quantity+{} where itemid='{}'".format(b,n))
                cur.execute("commit;")
            elif a=='b':
                b=int(input("enter number of item removed from the inventory:"))
                while True:
                    if b<=t[3]:
                        cur.execute("update stock set quantity=quantity-{} where itemid='{}'".format(b,n))
                        cur.execute("commit;")
                        break
                    else:
                        print("number of items entered is greater than the existing quantity of the given item in the inventory")
                        print("Please enter and amount lesser than the already existing quantity(",t[3],")")
                        b=int(input("enter number of item removed from the inventory:"))
    else:
        print("Invalid item id")

def changesup():#function to change supplier
    n=input("enter item id:")
    if len(n)==3:
        cur.execute("select * from stock where itemid='{}'".format(n))
        d=cur.fetchall()
        if d==[]:
            print("given item id does not match any of the contents of this inventory")
        else:
            s=input("enter new supplier id:")
            cur.execute("select * from supplier where supid='{}'".format(s))
            l=cur.fetchall()
            if l==[]:
                print("given supplier id doesn't exist")
                print("please enter a supplier id that exists")
            else:
                cur.execute("update stock set supid='{}' where itemid='{}'".format(s,n))
                cur.execute("commit;")
    else:
        print("Invalid item id")
        
def dispdetitid():#function to get details of the item by entering item id
    n=input("enter item id:")
    cur.execute("select * from stock where itemid='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("item id does not match\nitem doesn't exist")
    else:
        t=s[0]
        print("item id:",n,"\nsupplier id:",t[1],"\nsupplier name:",t[2],"\nquantity of item:",t[3])
def dispdetitna():#displays details of item when itemname is entered
    n=input("enter item name:")
    cur.execute("select * from stock where itemname='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("item name does not match\nitem doesn't exist")
    else:
        t=s[0]
        print("item id:",n,"\nsupplier id:",t[1],"\nsupplier name:",t[2],"\nquantity of item:",t[3])
def dispdetit():#combination of previous 2 functions
    print("To get details of the item by entering item id enter 1")
    print("To get details of the item by entering item name enter 2")
    n=int(input("enter choice:"))
    if n==1:
        dispdetitid()
    elif n==2:
        dispdetitna()
    else:
        print("please enter a valid choice")
def delitem():#function to delete details of given item from the stock 
    n=input("enter item id:")
    cur.execute("select * from stock where itemid='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("item id does not match\nitem doesn't exist")
    else:
        cur.execute("delete from stock where itemid='{}'".format(n))
        cur.execute("commit;")
def changeitna():#function to change item name
    n=input("enter item id:")
    cur.execute("select * from stock where itemid='{}'".format(n))
    s=cur.fetchall()
    if s==[]:
        print("item id does not match\nitem doesn't exist")
    else:
        a=input("enter new item id(maximum of 10 characters):")
        cur.execute("update stock set itemname='{}' where itemid='{}'".format(a,n))
        cur.execute("commit;") 
def checkquanzero():#function to check whether the quantity of an item is 0
    cur.execute("select * from stock;")
    s=cur.fetchall()
    for i in s:
        if i[3]==0:
            print("item ",i[2]," is out of stock")
    
        
        
while True:
    cur.execute("select * from supplier;")
    f=cur.fetchall()
    cur.execute("select * from stock;")
    h=cur.fetchall()
    print(h)
    print(f)
    if f==[]:
        print("")
        print("To exit program enter 0")
        print("To stay in the program enter 1")
        i=int(input("enter choice:"))
        if i!=0:
            print("enter supplier details")
            inputsup()
        else:
            break
    elif f!=[] and h==[]:
        print("")
        print("To exit program enter 0")
        print("To enter supplier details enter 1")
        print("To enter stock details enter 2")
        print("To get details of a supplier enter 3")
        print("To remove a supplier enter 4")
        print("To change details of a supplier enter 5")
        i=int(input("enter choice:"))
        if i==1:
            inputsup()
        elif i==2:
            inputstock() 
        elif i==3:
            getdetsup() 
        elif i==4:
            delsupdet()
        elif i==5:
            changedetsup()
        elif i==0:
            break
        else:
            print("enter a valid choice")
    else:
        print("")
        print("To exit program enter 0")
        print("To enter supplier details enter 1")
        print("To enter stock details enter 2")
        print("To get details of a supplier enter 3")
        print("To remove a supplier enter 4")
        print("To change details of a supplier enter 5")
        print("To display the items supplied by a given supplier enter 6")
        print("To update quantity of an item enter 7")
        print("To change supplier of an item enter 8")
        print("To change name of a given item enter 9")
        print("To display details of an item enter 10")
        print("To delete details of an item enter 11")
        i=int(input("enter choice:"))
        if i==1:
            inputsup()
        elif i==2:
            inputstock() 
        elif i==3:
            getdetsup() 
        elif i==4:
            delsupdet()
        elif i==5:
            changedetsup()
        elif i==6:
            dissupite()
        elif i==7:
            updatquan()
        elif i==8:
            changesup()
        elif i==9:
            changeitna()
        elif i==10:
            dispdetit() 
        elif i==11:
            delitem()
        elif i==0:
            break
        else:
            print("enter a valid choice")
        
con.close()            

