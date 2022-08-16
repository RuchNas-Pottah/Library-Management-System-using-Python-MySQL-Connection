import datetime
from datetime import date
import tkinter as tk
from tkinter import *
import mysql.connector as sqltor
mycon=sqltor.connect(host='localhost',user='root',passwd='***',database='library')
if mycon.is_connected():
    print('successfully connected mysql and python')
cursor=mycon.cursor()
import differdays
#storing the BookNo, BookNames and publication in lists
bnum=[]
cursor.execute('select distinct BookNo from Avalibility')
data=cursor.fetchall()
for row in data:
    bnum.append(row)
#creating a list with the book numbers only
bnumint=[]
for i in bnum:
    bnumint.append(int(list(i)[0]))
bname=[]
cursor.execute('select Name from Avalibility')
data=cursor.fetchall()
for row in data:
    bname.append(row)
bpub=[]
cursor.execute('select Publisher from Avalibility')
data=cursor.fetchall()
for row in data:
    bpub.append(row)
#storing the memberid in a list
mn=[]
cursor.execute('select id from Readers')
data=cursor.fetchall()
for row in data:
    mn.append(row)
mnint=[]
for i in mn:
    mnint.append(int(list(i)[0]))
def Showbooks():
    #to show the availibility table
    print('books:-')
    cursor.execute('select * from Avalibility')
    data=cursor.fetchall()
    for row in data:
        print(row)
    if data==[]:
        print('no record')
    print('\n')
def Readers():
    print('readers:-')
    #to show the Readers table
    cursor.execute('select * from readers')
    data=cursor.fetchall()
    for row in data:
        print(row)
    if data==[]:
        print('no record')
    print('\n')
def entry():
    #new entry in Readers table
    nm=input('enter member name')
    id=int(list(mn[len(mn)-1])[0])+1
    mn.append((id,))
    mnint.append(id)
    st="insert into Readers(Name,Id,BookIssued,DateOfIssue,DateOfReturn) values('{}',{},{},'{}','{}')".format(nm,id,0,'00-00-00','00-00-00')
    cursor.execute(st)
    mycon.commit()
def bookentry():
    #to enter distict new books
    n=int(input('enter number of distinct books to be added'))
    for i in range (n):
        nm=input('enter book name')
        id=int(list(bnum[len(bnum)-1])[0])+1
        au=input('enter author name')
        publ=input('enter name of publisher')
        cost=int(input('enter cost'))
        copies=int(input('enter number of copies'))
        status=input('enter status')
        if ((nm,) in bname and (publ,) in bpub):
            continue
        else:
            st="insert into Avalibility(BookNo,Name,Author,Publisher,Cost,NoOfCopies,Status) values({},'{}','{}','{}',{},{},'{}')".format(id,nm,au,publ,cost,copies,status)
            cursor.execute(st)
            mycon.commit()
            bnum.append((id,))
            bnumint.append(id)
            bname.append((nm,))
            bpub.append((publ,))
def update():
    #to update number of copies of a book
    nm=input('enter book name')
    n=int(input('enter number of copies of the book to be added'))
    m="select NoOfCopies from Avalibility where Name='%s'"%(nm,)
    cursor.execute(m)
    data=cursor.fetchall()
    if len(data)==0:
        print('no records found')
    else:
        for row in data:
            j=int(row[0])
            st="update Avalibility set NoOfCopies={} where Name='{}'".format(j+n,nm)
            cursor.execute(st)
            mycon.commit()
def ShowLate():
    print('late records:-')
    #to show Late records
    cursor.execute("select * from Late")
    data=cursor.fetchall()
    for row in data:
        print(row)
    if data==[]:
        print('no record')
    print('\n')
def ShowLost():
    print('lost records:-')
    #to show Late records
    cursor.execute("select * from Lost")
    data=cursor.fetchall()
    for row in data:
        print(row)
    if data==[]:
        print('no record')
    print('\n')
