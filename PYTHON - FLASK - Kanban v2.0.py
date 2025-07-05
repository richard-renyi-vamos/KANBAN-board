from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
db = SQLAlchemy(app)

# Database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='To Do')

# Homepage with task lists
@app.route('/')
def index():
    tasks = Task.query.all()
    todo_tasks = [task for task in tasks if task.status == 'To Do']
    in_progress_tasks = [task for task in tasks if task.status == 'In Progress']
    done_tasks = [task for task in tasks if task.status == 'Done']
    return render_template('index.html', todo_tasks=todo_tasks, in_progress_tasks=in_progress_tasks, done_tasks=done_tasks)

# Add a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='To Do')
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Update a task's status
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    new_status = request.form.get('status')
    task.status = new_status
    db.session.commit()
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# 🔍 Search tasks by title
@app.route('/search')
def search():
    query = request.args.get('q', '')
    tasks = Task.query.filter(Task.title.contains(query)).all()
    return render_template('search_results.html', tasks=tasks, query=query)

# 📄 View task details
@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

# ✏️ Edit task title
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        new_title = request.form.get('title')
        if new_title:
            task.title = new_title
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

# 🔃 Toggle status (cycle through statuses)
@app.route('/toggle_status/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    next_status = {
        'To Do': 'In Progress',
        'In Progress': 'Done',
        'Done': 'To Do'
    }
    task.status = next_status.get(task.status, 'To Do')
    db.session.commit()
    return redirect(url_for('index'))

# 📦 Bulk delete all done tasks
@app.route('/clear_done', methods=['POST'])
def clear_done():
    Task.query.filter_by(status='Done').delete()
    db.session.commit()
    return redirect(url_for('index'))

# Run app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
