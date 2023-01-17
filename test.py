from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_start_page(self):
        with app.test_client() as client:
            res = client.get('/boggle')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn( "<title>Boggle</title>", html)
            self.assertIn( "<div id='board'>", html)
            

    def test_word_submission(self):
        with app.test_client() as client:
            res0 = client.get('/boggle')
            res = client.post('/boggle/play', data={'word': 'notaword'})

            self.assertEqual(res.status_code, 200)
            self.assertIn(res.data['result'], 'not-word')

