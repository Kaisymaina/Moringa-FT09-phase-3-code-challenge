import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(None, "John Doe")  # Providing id as None, as it will be assigned automatically
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(None, "Test Title", "Test Content", 1, 1)  # Assuming author_id and magazine_id are 1 for the test
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(None, "Tech Weekly", "Technology")  # Providing id as None, as it will be assigned automatically
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

if __name__ == "__main__":
    unittest.main()

