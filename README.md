# 📚 Library Management System

A Python-based Library Management System with both a **command-line interface (CLI)** and a **Streamlit web interface**. It helps manage books and library members, track borrowed books, and update the number of available copies. Data is stored locally in a JSON file.

## Features

- **Dashboard:** View the number of book titles, members, total copies, borrowed copies, and available copies.
- **Add Books:** Store a book's title, author, total copies, and available copies.
- **List Books:** View book IDs, titles, authors, and copy availability.
- **Add Members:** Register members with a name, mobile number, and email address.
- **List Members:** View registered members and the books they have borrowed.
- **Borrow Books:** Check member and book IDs, confirm availability, and record a borrowing date.
- **Return Books:** Record book returns and increase the available-copy count.
- **Persistent Storage:** Save book and member records in `library.json`.
- **Generated IDs:** Assign unique-looking IDs to books and members.

## Technologies Used

- Python
- Streamlit
- JSON for local data storage
- Python standard-library modules: `json`, `random`, `string`, `pathlib`, and `datetime`

## Project Structure

```text
Library-Management/
├── main.py          # Command-line version
├── stream.py        # Streamlit web application
├── library.json     # JSON data store for books and members
└── README.md        # Project documentation
```

## Requirements

- Python 3.9 or later recommended
- `pip`
- A terminal or code editor such as Visual Studio Code

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kartikN1234/Library-Management-System.git
cd "Library Management"
```



### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

The command-line version (`main.py`) uses Python's standard library. The web version requires Streamlit.

```bash
python -m pip install streamlit
```



```

## Run the Application

### Option A: Streamlit web application
From the project directory, run:

```bash
python -m streamlit run stream.py
```

Streamlit will display a local URL in the terminal, usually `http://localhost:8501`. Open that address in your browser.

Use the sidebar to navigate between Dashboard, Add Book, List Books, Add Member, List Members, Borrow Book, and Return Book.

### Option B: Command-line application

Run:

```bash
python main.py
```

Follow the numbered menu in the terminal to add/list books and members, borrow or return books, or exit.

## Data Storage

The application reads and writes its records to `library.json`. The JSON file contains two main collections:

- `books`: book ID, title, author, total copies, available copies, and date added.
- `members`: member ID, name, mobile number, email, and borrowed-book records.

Keep `library.json` in the working directory used to launch the application. The app creates the file with empty book and member lists if it does not exist.

## Important Notes

- This project uses a local JSON file rather than a database server.
- The JSON file is updated when books or members are added and when books are borrowed or returned.
- Use test or sample records when demonstrating the project. Avoid publishing real members' phone numbers, email addresses, or other personal information in `library.json`.
- Before pushing to GitHub, review `library.json` and replace any personal or real member information with sample data.
- The current implementation is intended as a learning project, not a production library system. For real-world use, add stronger validation, duplicate-ID handling, safer error handling, and database-backed storage.
- If you deploy the Streamlit version to a hosting service, check that the platform supports persistent file storage. A local JSON file may not be retained reliably across redeployments or shared safely by multiple users.

## Python Concepts Demonstrated

- Classes and class methods
- Lists and dictionaries
- Functions and control flow
- Reading and writing JSON files
- Generating IDs using `random` and `string`
- Date and time handling with `datetime`
- File and path handling with `pathlib`
- Streamlit forms, sidebar navigation, metrics, columns, and status messages
- Basic validation of book/member IDs and available copies

## Future Improvements

- Add edit and delete operations for books and members.
- Add due dates, return deadlines, and overdue tracking.
- Add search and filtering for books and members.
- Improve input validation and exception handling.
- Prevent duplicate borrowing records where appropriate.
- Add authentication and role-based access for librarians and members.
- Migrate from JSON storage to SQLite or another database for more robust persistence.
- Add automated tests.

## Author

Kartik Nalawade

- GitHub: https://github.com/kartikN1234

---

If you find this project useful, feel free to star the repository.
