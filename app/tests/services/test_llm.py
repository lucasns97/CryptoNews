import unittest
from unittest.mock import patch
from src.services.llm import (
    generate_prompt,
    call_model,
    parse_response,
    analyze_news_with_llm,
)
from src.services.news import Article

###########
#  Tests  #
###########

class TestGeneratePrompt(unittest.TestCase):
    def test_generate_prompt_single_article(self):
        articles = [
            Article(
                title="Sample Title",
                description="Sample Description",
                content="Sample Content",
                publishedAt="2021-10-01",
            )
        ]
        prompt = generate_prompt(articles, "Bitcoin")
        self.assertIn("Bitcoin", prompt)
        self.assertIn("Sample Title", prompt)
        self.assertIn("Sample Content", prompt)
        self.assertIn('{"Reasoning":', prompt)

    def test_generate_prompt_multiple_articles(self):
        articles = [
            Article(
                title="Title 1",
                description="Desc 1",
                content="Content 1",
                publishedAt="2021-10-01",
            ),
            Article(
                title="Title 2",
                description="Desc 2",
                content="Content 2",
                publishedAt="2021-10-01",
            ),
        ]
        prompt = generate_prompt(articles, "Ethereum")
        self.assertIn("Ethereum", prompt)
        self.assertIn("Title 1", prompt)
        self.assertIn("Desc 2", prompt)
        self.assertIn('{"Reasoning":', prompt)


class TestCallModel(unittest.TestCase):
    def test_call_model(self):
        mock_response = unittest.mock.Mock()
        mock_response.choices = [
            unittest.mock.Mock(message=unittest.mock.Mock(content="Mocked response"))
        ]
        mock_llm_client = unittest.mock.Mock()
        mock_llm_client.chat.completions.create.return_value = mock_response

        result = call_model("Test prompt", mock_llm_client)
        self.assertEqual(result, "Mocked response")


class TestParseResponse(unittest.TestCase):
    def test_parse_response_valid_json(self):
        valid_json = (
            "```json\n"
            '{"Reasoning": "Test reason", "ValueWillDrop": true}\n'
            "```"
        )
        parsed = parse_response(valid_json)
        self.assertEqual(parsed["Reasoning"], "Test reason")
        self.assertTrue(parsed["ValueWillDrop"])

    def test_parse_response_invalid_json(self):
        invalid_json = (
            "```json\n"
            '{"Reasoning": "Test reason", "ValueWillDrop": true\n'
            "```"
        )
        with self.assertRaises(ValueError):
            parse_response(invalid_json)


class TestAnalyzeNewsWithLLM(unittest.TestCase):
    @patch(
        "src.services.llm.call_model",
        return_value=(
            "```json\n"
            '{"Reasoning": "Some explanation", "ValueWillDrop": false}\n'
            "```"
        ),
    )
    def test_analyze_news_with_llm(self, mock_call_model):
        articles = [
            Article(title="T", description="D", content="C", publishedAt="2021-10-01")
        ]
        result = analyze_news_with_llm(articles, "XRP")
        mock_call_model.assert_called_once()
        self.assertEqual(result["Reasoning"], "Some explanation")
        self.assertFalse(result["ValueWillDrop"])


if __name__ == "__main__":
    unittest.main()
