import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.services.news import fetch_articles, Article

MOCK_ARTICLES = [
    {
        "source": {"id": None, "name": "Gizmodo.com"},
        "author": "Matthew Gault",
        "title": "Bitcoin ATM Security Breach Compromised Social Security Numbers and Government IDs",
        "description": "Byte Federal operates 1,200 Bitcoin ATMs...",
        "url": "https://gizmodo.com/bitcoin-atm-security-breach-...",
        "urlToImage": "https://gizmodo.com/app/uploads/2024/12/BitcoinATM.jpg",
        "publishedAt": "2024-12-12T15:30:41Z",
        "content": "A massive data breach hit Bitcoin ATM company Byte Federal..."
    },
    {
        "source": {"id": None, "name": "Slashdot.org"},
        "author": "BeauHD",
        "title": "El Salvador Strikes $1.4 Billion IMF Deal After Scaling Back Bitcoin Policies",
        "description": "El Salvador secured a $1.4 billion loan deal...",
        "url": "https://slashdot.org/story/24/12/24/2015221/el-salvador...",
        "urlToImage": "https://a.fsdn.com/sd/topics/bitcoin_64.png",
        "publishedAt": "2024-12-24T22:40:00Z",
        "content": "In 2021, El Salvador became the first country in the world..."
    },
    {
        "source": {"id": None, "name": "Slashdot.org"},
        "author": "BeauHD",
        "title": "MicroStrategy's Big Bet On Bitcoin Went Stratospheric",
        "description": "MicroStrategy has transformed into a \"bitcoin treasury company,\"...",
        "url": "https://slashdot.org/story/24/12/31/204219/microstrategys...",
        "urlToImage": "https://a.fsdn.com/sd/topics/bitcoin_64.png",
        "publishedAt": "2024-12-31T21:45:00Z",
        "content": "The Fine Print: The following comments are owned by whoever posted them..."
    },
    {
        "source": {"id": None, "name": "[Removed]"},
        "author": None,
        "title": "[Removed]",
        "description": "[Removed]",
        "url": "https://removed.com",
        "urlToImage": None,
        "publishedAt": "2025-01-10T13:45:14Z",
        "content": "[Removed]"
    },
    {
        "source": {"id": None, "name": "NPR"},
        "author": "Rafael Nam",
        "title": "Is this Bitcoin's golden moment? These are 3 key things to watch for cryptos in 2025",
        "description": "Could 2025 be another game changing year for Bitcoin...",
        "url": "https://www.npr.org/2025/01/06/nx-s1-5248284/bitcoin-rally-crypto-trump",
        "urlToImage": "https://npr.brightspotcdn.com/dims3/default/strip/...",
        "publishedAt": "2025-01-06T10:00:00Z",
        "content": "Cryptocurrencies such as Bitcoin have lately been on a wild ride..."
    },
    {
        "source": {"id": None, "name": "Slashdot.org"},
        "author": "msmash",
        "title": "AI Startup Anthropic Raising Funding Valuing it at $60 Billion",
        "description": "Anthropic is in advanced talks to raise $2 billion dollars...",
        "url": "https://slashdot.org/story/25/01/07/1820244/ai-startup...",
        "urlToImage": "https://a.fsdn.com/sd/topics/ai_64.png",
        "publishedAt": "2025-01-07T18:20:00Z",
        "content": "Anthropic is yet another worthless joiner on the wagon..."
    },
    {
        "source": {"id": None, "name": "NPR"},
        "author": "Brittney Melton",
        "title": "Jimmy Carter's funeral services begin in DC. And, photos from the major winter storm",
        "description": "Former President Jimmy Carter's funeral services begin...",
        "url": "https://www.npr.org/2025/01/07/g-s1-41313/up-first-newsletter-jimmy-carter...",
        "urlToImage": "https://npr.brightspotcdn.com/dims3/default/strip/...",
        "publishedAt": "2025-01-07T13:12:36Z",
        "content": "Good morning. You're reading the Up First newsletter..."
    },
    {
        "source": {"id": None, "name": "Yahoo Entertainment"},
        "author": "CoinDesk",
        "title": "Bullish Signals Point to Another Bitcoin Price Explosion",
        "description": "CoinDesk's Christine Lee breaks down a few bullish signals for bitcoin...",
        "url": "https://finance.yahoo.com/video/bullish-signals-point-another-bitcoin-181126826.html",
        "urlToImage": "https://media.zenfs.com/en/coindesk_75/8cc0f8410c8150974ab74a5eef820292",
        "publishedAt": "2024-12-12T18:11:26Z",
        "content": "CoinDesk's Christine Lee breaks down a few bullish signals..."
    },
]

