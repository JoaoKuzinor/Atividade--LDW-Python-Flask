from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder="views")

app.secret_key = os.urandom(24)

routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    dir, "models/pais.sqlite3"
)

#Define pasta que receberá arquivos de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
#Define o tamanho máximo de um arquivo de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#Secret Key


# Inicia o servidor
if __name__ == "__main__":
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(host="localhost", port=4000, debug=True)
