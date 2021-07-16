from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json

class FlaskTests(TestCase):

    def test_home(self):
        """Ensure that the home page returns 200"""
        self.client = app.test_client()
        app.testing = True
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)



    def test_play(self):
        """Ensure that home page can select a game correctly"""
        self.client = app.test_client()
        app.testing = True

        with self.client:
            response = self.client.post('/play', data={'config': '5'})
            self.assertIn('board', session)
            self.assertIn('highscore', session)
            self.assertIn('score', session)
            self.assertIn('plays', session)

    def test_valid_word(self):
        """Test to see if a valid word exists on a predefined board"""
        self.client = app.test_client()
        app.testing = True

        with self.client.session_transaction() as s:
            s['board'] = [["R", "U", "N", "T"],["R", "U", "N", "T"],["R", "U", "N", "T"],["R", "U", "N", "T"]]
            s['score'] = 0
            s['plays'] = 0
            s['words'] = []
            s['highscore'] = {'score':0, 'plays':0}
        response = self.client.post('/add-word', json={"word":"RuN"}, content_type="application/json")
        self.assertEqual(json.loads(response.data)['message'], "ok")

