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

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.* FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id =?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id =?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]
