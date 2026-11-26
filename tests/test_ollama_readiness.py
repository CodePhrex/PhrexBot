import unittest
from unittest.mock import Mock
import requests
from ollama_readiness import readiness, URL

class ReadinessTests(unittest.TestCase):
    def test_listed_not_inference_verified(self):
        client = Mock()
        client.get.return_value.status_code = 200
        client.get.return_value.json.return_value = {'models': [{'name': 'llama3.2:latest'}]}
        result = readiness('llama3.2', client)
        self.assertEqual(result['state'], 'model_listed')
        self.assertFalse(result['inference_ready'])
        client.get.assert_called_once_with(URL, timeout=(2, 3), allow_redirects=False)

    def test_unavailable(self):
        client = Mock()
        client.get.side_effect = requests.ConnectionError()
        self.assertEqual(readiness('model', client)['state'], 'unavailable')

    def test_missing_and_disabled(self):
        client = Mock()
        client.get.return_value.status_code = 200
        client.get.return_value.json.return_value = {'models': []}
        self.assertEqual(readiness('model', client)['state'], 'model_missing')
        self.assertEqual(readiness('', client)['state'], 'disabled')
