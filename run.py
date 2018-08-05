from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config.update(
    SECRET_KEY = 'topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:qwerty@localhost/catlog_db',
    SQLALCHEMY_TRACK_MODIFICATION= False
                 )

db = SQLAlchemy(app)


#BASIC ROUTES
@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello Flask!'

@app.route('/new/')
def query_string(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_string(name='dheeraj'):
    return '<h1> hello there ! {} </h1>'.format(name)

#string
@app.route('/text/<string:name>')
def working_with_string(name):
    return '<h1> here is a string: ' + name + '</h1>'

@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1>the number you picked is:' + str(num) + '</h1>'

@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1>the sum is: {}'.format(num1 + num2) + '</h1>'

@app.route('/products/<float:num1>/<float:num2>')
def product_float(num1, num2):
    return '<h1>the product is: {}'.format(num1 * num2) + '</h1>'

@app.route('/watch')
def movies_2017():
    movies_list = ['harry potter',
                    'creed',
                    'seven pounds',
                    'john wick',
                    'infinity war']

    return render_template('movies.html', movies = movies_list, name ='Dheeraj')

#using templates
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

@app.route('/table')
def movies_plus():
    movies_dict = {'thor': 3.00,
                   'harry potter': 4.12,
                   'thor dark world': 2.15,
                   'oceans 11': 1.50,
                   'rio':2.00 }
    return render_template('table_data.html',
                            movies=movies_dict,
                            name = 'dheeraj' )

#filters
@app.route('/filters')
def filter_data():
    movies_dict = {'thor': 3.00,
                   'harry potter': 4.12,
                   'thor dark world': 2.15,
                   'oceans 11': 1.50,
                   'rio':2.00 }
    return render_template('filter_data.html', movies = movies_dict,name = None, film = 'daylight')

@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane dou':02.88,
                    'thor the dark world': 02.16,
                    'harry Potter': 03.00,
                    'race 3': 08.20,
                    'ram': 08.88,
                    'hobbit': 02.33,
                    'captain america':02.00
                    }

    return render_template('using_macro.html', movies = movies_dict)



class Publication(db.Model):

    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Name is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique= True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    #Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title,author,avg_rating,book_format,image,num_pages,pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
