from quiz import app
from quiz.main.routes import main
from quiz.users.routes import users
from quiz.quiz.routes import quiz


app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(quiz)
