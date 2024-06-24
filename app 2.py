from flask import Flask, render_template, request, redirect, Response, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import nltk
from nltk.tokenize import word_tokenize
from run import chat_with_model
from run import recognize_speech

conv = "You are a helpful and joyous mental therapy assistant. Always answer as helpfully and cheerfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Also, don't mention your name or you being an AI or assistant or an app, anywhere ever. Also generate one response only. Keep the response brief and concise. Talk in a human manner. \n"
app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///maya.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100),  nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    chat_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('chats', lazy=True))

class ChatTranscript(db.Model):
    chat_transcript_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    chat = db.relationship('Chat', backref=db.backref('transcripts', lazy=True))

class Summary(db.Model):
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), primary_key = True)
    summary = db.Column(db.Text, nullable = False)
    chat = db.relationship('Chat', backref=db.backref('summary', lazy=True))

def extract_nouns(input_string):
    tokens = word_tokenize(input_string)
    tagged_tokens = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]
    result = ""

    for noun in nouns:
        result += noun + " "
    return input_string[:12]

inputStr = "" #To store first prompt of new chat

@app.route('/')
def home():
    #if 'user_id' in session:
        #return redirect('/chat')
    return render_template('home.html') 

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST' and (request.form['username'] and request.form['email'] and request.form['password']):
        username = request.form['username']
        email = request.form['email']
        password  = request.form['password']
        new_user = User(username = username, email = email, password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup2.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password  = request.form['password']

        user = User.query.filter_by(email = email).first()

        if user and user.check_password(password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            return redirect('/chat')
        else:
            # return render_template('login.html', error = 'Invalid User')
            "Invalid email or password"
    return render_template('login2.html')

@app.route('/chat', methods=['GET', 'POST'])
def chats():
    if 'user_id' in session:
        global inputStr
        user = User.query.filter_by(user_id=session['user_id']).first()
        user_chats = Chat.query.filter_by(user_id=user.user_id).order_by(Chat.chat_id.asc()).all()
        # See jFor in HTML
        if request.method == 'POST':
            input = request.form['input']
            inputStr = input
            name = extract_nouns(input)
            new_chat = Chat(user_id=user.user_id, chat_name=name)
            db.session.add(new_chat)
            db.session.commit()
            return redirect(f'/chat/{new_chat.chat_id}') #Link in all chats
        return render_template('chat.html', user = user, user_chats = user_chats) 
    else:
        return redirect('/login')

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def view_chat(chat_id):
    if 'user_id' in session:
        global inputStr
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        user_chats = Chat.query.filter_by(user_id=user.user_id).order_by(Chat.chat_id.asc()).all()
        
        chat = Chat.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        transcripts = ChatTranscript.query.filter_by(chat_id=chat_id).order_by(ChatTranscript.timestamp.asc()).all()
        
        if inputStr:
            input = inputStr
            inputStr = ""
            transcript_user = ChatTranscript(chat_id=chat_id, sender="user", message=input)
            db.session.add(transcript_user)
            db.session.commit()
            # API Call to ML Model
            output = chat_with_model(input, conv)
            transcript_model = ChatTranscript(chat_id=chat_id, sender="model", message=output)
            db.session.add(transcript_model)
            db.session.commit()
            return redirect(f'/chat/{chat_id}')
        
        elif request.method == 'POST':
            input = request.form['input']
            transcript_user = ChatTranscript(chat_id=chat_id, sender="user", message=input)
            db.session.add(transcript_user)
            db.session.commit()            
            inputStr = input
            return redirect(f'/chat/{chat_id}')
        
        return render_template('chat3.html', user=user, chat=chat, transcripts=transcripts, user_chats=user_chats)
    else:
        return redirect('/login')


@app.route('/summarize/<int:chat_id>', methods=['GET', 'POST'])
def summarize(chat_id):
    transcripts = ChatTranscript.query.filter_by(chat_id=chat_id).order_by(ChatTranscript.timestamp.asc()).all()
    str = ""
    for chat in transcripts:
        if chat.sender == "user":
            str += "User: " + chat.message + '\n'
        else:
            str += "Assistant: " + chat.message + '\n'
    # API call to model to generate summary
    summary = "Hello"
    new_summary = Summary(chat_id = chat_id, summary = summary)
    db.session.add(new_summary)
    db.session.commit()
    return render_template('summarize.html', summary = new_summary)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/delete/<int:chat_id>', methods=['GET', 'POST'])
def delete(chat_id):
    chat_summary = Summary.query.filter_by(chat_id=chat_id).first()
    chat_transcripts = ChatTranscript.query.filter_by(chat_id=chat_id).all()
    chat = Chat.query.filter_by(chat_id=chat_id).first()
    if chat_summary:
        db.session.delete(chat_summary)
    for transcript in chat_transcripts:
        db.session.delete(transcript)
    if chat:
        db.session.delete(chat)

    db.session.commit()
    return redirect('/chat')

@app.route('/mic/<int:chat_id>', methods=['GET', 'POST'])
def mic(chat_id):
    global inputStr
    inputStr = recognize_speech()
    return redirect(f'/chat/{chat_id}')

@app.route('/mic', methods=['GET', 'POST'])
def mic2():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        global inputStr
        inputStr = recognize_speech()
        name = extract_nouns(inputStr)
        new_chat = Chat(user_id=user.user_id, chat_name=name)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f'/chat/{new_chat.chat_id}')
    
@app.route('/default1', methods=['GET', 'POST'])
def default_input1():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        global inputStr
        inputStr = "Can you help me? I'm feeling stressed."
        input = inputStr
        name = extract_nouns(input)
        new_chat = Chat(user_id=user.user_id, chat_name=name)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f'/chat/{new_chat.chat_id}') #Link in all chats
    

@app.route('/default2', methods=['GET', 'POST'])
def default_input2():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        global inputStr
        inputStr = "I need someone to talk to. I am feeling confused."
        input = inputStr
        name = extract_nouns(input)
        new_chat = Chat(user_id=user.user_id, chat_name=name)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f'/chat/{new_chat.chat_id}') #Link in all chats
    
@app.route('/default3', methods=['GET', 'POST'])
def default_input3():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        global inputStr
        inputStr = "I feel like I'm on my own. I am feeling lonely."
        input = inputStr
        name = extract_nouns(input)
        new_chat = Chat(user_id=user.user_id, chat_name=name)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f'/chat/{new_chat.chat_id}') #Link in all chats
    
@app.route('/default4', methods=['GET', 'POST'])
def default_input4():
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).first()
        global inputStr
        inputStr = "I'm completely directionless.I am feeling lost."
        input = inputStr
        name = extract_nouns(input)
        new_chat = Chat(user_id=user.user_id, chat_name=name)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f'/chat/{new_chat.chat_id}') #Link in all chats


if __name__ == "__main__":
    app.run(debug = True)