def lateInput():
    #to mark late fines
    id=int(input('enter member id'))
    x="select BookIssued from Readers where Id={} and DateOfIssue not like '{}'".format(id,'0000-00-00')
    cursor.execute(x)
    data=cursor.fetchall()
    if len(data)==0:
        print('Book not issued to this reader')
    else:
        y=0
        for row in data:
            y=int(row[0])
        bookno=y
        m="select DateOfReturn from Readers where Id='%s'"%(id,)
        cursor.execute(m)
        data=cursor.fetchall()
        j=''
        for row in data:
            j=str(row[0])
        print('tentative date of return was',j)
        today=input("enter today's date in the format: YYYY-MM-DD")
        print('Today is',today)
        s=differdays.differdays(today,j)
        if s<0:
            print('not possible, number of days cannot be negative',s)
        else:
            fine=s*2
            st="insert into Late(BookNo,Id,Finereqd)values({},{},{})".format(bookno,id,fine)
            cursor.execute(st)
            mycon.commit()
            ShowLate()
            st="update Readers set BookIssued={}, DateOfIssue='{}', DateOfReturn='{}' where Id={}".format(0,'00-00-00','00-00-00',id)
            cursor.execute(st)
            mycon.commit()
            Readers()
            #Readers table updated
def lateOut():
    #to delete late record and return book
    id=int(input('enter member id'))
    bookno="select BookNo from Late where Id={}".format(id)
    cursor.execute(bookno)
    data=cursor.fetchall()
    if len(data)==0:
        print('no records found in late list')
    else:
        bookie=''
        for row in data:
            bookie=int(row[0])
        st="delete from Late where Id={}".format(id)
        cursor.execute(st)
        mycon.commit()
        ShowLate()
        j=0
        m="select NoOfCopies from Avalibility where BookNo='%s'"%(bookie,)
        cursor.execute(m)
        data=cursor.fetchall()
        for row in data:
            j=int(row[0])
        st="update Avalibility set NoOfCopies={} where BookNo={}".format(j+1,bookie)
        cursor.execute(st)
        mycon.commit()
        print('removing member from LateFine list')
        print('showing the resultant stock')
        Showbooks()
        #Avalibility table updated
def lostInput():
    #to put name into lost list
    id=int(input('enter member id'))
    if id not in mnint:
        print('invalid id')
    x="select BookIssued from Readers where Id={} and DateOfIssue not like '{}'".format(id,'0000-00-00')
    cursor.execute(x)
    data=cursor.fetchall()
    if len(data)==0:
        print('no records found in lost')
    else:
        y=0
        for row in data:
            y=int(row[0])
        bookno=y
        m="select DateOfReturn from Readers where Id='%s'"%(id,)
        cursor.execute(m)
        data=cursor.fetchall()
        j=''
        for row in data:
            j=str(row[0])
        print('tentative date of return was',j)
        today=input("enter today's date in the format: YYYY-MM-DD")
        print('Today is',today)
        s=differdays.differdays(today,j)
        if s<0:
            print('not possible, number of days cannot be negative',s)
        else:
            fine=s*2
            st="insert into Lost(BookNo,Id,Finereqd) values({},{},{})".format(bookno,id,fine)
            cursor.execute(st)
            mycon.commit()
            ShowLost()
            print('please abide by the above mentioned fine and the replace the book')
            #marking the lost book in Availibility
            st="update Avalibility set Status='{}' where BookNo={}".format('L',bookno)
            cursor.execute(st)
            mycon.commit()
            Showbooks()
            st="update Readers set BookIssued={}, DateOfIssue='{}', DateOfReturn='{}' where Id={}".format(0,'00-00-00','00-00-00',id)
            cursor.execute(st)
            mycon.commit()
            Readers()
            #Readers table updated
def lostOut():
    id=int(input('enter member id'))
    print('removing member from Lost list')
    bookno='select BookNo from Lost where id={}'.format(id)
    cursor.execute(bookno)
    data=cursor.fetchall()
    if len(data)==0:
        print('no records found')
    else:
        y=0
        for row in data:
            y=int(row[0])
        bookie=y
        print(bookie)
        st="delete from Lost where id={}".format(id)
        cursor.execute(st)
        mycon.commit()
        yt="update Avalibility set Status='{}' where BookNo={}".format('y',bookie)
        cursor.execute(yt)
        mycon.commit()
        ShowLost()
        j=0
        m="select NoOfCopies from Avalibility where BookNo='%s'"%(bookie,)
        cursor.execute(m)
        data=cursor.fetchall()
        for row in data:
            j=int(row[0])
        st="update Avalibility set NoOfCopies={} where BookNo={}".format(j+1,bookie)
        cursor.execute(st)
        mycon.commit()
        print('showing the resultant stock')
        Showbooks()
    #Avalibility table updated
