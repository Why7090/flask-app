import os
from datetime import datetime
from zipfile import ZipFile
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
import random, shutil


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def hello_person():
    return """
        <p>Who do you want me to say "Hi" to?</p>
        <form method="POST" action="%s"><input name="person" /><input type="submit" value="Go!" /></form>
        <a href="%s">ModCombiner</a>
        """ % (url_for('greet'), url_for('upload_files'))

@app.route('/greet', methods=['POST'])
def greet():
    greeting = random.choice(["Hiya", "Hallo", "Hola", "Ola", "Salut", "Привет", "こんにちは", "您好"])
    return """
        <p>%s, %s!</p>
        <p><a href="%s">Back to start</a></p>
        """ % (greeting, request.form["person"], url_for('hello_person'))



@app.route('/modcombiner', methods=['GET'])
def upload_files():
    return render_template("upload.html", link=url_for('combine_mods'))

@app.route('/modcombiner', methods=['POST'])
def combine_mods():
    if request.method == 'POST':
        try:
            f = request.files['mod0']
            f.save('tempmods/0.zip')
            f = request.files['mod1']
            f.save('tempmods/1.zip')

            shutil.rmtree('tempmods/0', ignore_errors=True)
            shutil.rmtree('tempmods/1', ignore_errors=True)
            with ZipFile('tempmods/0.zip', 'r') as f:
                f.extractall(path='tempmods/0')
            with ZipFile('tempmods/1.zip', 'r') as f:
                f.extractall(path='tempmods/1')

            open('tempmods/0.zip', 'w').close()
            open('tempmods/1.zip', 'w').close()
            return '<p>Success. <br><a href="{0}">Back to the upload page</a></p>'.format(url_for('upload_files'))
        except Exception as e:
            return 'An error was occured:<br/><br/><h1>500 - Internal Server Error</h1><br/>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.<br/><h4>'+repr(e)+'</h4>', 500


if __name__ == '__main__':
    app.run()
