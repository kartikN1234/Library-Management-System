import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:

    database = "library.json"
    data = {"books": [], "members": []}

    # Load existing data from JSON or create JSON file
    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read().strip()

            if content:
                data = json.loads(content)

    else:
        with open(database, "w") as f:
            json.dump(data, f, indent=4)

    # Generate ID
    @staticmethod
    def gen_id(prefix="B"):

        random_id = ""

        for i in range(5):
            random_id += random.choice(
                string.ascii_uppercase + string.digits
            )

        return prefix + "-" + random_id

    # Save data
    @classmethod
    def save_data(cls):

        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4, default=str)

    # Add book
    @classmethod
    def add_book(cls, title, author, copies):

        book = {
            "id": cls.gen_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime(
                "%d/%m/%Y, %H:%M:%S"
            )
        }

        cls.data["books"].append(book)

        cls.save_data()

    # Add member
    @classmethod
    def add_member(cls, name, mobile, email):

        member = {
            "id": cls.gen_id("M"),
            "name": name,
            "Mobile_number": mobile,
            "email": email,
            "borrowed_book": []
        }

        cls.data["members"].append(member)

        cls.save_data()

    # Borrow book
    @classmethod
    def borrow_book(cls, member_id, book_id):

        members = [
            m for m in cls.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            return False, "No such member ID exists."

        member = members[0]

        books = [
            b for b in cls.data["books"]
            if b["id"] == book_id
        ]

        if not books:
            return False, "No such book ID exists."

        book = books[0]

        if book["available_copies"] <= 0:
            return False, "Sorry, no copies are currently available."

        borrow_entry = {
            "book_id": book["id"],
            "title": book["title"],
            "borrow_on": datetime.now().strftime(
                "%d/%m/%Y, %H:%M:%S"
            )
        }

        member["borrowed_book"].append(borrow_entry)

        book["available_copies"] -= 1

        cls.save_data()

        return True, "Book borrowed successfully."


    # Return book
    @classmethod
    def return_book(cls, member_id, book_id):

        members = [
            m for m in cls.data["members"]
            if m["id"] == member_id
        ]

        if not members:
            return False, "No such member ID exists."

        member = members[0]

        borrowed_books = [
            b for b in member["borrowed_book"]
            if b["book_id"] == book_id
        ]

        if not borrowed_books:
            return False, "This book is not borrowed by this member."

        # Remove borrowed book
        selected = borrowed_books[0]

        member["borrowed_book"].remove(selected)

        # Find original book
        books = [
            b for b in cls.data["books"]
            if b["id"] == book_id
        ]

        if books:
            books[0]["available_copies"] += 1

        cls.save_data()

        return True, "Book returned successfully."


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# Title
st.title("📚 Library Management System")

st.markdown("---")


# Sidebar
st.sidebar.title("Menu")

choice = st.sidebar.radio(
    "Select Operation",
    [
        "Dashboard",
        "Add Book",
        "List Books",
        "Add Member",
        "List Members",
        "Borrow Book",
        "Return Book"
    ]
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if choice == "Dashboard":

    st.header("Dashboard")

    total_books = len(Library.data["books"])
    total_members = len(Library.data["members"])

    total_copies = sum(
        book["total_copies"]
        for book in Library.data["books"]
    )

    available_copies = sum(
        book["available_copies"]
        for book in Library.data["books"]
    )

    borrowed_copies = total_copies - available_copies

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Book Titles",
        total_books
    )

    col2.metric(
        "Total Members",
        total_members
    )

    col3.metric(
        "Total Copies",
        total_copies
    )

    col4.metric(
        "Borrowed Copies",
        borrowed_copies
    )

    st.markdown("---")

    st.subheader("Available Copies")

    st.write(
        f"Currently available: **{available_copies}**"
    )


# --------------------------------------------------
# ADD BOOK
# --------------------------------------------------

elif choice == "Add Book":

    st.header("➕ Add Book")

    with st.form("add_book_form"):

        title = st.text_input(
            "Book Title"
        )

        author = st.text_input(
            "Book Author"
        )

        copies = st.number_input(
            "Number of Copies",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button(
            "Add Book"
        )

        if submitted:

            if not title.strip():
                st.error("Please enter the book title.")

            elif not author.strip():
                st.error("Please enter the author name.")

            else:

                Library.add_book(
                    title,
                    author,
                    copies
                )

                st.success(
                    "Book added successfully!"
                )


# --------------------------------------------------
# LIST BOOKS
# --------------------------------------------------

elif choice == "List Books":

    st.header("📚 All Books")

    books = Library.data["books"]

    if not books:

        st.info("No books found.")

    else:

        for book in books:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(4)

                col1.write(
                    f"**ID:** {book['id']}"
                )

                col2.write(
                    f"**Title:** {book['title']}"
                )

                col3.write(
                    f"**Author:** {book['author']}"
                )

                col4.write(
                    f"**Available:** "
                    f"{book['available_copies']}/"
                    f"{book['total_copies']}"
                )


# --------------------------------------------------
# ADD MEMBER
# --------------------------------------------------

elif choice == "Add Member":

    st.header("👤 Add Member")

    with st.form("add_member_form"):

        name = st.text_input(
            "Member Name"
        )

        mobile = st.text_input(
            "Mobile Number"
        )

        email = st.text_input(
            "Email"
        )

        submitted = st.form_submit_button(
            "Add Member"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter the member name."
                )

            elif not mobile.strip():

                st.error(
                    "Please enter the mobile number."
                )

            elif not email.strip():

                st.error(
                    "Please enter the email."
                )

            else:

                Library.add_member(
                    name,
                    mobile,
                    email
                )

                st.success(
                    "Member added successfully!"
                )


# --------------------------------------------------
# LIST MEMBERS
# --------------------------------------------------

elif choice == "List Members":

    st.header("👥 All Members")

    members = Library.data["members"]

    if not members:

        st.info("No members found.")

    else:

        for member in members:

            with st.container(border=True):

                st.subheader(
                    f"{member['name']} "
                    f"({member['id']})"
                )

                col1, col2 = st.columns(2)

                col1.write(
                    f"📱 **Mobile:** "
                    f"{member['Mobile_number']}"
                )

                col2.write(
                    f"📧 **Email:** "
                    f"{member['email']}"
                )

                borrowed = member["borrowed_book"]

                if borrowed:

                    st.write("**Borrowed Books:**")

                    for i, book in enumerate(
                        borrowed,
                        start=1
                    ):

                        st.write(
                            f"{i}. "
                            f"{book['title']} "
                            f"({book['book_id']})"
                        )

                else:

                    st.write(
                        "No books currently borrowed."
                    )


# --------------------------------------------------
# BORROW BOOK
# --------------------------------------------------

elif choice == "Borrow Book":

    st.header("📖 Borrow Book")

    members = Library.data["members"]
    books = Library.data["books"]

    if not members:

        st.warning(
            "No members available. Add a member first."
        )

    elif not books:

        st.warning(
            "No books available. Add a book first."
        )

    else:

        member_options = {
            f"{m['name']} ({m['id']})": m["id"]
            for m in members
        }

        book_options = {
            f"{b['title']} "
            f"({b['id']}) - "
            f"Available: {b['available_copies']}":
            b["id"]
            for b in books
            if b["available_copies"] > 0
        }

        if not book_options:

            st.warning(
                "No books are currently available."
            )

        else:

            selected_member = st.selectbox(
                "Select Member",
                list(member_options.keys())
            )

            selected_book = st.selectbox(
                "Select Book",
                list(book_options.keys())
            )

            if st.button(
                "Borrow Book",
                type="primary"
            ):

                member_id = member_options[
                    selected_member
                ]

                book_id = book_options[
                    selected_book
                ]

                success, message = Library.borrow_book(
                    member_id,
                    book_id
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)


# --------------------------------------------------
# RETURN BOOK
# --------------------------------------------------

elif choice == "Return Book":

    st.header("🔄 Return Book")

    members = Library.data["members"]

    members_with_books = [
        m for m in members
        if m["borrowed_book"]
    ]

    if not members_with_books:

        st.info(
            "No member currently has a borrowed book."
        )

    else:

        member_options = {
            f"{m['name']} ({m['id']})":
            m["id"]
            for m in members_with_books
        }

        selected_member = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        member_id = member_options[
            selected_member
        ]

        member = next(
            m for m in members
            if m["id"] == member_id
        )

        borrowed_books = member["borrowed_book"]

        book_options = {
            f"{b['title']} ({b['book_id']})":
            b["book_id"]
            for b in borrowed_books
        }

        selected_book = st.selectbox(
            "Select Book to Return",
            list(book_options.keys())
        )

        if st.button(
            "Return Book",
            type="primary"
        ):

            book_id = book_options[
                selected_book
            ]

            success, message = Library.return_book(
                member_id,
                book_id
            )

            if success:
                st.success(message)
                st.rerun()

            else:
                st.error(message)