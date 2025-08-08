import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import requests

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")
        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        self.assertIn("https://example.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No keyword here"
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    def test_search_no_match(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "Nothing relevant"
        results = crawler.search("missing")
        self.assertEqual(results, [])

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        output = mock_stdout.getvalue()
        self.assertIn("https://test.com/result", output)

if __name__ == "__main__":
    unittest.main()
