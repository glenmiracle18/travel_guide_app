

from flask import Flask, render_template, request,redirect,session,session

import urllib

import requests

import pprint

import csv

import sys

import os



app = Flask(__name__)





@app.route('/')

def travel_home():

    # Returns the rendered template travel.html which is my home screen.

    return render_template("travel.html")



"""

car

"""



@app.route('/car_form')

def car_form():

    # Returns the rendered car_form.html which is my home screen.

    return render_template("car_form.html")





@app.route('/planner', methods=["GET","POST"])

def travel():


    if request.method == "GET": # verifies the request statement, to pull out the form



        return render_template('travel.html')



    elif request.method == "POST":



        start = request.form["startplace"]



        end = request.form["endplace"]





        status_code, results = perform_query(start, end)

        if status_code != 200:

            messeage = "Wrong Entry. Try Again"

            return render_template('car_form.html',m=messeage)



        pprint.pprint(results['routes'][0])





        return render_template('car_result.html',routes=results['routes'][0])









APP_ID = '',

APP_KEY = '',



def perform_query(start, end):



    journey_path_format = 'transportapi.com/v3/uk/car/journey/from/postcode:{}/to/postcode:{}.json'



    url_path = urllib.parse.quote(



        journey_path_format.format(start, end))



    params = {

        'nationalSearch': 'true',

        'app_id': APP_ID,

        'app_key': APP_KEY,

    }





    r = requests.get(

        'https://' + url_path, params=params, allow_redirects=False)

    ans = r.json()



    print(r.url)



    return r.status_code, ans

















"""""""""

cycle

"""""""""



@app.route('/cycle')

def cycle_form():

    # Returns the rendered template cycle_form.html which is my home screen.

    return render_template("cycle_form.html")





@app.route('/cycle_result', methods=["GET","POST"])

def cycle_result():



    if request.method == "GET":



        return render_template('travel.html')



    elif request.method == "POST":



        start = request.form["startplace"]



        end = request.form["endplace"]



        status_code, results=perform_query_cycle(start, end)

        if status_code != 200:

            messeage = "Wrong Entry. Try Again"

            return render_template('cycle_form.html', m=messeage)



        print(results)



        return render_template('cycle_result.html',routes=results['routes'][0])



APP_ID = '23b8cb3d',

APP_KEY = '5a881dfd810d7474b0446591e247c92a',



def perform_query_cycle(start, end):



    journey_path_format = 'transportapi.com/v3/uk/cycle/journey/from/postcode:{}/to/postcode:{}.json'



    url_path = urllib.parse.quote(



        journey_path_format.format(start, end))



    params = {

        'nationalSearch': 'true',

        'app_id': APP_ID,

        'app_key': APP_KEY,

    }





    r = requests.get(

        'https://' + url_path, params=params, allow_redirects=False)

    ans = r.json()



    print(r.url)



    return r.status_code, ans







"""""""""

Train

"""""""""



@app.route('/train')

def train():

    # Returns the rendered template travel.html which is my home screen.



    # #with open("station_codes.csv" ,'a') as f:

    # traincode=open("station_codes.csv",'r')

    # a=traincode.read('Station Name')

    # traincode.read('CRS Code')

    station_names = []

    with open('static/station_codes.csv', 'r') as f:

        reader = csv.reader(f)

        next(reader, None)

        for row in reader:

            station_name = row[0]

            station_code = row[1]



            station = {

                'station_name' : station_name,

                'station_code' : station_code,

            }



            station_names.append(station)

        print('Test start point 1')

        print(station_names)





    return render_template("train_form.html", station_names=station_names)



@app.route('/train_result', methods=["GET","POST"])

def train_result():



    if request.method == "GET":



        return render_template('travel.html')



    elif request.method == "POST":



        location = request.form["location"]

        print(location)



        date = request.form["date"]

        print(date)



        time = request.form["time"]

        status_code, results=perform_query_train(location, date,time)

        if status_code != 200:

            messeage = "Wrong Entry. Try Again Go Back And Try"

            return render_template('train_form.html', m=messeage)

    return render_template('train_result.html',routes=results)



APP_ID = '23b8cb3d',

APP_KEY = '5a881dfd810d7474b0446591e247c92a',



def perform_query_train(start,date,time):





    journey_path_format_train='transportapi.com/v3/uk/train/station/{}/{}/{}/timetable.json'



    url_path = urllib.parse.quote(



        journey_path_format_train.format(start,date,time))



    params = {

        'app_id': APP_ID,

        'app_key': APP_KEY,

    }





    r = requests.get(

        'https://' + url_path, params=params, allow_redirects=False)



    print(r)

    print(r.url)

    ans = r.json()



    return r.status_code, ans




@app.route('/weather', methods=["POST", "GET"])

def weather():

    if request.method == "POST":

        cityname = request.form['city']

        # r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + cityname + '&appid=5875a1fb51a659b3aa4807292e7d58c1')

        # json_object = r.json()

        # print(r.url)



        status_code, results = perform_weather(cityname)



        if status_code != 200:

            messeage = "Wrong Entry. Try Again"

            return render_template('weather.html', m=messeage)

        temprature_kelvin = float(results['main']['temp'])

        temprature_celcius = (temprature_kelvin - 273.15)

        temprature_celciu = round(temprature_celcius)

        return render_template('weather.html',temp=temprature_celciu)

    elif request.method == "GET":

        return render_template('weather.html')



def perform_weather(cityname):

    APP_ID = '5875a1fb51a659b3aa4807292e7d58c1',





    r =requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + cityname + '&appid=5875a1fb51a659b3aa4807292e7d58c1')

    #

    # params = {

    #     'app_id': APP_ID,

    # }

    #

    #

    # r = requests.get(

    #     'https://' + url_path, params=params, allow_redirects=False)



    print(r)

    ans = r.json()



    return r.status_code, ans







@app.route('/map')

def map():

    return render_template('map.html')



@app.route('/news', methods=["POST", "GET"])

def news():

    print('not crashed')

    r = requests.get(

        'https://newsapi.org/v2/top-headlines?country=gb&category=business&apiKey=05d58b80c80b454998b1af7c250f3493')

    news = r.json()

    print(news)

    return render_template('news.html', n=news["articles"] )


"""
sign_in page
"""

@app.route('/sign_in')
def sign_in():
    print("This is the sign_in and login page")
    return render_template('sign_in.html')


@app.route('/destinations')
def destinations():
    print("You might want to visit these destinations sometime")
    return render_template('destinations.html')

@app.route('/about_us')
def about_us():
    print("This is information about the developers of the app")
    return render_template('about_us.html')

@app.route('/feedback')
def feedback():
    """
    this is a form to submit feedback about the app
    """
    print("this is the feedback page")
    return render_template('feedback.html')

@app.route('/housing')
def accomodations():
    print("this is the accomodations page")
    return reder_template('housing.hmtl')




"""



A function is created called path.Which is used to read out the data for python  .

Station_code contatins all the code for the station.

"""


if __name__ == '__main__':

    app.run()
