from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='To Do')

@app.route('/')
def index():
    tasks = Task.query.all()
    todo_tasks = [task for task in tasks if task.status == 'To Do']
    in_progress_tasks = [task for task in tasks if task.status == 'In Progress']
    done_tasks = [task for task in tasks if task.status == 'Done']
    return render_template('index.html', todo_tasks=todo_tasks, in_progress_tasks=in_progress_tasks, done_tasks=done_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    new_task = Task(title=title, status='To Do')
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    new_status = request.form.get('status')
    task.status = new_status
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