###########
#  Tests  #
###########

class TestFetchArticles(unittest.TestCase):

    def setUp(self):
        # Common mock response for all tests
        self.mock_response_data = {
            "articles": MOCK_ARTICLES
        }

    @patch('requests.get')
    def test_fetch_articles_no_date(self, mock_get):
        """Test fetching articles with no date specified."""
        # Set up the mock response
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_get.return_value = mock_resp

        # Call the function
        result = fetch_articles(query="bitcoin")

        # Assertions
        # 1. requests.get was called once
        mock_get.assert_called_once()

        # 2. The returned object is a list of Article
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(a, Article) for a in result))

        # 3. The length matches top_k=10 default (but our mock only has 8)
        self.assertEqual(len(result), 8)

        # 4. Check a field in the first article
        self.assertEqual(result[0].title, MOCK_ARTICLES[0]['title'])
        self.assertEqual(result[0].author, MOCK_ARTICLES[0]['author'])

    @patch('requests.get')
    def test_fetch_articles_with_date(self, mock_get):
        """Test fetching articles with a specified date filter."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_get.return_value = mock_resp

        test_date = datetime(2025, 1, 10)  # e.g. Jan 10, 2025
        result = fetch_articles(query="bitcoin", date=test_date)

        # Verify the 'from' and 'to' query params in the request
        called_args, called_kwargs = mock_get.call_args
        params_sent = called_kwargs.get('params', {})
        self.assertIn('from', params_sent)
        self.assertIn('to', params_sent)

        # The 'from' should be one day prior
        self.assertEqual(params_sent['from'], (test_date - timedelta(days=1)).strftime('%Y-%m-%d'))
        self.assertEqual(params_sent['to'], test_date.strftime('%Y-%m-%d'))

        # Verify we still parse articles
        self.assertEqual(len(result), 8)

    @patch('requests.get')
    def test_fetch_articles_top_k(self, mock_get):
        """Test fetching articles with a smaller top_k parameter."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_get.return_value = mock_resp

        # Request fewer articles
        top_k = 3
        result = fetch_articles(query="bitcoin", top_k=top_k)

        # Should only return first 3
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].title, MOCK_ARTICLES[0]['title'])
        self.assertEqual(result[-1].title, MOCK_ARTICLES[2]['title'])

    @patch('requests.get')
    def test_fetch_articles_empty_response(self, mock_get):
        """Test fetching articles when the API returns no articles."""
        # Mock with an empty list of articles
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"articles": []}
        mock_get.return_value = mock_resp

        result = fetch_articles(query="bitcoin")

        self.assertEqual(len(result), 0, "Should return an empty list if no articles found.")

    @patch('requests.get')
    def test_fetch_articles_raise_for_status(self, mock_get):
        """Test that fetch_articles raises an HTTPError when the request fails."""
        mock_resp = MagicMock()
        # Configure raise_for_status to raise an HTTPError
        mock_resp.raise_for_status.side_effect = Exception("HTTP Error occurred")
        mock_get.return_value = mock_resp

        with self.assertRaises(Exception) as context:
            _ = fetch_articles(query="bitcoin")

        self.assertIn("HTTP Error occurred", str(context.exception))


if __name__ == '__main__':
    unittest.main()
