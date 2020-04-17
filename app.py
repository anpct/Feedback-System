from flask import Flask, render_template, request, redirect, url_for, send_file
import json
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
json_file = open('static/questions.json', 'r')
q = json.load(json_file)
app.config["MONGO_URI"] = "************"
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html', msg=None)


@app.route('/alumni/<type>', methods=['GET', 'POST'])
def alumni(type):
    if type == 'FBA':
        dict_ques = q[q['alumni_feedback_FBA']]
    elif type == 'PEO':
        dict_ques = q[q['PEO']]
    else:
        dict_ques = q[q['PO']]
    if request.method == 'POST':
        t_dict={}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "alumni" + type
        t_dict['id'] = request.form['id']
        t_dict['name'] = request.form['name']
        t_dict['job'] = request.form['job']
        t_dict['address'] = request.form['address']
        t_dict['number'] = request.form['number']
        t_dict['advanced_degree'] = request.form['advanced_degree']
        t_dict['university_honors'] = request.form['university_honors']
        t_dict['employer_honors'] = request.form['employer_honors']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    return render_template('form.html', dict_ques=dict_ques, person='alumni')


@app.route('/employer/<type>', methods=['GET', 'POST'])
def employer(type):
    if type == 'PO':
        dict_ques = q[q['PO']]
    elif type == 'PEO':
        dict_ques = q[q['PEO']]
    elif type == 'FBEG':
        dict_ques = q[q['employer_feedback_FBEG']]
    else:
        dict_ques = q[q['employer_feedback_FBE']]
    if request.method == 'POST' and type != "FBE":
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "employer" + type
        t_dict['company'] = request.form['company']
        t_dict['name'] = request.form['name']
        t_dict['department'] = request.form['department']
        t_dict['designation'] = request.form['designation']
        t_dict['email'] = request.form['email']
        t_dict['number'] = request.form['number']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    if request.method == 'POST' and type == "FBE":
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "employer" + type
        t_dict['company'] = request.form['company']
        t_dict['name'] = request.form['name']
        t_dict['name_emp'] = request.form['namee']
        t_dict['designation'] = request.form['designation']
        t_dict['future'] = request.form['future']
        t_dict['improve'] = request.form['improve']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    return render_template('form.html', dict_ques=dict_ques, person='employer', type=type)


@app.route('/parents/<type>', methods=['GET', 'POST'])
def parents(type):
    if type == '1':
        dict_ques = q[q['parent_feedback']]
    elif type == 'PEO':
        dict_ques = q[q['PEO']]
    else:
        dict_ques = q[q['PO']]
    if request.method == 'POST':
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "parents" + type
        t_dict['id'] = request.form['id']
        t_dict['name'] = request.form['name']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    return render_template('form.html', dict_ques=dict_ques, person='parents')


@app.route('/students/<type>', methods=['GET', 'POST'])
def students(type):
    if type == 'SEFB':
        dict_ques = q[q['SEFB']]
    elif type == 'PEO':
        dict_ques = q[q['PEO']]
    elif type == 'PO':
        dict_ques = q[q['PO']]
    elif type == 'LAB':
        dict_ques = q[q['student_feedback_on_labs']]
    else:
        dict_ques = q[q['student_feedback_on_faculty']]
    if request.method == 'POST' and type != 'LAB':
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "students" + type
        t_dict['id'] = request.form['id']
        t_dict['name'] = request.form['name']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    if request.method == 'POST' and type == 'LAB':
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "students" + type
        t_dict['id'] = request.form['id']
        t_dict['name'] = request.form['name']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = [request.form["lab1"+str(i)], request.form["lab2"+str(i)], request.form["lab3"+str(i)], request.form["lab4"+str(i)]]
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    return render_template('form.html', dict_ques=dict_ques, person='students', type=type)


@app.route('/faculty', methods=['GET', 'POST'])
def faculty():
    dict_ques = q[q['faculty_feedback']]
    if request.method == 'POST':
        t_dict = {}
        t_dict['datetime'] = datetime.datetime.now()
        t_dict['feedback_name'] = "faculty"
        t_dict['years'] = request.form['years']
        t_dict['name'] = request.form['name']
        t_dict['comments'] = request.form['comments']
        t_dict['suggestions'] = request.form['suggestions']
        for i in dict_ques:
            t_dict[str(i).replace('.', '')] = float(request.form[i])
        mongo.db.feedback.insert_one(t_dict)
        return render_template('home.html', msg='DONE')
    return render_template('form.html', dict_ques=dict_ques, person='faculty')


@app.route('/download')
def downloadFile():
    path = "static/feedback_report.pdf"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
