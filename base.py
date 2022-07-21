from turtle import title
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc 

app = Flask(__name__, template_folder="template")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable= False)
  

    def __repr__(self) -> str:
        return f"{self.srno}-{self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':

        title = (request.form['title'])
        todo=Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    # import pdb; pdb.set_trace()
    allTodo=Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "This is Products page !! "

@app.route("/update/<int:srno>", methods=['GET', 'POST'])
def update(srno):
    if request.method =='POST' :  
        title = (request.form['title'])
       
        todo=Todo.query.filter_by(srno=srno).first()
        todo.title=title
      
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(srno=srno).first()
    return render_template('update.html', todo=todo)

@app.route("/Delete/<int:srno>")
def delete(srno):
    todo=Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__" :
    app.run(debug=True, port=5000)