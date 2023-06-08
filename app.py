from flask import Flask, request, jsonify, make_response
from flask_mail import Message, Mail
from flask_cors import CORS, cross_origin
import mysql.connector
from datetime import datetime
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['APPCONFIGSECRETKEY']
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ["EMAIL_SENDER"]
app.config['MAIL_PASSWORD'] = os.environ["EMAIL_PASSWORD"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Mail after config setup
mail = Mail(app)

mydb = mysql.connector.connect(
    host=os.environ['MYSQLHOST'],
    user=os.environ['MYSQLUSER'],
    password=os.environ['MYSQLPASSWORD'],
    database=os.environ['MYSQLDATABASE']
)
cursor = mydb.cursor(buffered=True, dictionary=True)

get_blog_articles_query = """ 
SELECT * FROM blog_articles
"""

cursor.execute(get_blog_articles_query)
blog_articles = cursor.fetchall()


@app.route('/get-blogs', methods=['GET'])
@cross_origin(origins='https://pierregoaerv2.netlify.app/')
def get_blogs():
    return jsonify(blog_articles), 200


@app.route('/contact', methods=['POST', 'OPTIONS'])
# @cross_origin(origins='http://localhost:8000')
@cross_origin(origins='https://pierregoaerv2.netlify.app/')
def contact():
    # get contact form data
    form_data = request.get_json()
    name = form_data["name"]
    email = form_data["email"]
    message = form_data["message"]
    today = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    print(form_data)

    # update google sheet
    # contacts_worksheet = gsheet_file.worksheet("contacts")
    # worksheet_rows = len(contacts_worksheet.get_all_values())
    # new_data = [today, name, email, phone, service, timeframe, budget, message]
    # for col in range(1, len(new_data) + 1):
    #     contacts_worksheet.update_cell(worksheet_rows + 1, col, str(new_data[col - 1]))

    # send email notification
    # html = f"pierregoaer.com - New Message!<br>" \
    #        f"<br>" \
    #        f"Date : {today}<br>" \
    #        f"Nom : {name}<br>" \
    #        f"Email : {email}<br>" \
    #        f"Message : {message}<br><br>"
    # msg = Message(
    #     subject='pierregoaer.com - New Message!',
    #     html=html,
    #     sender=('Pierre Goaer', app.config['MAIL_USERNAME']),
    #     recipients=[os.environ["EMAIL_RECIPIENT"]]
    # )
    # mail.send(msg)
    response = jsonify(message="Message Sent")

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(response.headers, response.response, response.data)
    return response
    # return "success", 200


if __name__ == "__main__":
    # TODO: Select proper run for DEV or PROD
    app.run(port=3000, debug=True)
    # app.run(threaded=True)
