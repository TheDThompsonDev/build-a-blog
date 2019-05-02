from flask import Flask, render_template, redirect, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.secret_key = "y337kGcys&zP3B"
db = SQLAlchemy(app)

############################## Class Objects ##############################
class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

############################## Login Page ##############################
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect ('/')
        else:
            return '<h1>Error!</h1>'

    return render_template('login.html')

############################## Register Page ##############################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return '<h1>Duplicate user</h1>'
    return render_template('register.html')

############################## Logout ##############################
@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')
############################## Main Page ##############################
    
@app.route('/', methods=['POST', 'GET'])
def index():
    post_id = request.args.get('id')
    title = 'Build a Blog'
    posts = [] #list for posts
    if post_id:
        posts = Blog.query.filter_by(id=post_id).all() #search for post by id
        title = Blog.title 
        return render_template('post.html', title = title, posts = posts, id = id) 
    return redirect('/blog') 

############################## Blog ##############################
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #returns and displays all the blog posts
    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)

############################## New Post ##############################
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ''
    text_error = ''
    #if it is a post method, it grabs the title and body 
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title_error = 'You need to have a title!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)
        if not body:
            text_error = 'You need to add content!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)
        #checks to see if there is a title and body 
        new_post = Blog(title, body)
        posts = [new_post]
        
        title = new_post.title
        body = new_post.body
        #adds and commits the new post to the database
        db.session.add(new_post)
        db.session.commit()

        return render_template('post.html', title = title, body=body, posts = posts)
    return render_template('newpost.html', title_error = title_error, text_error = text_error)
if __name__ == '__main__':
    app.run()
