import os
import sys
from datetime import datetime

import psycopg2
from PyPDF2 import PdfReader

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="task",
    user="postgres",
    password="1",
    host="localhost",
    port="5432",
)
cur = conn.cursor()


def parse_datetime(datetime_str):
    """
    Parse date/time string from PDF metadata to a Python datetime object.
    """
    # Extract the date/time string without 'D:'
    datetime_str = datetime_str[2:]
    # Extract date and time components
    date_str = datetime_str[:8]
    time_str = datetime_str[8:14]
    # Convert to Python datetime object
    datetime_obj = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
    return datetime_obj


def extract_metadata(pdf_path):
    """
    Extract metadata from a PDF file.
    """
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        info = reader.metadata
        title = info.get("/Title")
        author = info.get("/Author")
        subject = info.get("/Subject")
        creator = info.get("/Creator")
        creation_date = parse_datetime(info.get("/CreationDate"))
        modification_date = parse_datetime(info.get("/ModDate"))
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return (
            title,
            author,
            subject,
            creator,
            creation_date,
            modification_date,
            content,
        )


def insert_pdf_metadata_into_db(
    pdf_path, title, author, subject, creator, creation_date, modification_date, content
):
    """
    Insert PDF metadata into PostgreSQL database.
    """
    try:
        cur.execute(
            "INSERT INTO pdf_metadata (pdf_path, title, author, subject, creator, creation_date, modification_date, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                pdf_path,
                title,
                author,
                subject,
                creator,
                creation_date,
                modification_date,
                content,
            ),
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {e}")


def scan_directory_and_insert_into_db(directory):
    """
    Recursively scan a directory and its subdirectories,
    extract metadata from PDF files, and insert into PostgreSQL database.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                (
                    title,
                    author,
                    subject,
                    creator,
                    creation_date,
                    modification_date,
                    content,
                ) = extract_metadata(file_path)
                insert_pdf_metadata_into_db(
                    file_path,
                    title,
                    author,
                    subject,
                    creator,
                    creation_date,
                    modification_date,
                    content,
                )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py directory_path")
        sys.exit(1)

    directory_to_scan = sys.argv[1]
    if not os.path.isdir(directory_to_scan):
        print(f"Error: {directory_to_scan} is not a valid directory.")
        sys.exit(1)

    # Create table if not exists
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pdf_metadata (
            id SERIAL PRIMARY KEY,
            pdf_path TEXT,
            title TEXT,
            author TEXT,
            subject TEXT,
            creator TEXT,
            creation_date TIMESTAMP,
            modification_date TIMESTAMP,
            content TEXT
        )
    """
    )
    conn.commit()

scan_directory_and_insert_into_db(directory_to_scan)

# Close the database connection
cur.close()
conn.close()