def readbook():
    name=input('enter book name')
    m="select Bookno from Avalibility where Name='%s'"%(name,)
    cursor.execute(m)
    data=cursor.fetchall()
    j=0
    for i in data:
        j=int(i[0])
    if len(data)==0:
        print('invalid book name')
    else:
        x="select * from Readers, Avalibility where Bookno={} and Readers.Bookissued=avalibility.BookNo".format(j)
        cursor.execute(x)
        data=cursor.fetchall()
        if len(data)==0:
            print('book not taken')
        else:
            for row in data:
                print(row)
def findreader():
    name=input('enter reader name')
    m="select id from readers where Name='%s'"%(name,)
    cursor.execute(m)
    data=cursor.fetchall()
    j=0
    for i in data:
        j=int(i[0])
    if len(data)==0:
        print('invalid reader name')
    else:
        x="select * from Readers, Avalibility where id={} and Readers.Bookissued=avalibility.BookNo".format(j)
        cursor.execute(x)
        data=cursor.fetchall()
        if len(data)==0:
            print('book not taken')
            st="select * from readers where Name='%s'"%(name,)
            cursor.execute(st)
            data=cursor.fetchall()
            for row in data:
                print(row)
        else:
            for row in data:
                print(row)
def Showall():
    root = tk.Tk()
    root.geometry("800x300")
    root.title("LIBRARY")
    root.configure(bg="sky blue")

    submitbtn1 = tk.Button(root, text ="Showing the book records",  
                      bg ='blue', command = Showbooks)
    submitbtn1.place(x = 150, y = 75, width = 500)

    submitbtn2= tk.Button(root, text ="Showing the readers records",  
                      bg ='red', command = Readers)
    submitbtn2.place(x = 150, y = 100, width = 500)

    submitbtn3 = tk.Button(root, text ="Showing the late records",  
                      bg ='yellow', command = ShowLate)
    submitbtn3.place(x = 150, y = 125, width = 500)

    submitbtn4 = tk.Button(root, text ="Showing the lost records",  
                      bg ='green', command = ShowLost)
    submitbtn4.place(x = 150, y = 150, width = 500)

    root.mainloop()
