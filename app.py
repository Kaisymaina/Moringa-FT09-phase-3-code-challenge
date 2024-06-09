from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def cleanup_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete invalid magazines
    cursor.execute('DELETE FROM magazines WHERE name = "" OR category = ""')

    # Delete invalid authors
    cursor.execute('DELETE FROM authors WHERE name = ""')

    conn.commit()
    conn.close()

def main():
    # Initialize the database and create tables
    create_tables()

    # Clean up invalid entries in the database
    cleanup_database()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Collect user input
    author_name = input("Enter author's name: ").strip()
    while not author_name:
        author_name = input("Author's name cannot be empty. Enter author's name: ").strip()

    magazine_name = input("Enter magazine name: ").strip()
    while not (2 <= len(magazine_name) <= 16):
        magazine_name = input("Magazine name must be between 2 and 16 characters. Enter magazine name: ").strip()

    magazine_category = input("Enter magazine category: ").strip()
    while not magazine_category:
        magazine_category = input("Magazine category cannot be empty. Enter magazine category: ").strip()

    article_title = input("Enter article title: ").strip()
    while not (5 <= len(article_title) <= 50):
        article_title = input("Article title must be between 5 and 50 characters. Enter article title: ").strip()

    article_content = input("Enter article content: ").strip()
    while not article_content:
        article_content = input("Article content cannot be empty. Enter article content: ").strip()

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(f"Magazine ID: {magazine['id']}, Name: {magazine['name']}, Category: {magazine['category']}")
        mag_instance = Magazine(magazine["id"], magazine["name"], magazine["category"])
        print(mag_instance)

    print("\nAuthors:")
    for author in authors:
        print(f"Author ID: {author['id']}, Name: {author['name']}")
        author_instance = Author(author["id"], author["name"])
        print(author_instance)

    print("\nArticles:")
    for article in articles:
        print(f"Article ID: {article['id']}, Title: {article['title']}, Content: {article['content']}")
        article_instance = Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"])
        print(article_instance)

if __name__ == "__main__":
    main()
