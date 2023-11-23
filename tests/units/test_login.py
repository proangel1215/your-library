from flask import Flask
import unittest
from flask_testing import TestCase
from app import create_app

class TestBooksRoute(TestCase):

    def create_app(self):
        return create_app("config.TestingConfig")


    def test_login_route(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        assert b"login" in response.data
        
