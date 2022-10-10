from flask import Flask, render_template, request, redirect
app = Flask(__name__)
import csv
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

# Username is a parameter for the function hello_world
@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():

    if request.method == "POST":
        try:
            data = request.form.to_dict()
            print(data)
            send_an_email(data)
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'smth went wrong. Try again!'


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

def send_an_email(data):
    email = EmailMessage()
    email['from'] = data["email"]
    email['to'] = 'gaitanaru.iulia@gmail.com'
    email['subject'] = data["subject"]
    message = "Email Sender: " + email["from"] + "\nSubiect: "+ email["subject"] + "\nContent: " + data["message"]
    email.set_content(message)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('gaitanaru.iulia@gmail.com', 'xudzzhuqyzaqxwsl')
        smtp.send_message(email)
        print("Sent it!")