from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
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
        print(f"Setting magazine name to: {value}")  # Debugging print
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        print(f"Setting magazine category to: {value}")  # Debugging print
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.* FROM articles
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    def article_titles(self):
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        if not authors:
            return None
        return [Author(author['id'], author['name']) for author in authors]
