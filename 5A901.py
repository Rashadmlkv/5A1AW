from flask import Flask, jsonify, request, render_template, redirect
import smtplib, ssl
from flask_sqlalchemy import SQLAlchemy
from models import Task
from models.Task import app, db



"""shows all tasks from db"""
@app.route("/")
def get_all(methods=["GET"]):
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


"""insert task"""
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    new_task = Task(title=title)
    db.create_all()
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'task added'})



"""marks task as completed"""
@app.route("/update/<int:id>")
def update(id):
    task = Task.query.get(id)
    task.complete = not task.complete
    db.session.commit()

    return jsonify({'message': 'task completed'})


"""finds a task by id"""
@app.route("/<int:id>")
def find(id):
    task = Task.query.get(id)
    if task:
        return render_template('task_detail.html', task=task)
    else:
        return f"Task with ID {id} not found.", 404


"""delete task"""
@app.route("/delete/<int:id>")
def delete(id, methods=["DELETE"]):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'task deleted'})



"""send mail"""
@app.route("/send-email/<int:id>")
def send_email(id, methods=["GET"]):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context) 
        server.ehlo()
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, 'sender@gmail.com', 'test')
        return jsonify({'message': 'email sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        server.quit()


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
