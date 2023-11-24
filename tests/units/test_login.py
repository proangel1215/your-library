from flask import Flask
import unittest
from flask_testing import TestCase
from app import create_app



def test_login_route(test_client):
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data
