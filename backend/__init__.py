from flask import Flask
import flask_assets as assets
import os
import sass

root=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app=Flask(__name__, root_path=root)
app.config.from_object('backend.settings')

from backend import controller
