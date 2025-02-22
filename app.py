from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootpassword'
app.config['MYSQL_DB'] = 'task_manager'

mysql = MySQL(app)

class TaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    submit = SubmitField('Add Task')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task_name = form.name.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks(name) VALUES (%s)", (task_name,))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html', form=form)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    
    if request.method == 'POST':
        task_name = request.form['name']
        cur.execute("UPDATE tasks SET name = %s WHERE id = %s", (task_name, task_id))
        mysql.connection.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
