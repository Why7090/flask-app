import os
from datetime import datetime
from zipfile import ZipFile
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
import random, shutil, combiner


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def hello_person():
    return """
        <p>Who do you want me to say "Hi" to?</p>
        <form method="POST" action="{0:s}"><input name="person" /><input type="submit" value="Go!" /></form>
        <a href="{1:s}">ModCombiner</a>
        """.format(url_for('greet'), url_for('upload_files'))


@app.route('/greet', methods=['POST'])
def greet():
    greeting = random.choice(["Hiya", "Hallo", "Hola", "Ola", "Salut", "Привет", "こんにちは", "您好"])
    return """
        <p>{0:s}, {1:s}!</p>
        <p><a href="{2:s}">Back to start</a></p>
        """.format(greeting, request.form["person"], url_for('hello_person'))


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
            shutil.rmtree('tempmods/out', ignore_errors=True)
            os.makedirs('tempmods/out', exist_ok=True)
            with ZipFile('tempmods/0.zip', 'r') as f:
                f.extractall(path='tempmods/0')
            with ZipFile('tempmods/1.zip', 'r') as f:
                f.extractall(path='tempmods/1')

            open('tempmods/0.zip', 'w').close()
            open('tempmods/1.zip', 'w').close()

            combiner.Sprites().run()

            return '<p>Success. <br><a href="{0}">Back to the upload page</a></p>'.format(url_for('upload_files'))

        except Exception as e:
            return '''<h1>500 - Internal Server Error</h1>
                    <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p><br/><br/>
                    <h4>An error has occured:</h4>
                    <h3>{0}</h3>'''.format(repr(e)), 500


@app.route('/<path:path>')
def static_file(path):
    if not os.path.exists('static/'+path):
        return '''<h1>404 - Not Found</h1><br/>
                  <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p><br/><h4>We have nothing here.<br/>
                  You may want to visit <a href={0}>{0}</a> or the <a href="/">Lobby</a></h4>.'''.format(url_for('static', filename=path)), 404
    else:
        return send_from_directory('static/', path)


if __name__ == '__main__':
    app.run()
