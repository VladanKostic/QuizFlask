from flask_table import Table, Col

class FinishQuiz(Table):
    num_of_que = Col('Num of que:')
    num_of_que = Col('Num of que:')
    datum = Col('Datum radova:')
    opis_radova = Col('Opis radova:')
    iznos_radova = Col('Iznos radova:')

class ResultsSoFarQuiz(Table):
    id_quiz = Col('Id of the quiz:')
    datetima_of_create = Col('Time when quiz create:')
    datetima_of_start = Col('Time when quiz start:')
    datetima_of_end = Col('Time when quiz end:')
    number_of_question = Col('Percent of success:')
    number_of_true = Col('Percent of success:')
