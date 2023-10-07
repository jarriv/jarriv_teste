from flask import Flask
from flask_jsglue import JSGlue



app = Flask(__name__)
jsglue = JSGlue(app)




from app import routes


