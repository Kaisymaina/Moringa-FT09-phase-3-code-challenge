from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = value

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

class ArticleRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_article(self, title, content, author_id, magazine_id):
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (title, content, author_id, magazine_id))
        article_id = cursor.lastrowid
        self.db_connection.commit()
        return article_id

    def get_author(self, article_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        ''', (article_id,))
        author_data = cursor.fetchone()
        return Author(author_data['id'], author_data['name'])

    def get_magazine(self, article_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            SELECT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        ''', (article_id,))
        magazine_data = cursor.fetchone()
        return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category'])

# Example usage:
db_connection = get_db_connection()
article_repository = ArticleRepository(db_connection)

article_id = article_repository.create_article("Example Title", "Example Content", 1, 1)
article = Article(article_id, "Example Title", "Example Content", 1, 1)

author = article_repository.get_author(article_id)
print(author.name)

magazine = article_repository.get_magazine(article_id)
print(magazine.name)
