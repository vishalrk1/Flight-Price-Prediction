import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime as dt

## loading in trained model
model = joblib.load('Models/FlightPrice.pkl')

@st.cache()
def make_predictions(journey_date, journey_time, arrival_date, arrival_time, source, destination, stops, airline):
    # preprocessing data before predictions
    pred_input = []

    stops = int(stops)
    pred_input.append(stops)

    # departure Date
    journey_day = int(pd.to_datetime(journey_date, format="%Y-%m-%dT%H:%M").day)
    pred_input.append(journey_day)

    journey_month = int(pd.to_datetime(journey_date, format ="%Y-%m-%dT%H:%M").month)
    pred_input.append(journey_month)

    dep_min = int(journey_time.minute)
    pred_input.append(dep_min)

    dep_hour = int(journey_time.hour)
    pred_input.append(dep_hour)

    arrival_min = int(arrival_time.minute)
    pred_input.append(arrival_min)

    arrival_hour = int(arrival_time.hour)
    pred_input.append(arrival_hour)

    arrival_day = int(pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").day)
    pred_input.append(arrival_day)

    duration_min = abs(arrival_min - dep_min)
    pred_input.append(duration_min)

    duration_hour = abs(arrival_hour - dep_hour)
    pred_input.append(duration_hour)

    air_list = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia', 'Vistara Premium economy', 'Jet Airways Business', 'Multiple carriers Premium economy', 'Trujet']
    for a in air_list:
        if a == airline:
            pred_input.append(1)
        else:
            pred_input.append(0)

    src_list = ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
    for i in src_list:
        if i == source:
            pred_input.append(1)
        else:
            pred_input.append(0)

    dst_list = ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad']
    for d in dst_list:
        if d == destination:
            pred_input.append(1)
        else:
            pred_input.append(0)

    prediction = model.predict(np.array([pred_input]))

    return int(prediction)


def main():
    
    st.title('Flight Fair Price Predictor')
    st.subheader('Fill the following details to get the idea about flight fair price')

    col1, col2 = st.columns([2, 1])
    journey_date = col1.date_input('Journey Date')
    journey_time = col2.time_input('Departure time')

    col3, col4 = st.columns([2, 1])
    arrival_date = col3.date_input('Arroval Date')
    arrival_time = col4.time_input('Arrival time')

    col5, col6 = st.columns(2)
    source = col5.selectbox('Departure city',['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'])
    destination = col6.selectbox('Destination city', ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'])

    stops = st.selectbox('Total Stops', ['non-stop', 1, 2, 3, 4])

    airline = st.selectbox('Choose Airline', ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia', 'Vistara Premium economy', 'Jet Airways Business', 'Multiple carriers Premium economy', 'Trujet'])

    predict = st.button('Make Prediction',)

    if stops == 'non-stop':
        stops = 0
    
    # make prediction button logic
    if predict:
        with st.spinner('Wait for prediction....'):
            t = make_predictions(journey_date, journey_time, arrival_date, arrival_time, source, destination, stops, airline)
        st.success(f'Fair Price will be around Rs.{t}')

if __name__=='__main__': 
    main()