def cont():
    print('list of book ids',bnumint)
    print('list of member ids',mnint)
    #Selecting course of action
    print('Please select any of the following options to proceed')
    print('1.Manually Browse the Library''\n''2. Ask for the book status as per specifications''\n''3.Become a member''\n''4.Take Book''\n''5.Return Book')
    print('6.Add new books''\n''7.Accept fines''\n''8.Check which reader has a book''\n''9.Find a reader''\n''10.Show the tables')
    choice=int(input('enter choice'))
    if choice==1:
        #library to be browsed manually
        print('Welcome Explorer!')
    elif choice==2:
        #book status is to be asked
        print('1.Browse by Name''\n''2. Browse by author''\n''3.Browse by Publisher')
        ch=int(input('make your choice'))
        if ch==1:
            nm=input('enter name of the book')
            st="select * from avalibility where Name='%s'"%(nm,)
            cursor.execute(st)
            data=cursor.fetchall()
            for row in data:
                print(row)
            if data==[]:
                print('no record')
        if ch==2:
            nm=input('enter author')
            st="select * from avalibility where Author='%s'"%(nm,)
            cursor.execute(st)
            data=cursor.fetchall()
            for row in data:
                print(row)
            if data==[]:
                print('no record')
        if ch==3:
            nm=input('enter name of the Publisher')
            st="select * from avalibility where Publisher='%s'"%(nm,)
            cursor.execute(st)
            data=cursor.fetchall()
            for row in data:
                print(row)
            if data==[]:
                print('no record')
    elif choice==3:
        #new entry
        n=int(input('enter number of new entries to be made in members list'))
        for i in range (n):
            entry()
        Readers()
    elif choice==4:
        #Book to be taken
        ask=int(input('mention BookNo'))
        if ask not in bnumint:
            print('book number entered incorrectly')
        else:
            id=int(input('mention member id'))
            #checking if the reader already has a book
            x="select name from Readers where Bookissued={} and Id='{}'".format(0,id,)
            cursor.execute(x)
            data=cursor.fetchall()
            if len(data)==0:
                print('first return the previous book')
            else:
                st="select * from Avalibility where BookNo='%s'"%(ask,)
                cursor.execute(st)
                data=cursor.fetchall()
                for row in data:
                    print(row)
                #checking if at least one copy of the required book is available
                m="select NoOfCopies from Avalibility where BookNo='%s'"%(ask,)
                cursor.execute(m)
                data=cursor.fetchall()
                for row in data:
                    j=int(row[0])
                    print('number of copies left presently',j)
                    if j!=0:
                        st="update Readers set BookIssued={}, DateOfIssue=now(), DateOfReturn=date_add(now(), interval 15 day) where Id={}".format(ask,id)
                        cursor.execute(st)
                        mycon.commit()
                        Readers()
                        #Readers table updated
                        st="update Avalibility set NoOfCopies={} where BookNo={}".format(j-1,ask)
                        cursor.execute(st)
                        mycon.commit()
                        print('now showing the resultant stock')
                        Showbooks()
                        #Avalibility table updated
                    elif j==0:
                        print('Sorry...no more copy of this book is present now.')
    elif choice==5:
        #Book to be returned
        id=int(input('mention reader id'))
        if id not in mnint:
            print('invalid reader id')
        else:
            x="select name from Readers where Bookissued={} and Id={}".format(0,id,)
            cursor.execute(x)
            data=cursor.fetchall()
            if len(data)!=0:
                print('book not taken yet')
            else:
                x="select BookIssued from Readers where Id={}".format(id,)
                cursor.execute(x)
                data=cursor.fetchall()
                y=0
                for row in data:
                    y=int(row[0])
                bookno=y
                print('book taken is',bookno)
                st="select * from Avalibility where BookNo='%s'"%(bookno,)
                cursor.execute(st)
                data=cursor.fetchall()
                for row in data:
                    print(row)
                st="update Readers set BookIssued={}, DateOfIssue='{}', DateOfReturn='{}' where Id={}".format(0,'00-00-00','00-00-00',id)
                cursor.execute(st)
                mycon.commit()
                print('now showing the Readers table')
                Readers()
                #Readers table updated
                m="select NoOfCopies from Avalibility where BookNo='%s'"%(bookno,)
                cursor.execute(m)
                data=cursor.fetchall()
                j=0
                print(data)
                for row in data:
                    j=int(row[0])
                st="update Avalibility set NoOfCopies={} where BookNo={}".format(j+1,bookno)
                cursor.execute(st)
                mycon.commit()
                print('showing the resultant stock')
                Showbooks()
                #Avalibility table updated
    elif choice==6:
        choice=input('enter a new book? y or n')
        if choice=='y':
            bookentry()
        else:
            update()
        Showbooks()
    elif choice==7:
        #to work out fines: to update the fines table, to delete the record when a fine is paid
        print('Please select any of the following options to proceed')
        print('1.enter record in Late''\n''2. Delete record from Late''\n''3.enter record in Lost''\n''4.Delete record from Lost''\n')
        ch=int(input('enter option'))
        if ch==1:
            lateInput()
        elif ch==2:
            lateOut()
        elif ch==3:
            lostInput()
        else:
            lostOut()
    elif choice==8:
        print('showing status of the required book')
        readbook()
    elif choice==9:
        findreader()
    elif choice==10:
        print('1.Show all books?''\n''2.Show all readers''\n''3.show late records''\n''4.show lost records')
        ch=int(input('enter choice'))
        if ch==1:
            Showbooks()
        elif ch==2:
            Readers()
        elif ch==3:
            ShowLate()
        else:
            ShowLost()        
    else:
        print('invalid option chosen')
#showing all tables
Showall()    
flag=1
while flag==1:
    cont()
    print('\n')
    ask=input('continue? y/n')
    print('\n')
    if ask=='y':
        flag=1
        continue
    else:
        flag=0
        break
