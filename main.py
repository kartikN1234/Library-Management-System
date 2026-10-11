import json
import random
import string
from pathlib import Path
from datetime import datetime
#These are libraries

class Library:
    database="library.json"
    data={"books":[],"members":[]}

    #load existing data from JSON or create your json
    if Path(database).exists():
        with open(database,"r") as f:
            content=f.read().strip()
            if content:
                data=json.loads(content)
    else:
        with open(database,"w") as f:
            json.dump(data,f,indent=4)


    def gen_id(Prefix="B"):
        random_id=""
        for i in range(5):
            random_id+=random.choice(string.ascii_uppercase+string.digits)

        return Prefix+ "-" + random_id

    @classmethod
    def save_data(cls):
        with open(cls.database,"w") as f:
            json.dump(cls.data,f,indent=4,default=str)

    def add_book(self):
        title=input("Enter the book title: ")
        author=input("Enter the book author: ")
        copies=int(input("How many copies you want to add: "))

        book={
            "id":Library.gen_id(), #This works because gen_id() doesn't use anything from the Library object.Library.gen_id() is being used because gen_id() doesn't need self or any object-specific data.Call the gen_id function directly from the Library class.
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies":copies,
            "added_on":datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        Library.data["books"].append(book)
        Library.save_data()

    def list_books(self):
        if not Library.data["books"]:
            print("Sorry no books found")
            return
        else:
            for b in Library.data["books"]:
                print(f"{b["id"]:12} {b["title"][:24]:25} {b["author"][:19]:20} {b["total_copies"]}/{b["available_copies"]:>3}")


    def add_member(self):
        name=input("Enter your name: ")
        Mobile=int(input("Enter your mobile number: "))
        email=input("Enter your email: ")

        member={
            "id":Library.gen_id("M"),
            "name":name,
            "Mobile_number":Mobile,
            "email":email,
            "borrowed_book":[]

        }
        Library.data["members"].append(member)
        Library.save_data()
        print("Member added successfully")

    def list_members(self):
        if not Library.data["members"]:
            print("No members found")
            return 
        else:
            for m in Library.data["members"]:
                print(f"{m['id']:12} {m['name']:15} {m['Mobile_number']:<20} {m['email'][:25]:30}")
                print("This person has corrently ")
                print(f"{m["borrowed_book"]}")

    def borrow_book(self):
        member_id=input("Enter the member ID: ").strip()
        # for m in Library.data["members"]:
        #     if m["id"]==member_id:
        members=[m for m in Library.data["members"] if m["id"]==member_id]
        if not members:
            print("No such ID exist")
            return 
        #If multiple members of the same id came in members then 
        member=members[0]

        book_id=input("Enter the book ID: ").strip()
        books=[b for b in Library.data["books"] if b["id"]==book_id]
        if not books:
            print("No such book exist")
            return 
        book=books[0]

        if book["available_copies"]<=0:
            print("sorry no books exists right now")
            return
        borrow_entry={
            "book_id":book["id"],
            "title":book["title"],
            "borrow_on":datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        # This is an important point because the list is new, but the dictionaries inside it are not deep-copied.
        # Because the list comprehension creates a new list, but m still refers to the same dictionary.
        member["borrowed_book"].append(borrow_entry)
        book["available_copies"]-=1
        Library.save_data()

    def return_book(self):
        member_id=input("Enter the member ID: ").strip()
        members=[m for m in Library.data["members"] if m["id"]==member_id]
        if not members:
            print("No such ID exist")
            return 
        member=members[0]

        if not member["borrowed_book"]:
            print("You haven't borrowed any book yet")
            return

        print("Borrowed Books")
        for i,b in enumerate(member["borrowed_book"],start=1):
            print(f"{i}. {b["title"]} ({b["book_id"]})")

        try:
            choice=int(input("Enter number to return: "))
            selected=member["borrowed_book"].pop(choice-1)
        except Exception as err:
            print("Invalid value")

        books=[bk for bk in Library.data["books"] if bk["id"]==selected["book_id"]]
        # book=books[0]
        # book["available_copies"]+=1
        if books:
            books[0]["available_copies"]+=1
        Library.save_data()

       





        

object=Library()


print("="*50)
print("Library Management System")
print("="*50)
print("1. Add Book")
print("2. List Books")
print("3. Add Member")
print("4. List Members")
print("5. Borrow Book")
print("6. Return Book")
print("0. Exit the portal")
print("-"*50)


while True:
    choice=int(input("What task you want to do ? "))

    if choice == 1:
        object.add_book()
    elif choice==2:
        object.list_books()
    elif choice==3:
        object.add_member()
    elif choice==4:
        object.list_members()
    elif choice==5:
        object.borrow_book()
    elif choice==6:
        object.return_book()
    elif choice==0:
        print("Thank you for visiting :)")
        exit(0)

