from app import app
from app.main.routes import main
from app.users.routes import users
from app.quiz.routes import quiz


app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(quiz)
