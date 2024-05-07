#'#!/usr/bin/env python3
import streamlit as st


def save_log(log_text):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as file:
        file.write(f"{timestamp}: {log_text}\n")

def load_logs():
    from datetime import datetime
    try:
        with open("logs.txt", "r") as file:
            logs = file.readlines()
            return logs
    except FileNotFoundError:
        return []

def clear_logs():
    with open("logs.txt", "w") as file:
        file.truncate(0)

def load_alarms():
    from datetime import datetime
    try:
        with open("alarms.txt", "r") as file:
            logs = file.readlines()
            return logs
    except FileNotFoundError:
        return []

def clear_alarms():
    with open("alarms.txt", "w") as file:
        file.truncate(0)

def load_sensor_data():
    import csv
    data = []
    with open('sensor_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Extract timestamp from the first column
            timestamp_str = row[0]
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y %H:%M')
            # Extract sensor values from the remaining columns
            sensor_values = [float(value) for value in row[1:]]
            # Append timestamp and sensor values to data list
            data.append((timestamp, *sensor_values))
    return data

def load_ph_values():
    data = []
    with open('pH_values.txt', 'r') as file:
        for line in file:
            data.append(float(line.strip()))
    return data

def load_EC_values():
    data = []
    with open('EC_values.txt', 'r') as file:
        for line in file:
            data.append(float(line.strip()))
    return data

def data_plots():
    import time
    import pandas as pd
    import datetime
    import numpy as np
    import altair as alt
    import random


    st.markdown(f'# {list(page_names_to_funcs.keys())[0]}')  
    
    ec_flag = "False"
    dosing_flag,ec_flag,ph_flag = load_flags()
    measure_ec_clicked = st.button("Measure EC")
    if measure_ec_clicked:
        ec_flag = "True"
        ph_flag = "False"
        save_flags(ec_flag=ec_flag,pH_flag=ph_flag)
        with st.spinner('Measuring EC...'):
            while ec_flag == "True":
                time.sleep(1)
                dosing_flag,ec_flag,ph_flag = load_flags()
        if ec_flag == "False":
            st.success("EC measuring sequence finished.")
            st.rerun()
    
    st.write("Last recorded EC values:")
    loaded_EC_data  = load_EC_values()
    data = pd.DataFrame({
        'sample no': list(range(1, 11)),
        'EC(mS)': loaded_EC_data
        })    
        
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='sample no',
        y='EC(mS)'
    ).properties(
        width=500,
        height=400
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='sample no',
        y='EC(mS)'
    ).properties(
        width=500,
        height=400
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)

    
    st.write("")

    ph_flag = "False"
    dosing_flag,ec_flag,ph_flag = load_flags()
    measure_pH_clicked = st.button("Measure pH")
    if measure_pH_clicked:
        ec_flag = "False"
        ph_flag = "True"
        save_flags(ec_flag=ec_flag,pH_flag=ph_flag)
        with st.spinner('Measuring pH...'):
            while ph_flag == "True":
                time.sleep(1)
                dosing_flag,ec_flag,ph_flag = load_flags()
        if ph_flag == "False":
            st.success("pH measuring sequence finished.")
            st.rerun()
    
    st.write("Last recorded pH values:")
    #display water temperature chart
    loaded_pH_data  = load_ph_values()
    data = pd.DataFrame({
        'sample no': list(range(1, 101)),
        'pH': loaded_pH_data
        })    
        
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='sample no',
        y='pH'
    ).properties(
        width=500,
        height=400
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='sample no',
        y='pH'
    ).properties(
        width=500,
        height=400
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)

    
    st.write("")

    st.write("Co2 concentration:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()

    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Co2 (ppm)': [entry[1] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Co2 (ppm)'
    ).properties(
        width=500,
        height=500
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Co2 (ppm)'
    ).properties(
        width=500,
        height=500
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Air temperetarue (bme280):")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Air temperature (°C)': [entry[2] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Relative humidity:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Humidity (%)': [entry[3] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Humidity (%)'
    ).properties(
        width=500,
        height=500
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Humidity (%)'
    ).properties(
        width=500,
        height=500
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("VOC index:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'VOC index': [entry[4] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='VOC index'
    ).properties(
        width=500,
        height=500
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='VOC index'
    ).properties(
        width=500,
        height=500
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Water tank water level:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Water level': [entry[5] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Water level'
    ).properties(
        width=500,
        height=160
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Water level'
    ).properties(
        width=500,
        height=160
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Nutrients level:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Nutrients level': [entry[6] for entry in sensor_data]
        })
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Nutrients level'
    ).properties(
        width=500,
        height=160
    )
    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Nutrients level'
    ).properties(
        width=500,
        height=160
    )
    # Combine the line and points into a layered chart
    chart = (line + points).interactive()
    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Water temperature:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Water temperature (°C)': [entry[7] for entry in sensor_data]
        })
    
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Water temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Water temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    # Combine the line and points into a layered chart
    chart = (line + points).interactive()

    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Air temperature:")
    #display air temperature chart
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Air temperature (°C)': [entry[8] for entry in sensor_data]
        })
    
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500,
    )

    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    # Combine the line and points into a layered chart
    chart = (line + points).interactive()

    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.button("Refresh data plots")


def load_last_button_press_time():
    import json
    import datetime
    try:
        with open("last_button_press_time.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {"last_press_time": "2024-1-1 1:1:1","dosing_frequency": 14}

def save_last_button_press_time(newValues):
    import json
    import datetime
    with open("last_button_press_time.json", "w") as file:
        json.dump({"last_press_time": newValues["last_press_time"].strftime("%Y-%m-%d %H:%M:%S"), "dosing_frequency": newValues["dosing_frequency"]}, file)

import json
from datetime import datetime, timedelta

default_slider_values = {
    "roots_start": 0,
    "roots_end": 13,
    "leaves_start": 13,
    "leaves_end": 25,
    "growing_start": 25,
    "growing_end": 68,
    "preflowering_start": 68,
    "preflowering_end": 90,
    "flowering_start": 90,
    "flowering_end": 122,
    "ripening_start": 122,
    "ripening_end": 148
}

default_timer_values = {
    "lights_on_timer1": 5, 
    "lights_off_timer1": 23, 
    "lights_on_timer2": 5, 
    "lights_off_timer3": 23, 
    "ventilators_on_timer": 15, 
    "pump_on_timer": 50, 
    "compressor_on_timer": 45
}

def load_timer_values():
    try:
        with open("timer_values.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_timer_values

def save_progress(value):
    with open("progress.json","w") as file:
        json.dump(value,file)

def load_progress():
    try:
        with open("progress.json","r") as file:
            return json.load(file)
    except (FileNotFoundError):
        return 0
    
def save_dosage_size(value):
    with open("dosage_size.json","w") as file:
        json.dump(value,file)

def load_dosage_size():
    try:
        with open("dosage_size.json","r") as file:
            return json.load(file)
    except (FileNotFoundError):
        return 0

def save_flags(dosing_flag="False",ec_flag="False",pH_flag="False"):
    if (dosing_flag == "True" and ec_flag == "True") or (dosing_flag == "True"  and pH_flag == "True" ) or (ec_flag == "True"  and pH_flag == "True" ):
        flags = ["False", "False", "False"]
    else:
        flags = [dosing_flag, ec_flag, pH_flag]  
    
    with open("flags.txt", "w") as file:
        for flag in flags:
            file.write(str(flag) + "\n")

def load_flags():
    try:
        with open("flags.txt", "r") as file:
            lines = file.readlines()
            flags = [(line.strip()) for line in lines]
            return flags[0], flags[1], flags[2]  #list
    except FileNotFoundError:
        return "False", "False", "False"

def save_timer_values(values):
    with open("timer_values.json", "w") as file:
        json.dump(values, file)

def load_slider_values():
    try:
        with open("slider_values.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_slider_values  

def save_slider_values(values):
    with open("slider_values.json", "w") as file:
        json.dump(values, file)

def save_planting_date(date):
    with open("planting_date.json", "w") as file:
        json.dump(date.strftime("%Y-%m-%d"), file)

def load_planting_date():
    try:
        with open("planting_date.json", "r") as file:
            return datetime.strptime(json.load(file), "%Y-%m-%d")
    except FileNotFoundError:
        return None  

def save_button_states(states):
    with open("button_states.json", "w") as file:
        json.dump(states, file)

def load_button_states():
    try:
        with open("button_states.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("error loading button states")
        return {"Selected Mode": "Manual", "Selected Stage": "1st roots\ud83e\udd54", "Turn On Light1": false, "Power output1": 90, "Turn On Light2": false, "Power output2": 90, "Turn On Ventilators": false, "Turn On Water Pump": false, "Turn On Air Pump": false, "Set Temperature": 25}

def displayProgress(progressValue):
    if  progressValue > 1.0:
        progressValue = 1
        progressRoots = st.progress(100) #progress bar
    elif progressValue < 0.0:
        progressValue = 0
        progressRoots = st.progress(0)
    else:
        progressRoots = st.progress(progressValue) 
    st.write("Stage progress: "+f':blue[{progressValue*100:.2f}%]' )

def calculate_average_values(input_dict):
    sum_values = {}
    count = len(input_dict)
    for stage, values in input_dict.items():
        for key, value in values.items():
            if key not in sum_values:
                sum_values[key] = value #doesn't exist yet, create
            else:
                sum_values[key] += value#add to value

    for key in sum_values:
        sum_values[key] = sum_values[key]/count#calc mean 
    
    return sum_values

def controls():
    import pandas as pd
    import altair as alt
    import numpy as np
    import datetime
    import time

    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
    """
            This page allows the user to modify the controls and settings
    """
    )
    mode_options = ["Auto", "Manual"]

    button_states = load_button_states() 
    if button_states["Selected Mode"]=="Auto":
        selected_mode = 0
    else:
        selected_mode = 1

    #radio select mode
    button_states["Selected Mode"] = st.sidebar.radio("Select Mode", mode_options, selected_mode,horizontal=True)
    save_button_states(button_states)
    if button_states["Selected Mode"]=="Auto" and selected_mode == 1:
        st.rerun()
    elif button_states["Selected Mode"]=="Manual" and selected_mode == 0:
        st.rerun()
    

    planting_date = load_planting_date()

    stages = {
        "1st roots🥔": {},
        "1st true leaves 🌱": {},
        "growing 🥦": {},
        "preflowering🌿": {},
        "flowering🌸": {},
        "ripening🍒": {},
        "cleaning🧹": {}
    }

    stageValues = {
        "1st roots": {"Grow(ml/l)": 0.5, "Micro(ml/l)":0.5, "Bloom(ml/l)": 0.5, "ECmin(mS)": 0.3, "ECmax(mS)": 0.6},
        "1st true leaves": {"Grow(ml/l)": 1.0, "Micro(ml/l)":1.0, "Bloom(ml/l)": 1.0, "ECmin(mS)": 0.8, "ECmax(mS)": 1.2},
        "growing": {"Grow(ml/l)": 1.8, "Micro(ml/l)":1.2, "Bloom(ml/l)": 0.6, "ECmin(mS)": 1.3, "ECmax(mS)": 1.8},
        "preflowering": {"Grow(ml/l)": 2.0, "Micro(ml/l)":2.0, "Bloom(ml/l)": 1.5, "ECmin(mS)": 1.8, "ECmax(mS)": 2.0},
        "flowering": {"Grow(ml/l)": 0.8, "Micro(ml/l)":1.6, "Bloom(ml/l)": 2.4, "ECmin(mS)": 1.4, "ECmax(mS)": 2.2},
        "ripening": {"Grow(ml/l)": 0.6, "Micro(ml/l)": 1.2, "Bloom(ml/l)": 1.8, "ECmin(mS)": 1.4, "ECmax(mS)": 2.6},
        "cleaning": {"Grow(ml/l)": 0, "Micro(ml/l)": 0, "Bloom(ml/l)": 0, "ECmin(mS)": 0, "ECmax(mS)": 2.6}
    }
    
    active_stages = {}

    if button_states["Selected Mode"] == "Manual":
        save_button_states(button_states)
        #select stage radio button
        selected_stage = st.sidebar.radio("Select Stage", list(stages.keys()))
        button_states["Selected Stage"] = selected_stage
        save_button_states(button_states)
        
        # Stage progress
        st.write(f"## {selected_stage}")
        #progress slider
        estimatedProgress=st.slider("Estimated progress(%)", max_value = 100, value=load_progress())
        save_progress(estimatedProgress)
        dosage_size = st.slider("Dosage size(%)", max_value = 200, value = load_dosage_size())
        save_dosage_size(dosage_size)
        #y=y1​+(x(i)−x1​)*(​y2​−y1​)/(x2​−x1)


        next_stage_index = (list(stages.keys()).index(selected_stage) + 1) % (len(stages))
        selected_stage_index = next_stage_index-1
        selected_stage_name = list(stageValues.keys())[selected_stage_index]
        next_stage_name = list(stageValues.keys())[next_stage_index]
        next_stage_values = stageValues[next_stage_name]
        for key, value1 in stageValues[selected_stage_name].items():
            if key in next_stage_values:
                if selected_stage_name == "cleaning":
                    value2 = 0
                else:
                    value2 = next_stage_values[key]
            st.write(f"- {key}: {(float(value1)+(estimatedProgress)*(float(value2)-float(value1))/(100))*dosage_size/100:.2f}")


        st.write("Last measured EC values:")
        loaded_EC_values = load_EC_values()
        data = pd.DataFrame({
            'sample no': list(range(1, 11)),
            'EC(mS)': loaded_EC_values
            })
        
        # Create Altair chart
        line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
            x='sample no',
            y='EC(mS)'
        ).properties(
            width=500,
            height=300
        )

        points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
            x='sample no',
            y='EC(mS)'
        ).properties(
            width=500,
            height=300
        )

        # Combine the line and points into a layered chart
        chart = (line + points).interactive()

        # Add axis labels
        chart = chart.configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        ).configure_legend(
            labelFontSize=12
        )
        st.altair_chart(chart, use_container_width=True)
        last_button_press_time = load_last_button_press_time()


        dosing_flag,ec_flag,ph_flag = load_flags()
        start_dosing_clicked = st.button("Start dosing")
        if start_dosing_clicked:
            dosing_flag = "True"
            save_flags(dosing_flag="True")  # Set dosing flag to True
            current_time = datetime.datetime.now()
            save_last_button_press_time({"last_press_time": current_time,"dosing_frequency":last_button_press_time["dosing_frequency"]})
            save_progress(estimatedProgress)
            #st.info(f"In Progress... (saving new date: {current_time.strftime('%Y-%m-%d %H:%M:%S')})")
            with st.spinner(f"Dosing in progress..."):
                while dosing_flag == "True":
                    time.sleep(1)
                    dosing_flag,ec_flag,ph_flag = load_flags()
            st.success("Dosing sequence finished.") 
        elif last_button_press_time is not None:
            lastButtonPressTime = last_button_press_time["last_press_time"]
            st.write(f"Last balanced: {lastButtonPressTime}")


        st.write(f"## Light 1 💡")
        powerOutput1 = st.slider("Power output (%)", min_value=0, max_value=100, value=button_states["Power output1"], key=0)
        if button_states["Turn On Light1"]:
            if st.button("Turn Off Light 1"):
                button_states["Turn On Light1"] = False
                button_states["Power output1"] = powerOutput1
                st.success("Light 1 turned off!")
                save_button_states(button_states)
                st.rerun()
        else:
            if st.button("Turn On Light 1"):
                button_states["Turn On Light1"] = True
                button_states["Power output1"] = powerOutput1
                st.success("Lights turned on!")
                save_button_states(button_states)
                st.rerun()

        st.write(f"## Light 2 💡")
        powerOutput2 = st.slider("Power output (%)", min_value=0, max_value=100, value=button_states["Power output2"], key=1)

        if button_states["Turn On Light2"]:
            if st.button("Turn Off Light 2"):
                button_states["Turn On Light2"] = False
                button_states["Power output2"] = powerOutput2
                st.success("Light 2 turned off!")
                save_button_states(button_states)
                st.rerun()
        else:
            if st.button("Turn On Light 2"):
                button_states["Turn On Light2"] = True
                button_states["Power output2"] = powerOutput2
                st.success("Lights turned on!")
                save_button_states(button_states)
                st.rerun()

        st.write(f"## Ventilating 🌀")
        if button_states["Turn On Ventilators"]:
            if st.button("Turn Off Ventilators"):
                button_states["Turn On Ventilators"] = False
                st.success("Ventilators turned off!")
                save_button_states(button_states)
                st.rerun()
        else:
            if st.button("Turn On Ventilators"):
                button_states["Turn On Ventilators"] = True
                st.success("Ventilators turned on!")
                save_button_states(button_states)
                st.rerun()

        st.write(f"## Water pump 💧")
        if button_states["Turn On Water Pump"]:
            if st.button("Turn Off Water Pump"):
                button_states["Turn On Water Pump"] = False
                st.success("Water Pump turned off!")
                save_button_states(button_states)
                st.rerun()
        else:
            if st.button("Turn On Water Pump"):
                button_states["Turn On Water Pump"] = True
                st.success("Water Pump turned on!")
                save_button_states(button_states)
                st.rerun()

        st.write(f"## Air pump 🫧")
        if button_states["Turn On Air Pump"]:
            if st.button("Turn Off Air Pump"):
                button_states["Turn On Air Pump"] = False
                st.success("Air Pump turned off!")
                save_button_states(button_states)
                st.rerun()
        else:
            if st.button("Turn On Air Pump"):
                button_states["Turn On Air Pump"] = True
                st.success("Air Pump turned on!")
                save_button_states(button_states)
                st.rerun()
        

    if button_states["Selected Mode"]  == "Auto":
        
        save_button_states(button_states)

        selected_date = st.date_input("Date of seed starting", value=planting_date)

        if st.button("Set the date"):
            save_planting_date(selected_date)
            st.success("Planting date set successfully!")
            st.rerun()
            

        # Elapsed days
        if planting_date:
            elapsed_days = (datetime.datetime.now() - planting_date).days
            
        else:
            st.warning("Please set the planting date.")
            elapsed_days = 0

        # Stage sliders
        slider_values = load_slider_values()
        timer_values = load_timer_values()
        roots_start = slider_values.get("roots_start", 0)
        roots_end = slider_values.get("roots_end", 13)
        leaves_start, leaves_end = slider_values.get("leaves_start", 13), slider_values.get("leaves_end", 25)
        growing_start, growing_end = slider_values.get("growing_start", 25), slider_values.get("growing_end", 68)
        preflowering_start, preflowering_end = slider_values.get("preflowering_start", 68), slider_values.get("preflowering_end", 90)
        flowering_start, flowering_end = slider_values.get("flowering_start", 90), slider_values.get("flowering_end", 122)
        ripening_start, ripening_end = slider_values.get("ripening_start", 122), slider_values.get("ripening_end", 148)

        stageKeys=list(stages.keys())
        

        # Display active stages
        progressValue = (elapsed_days-roots_start)/(roots_end-roots_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[0]}")
            displayProgress(progressValue)
            y1 = stageValues['1st roots']
            y2 = stageValues['1st true leaves']
            interpolated_values = {}
            for key in y1:
                interpolated_values[key] = y1[key] + progressValue * (y2[key] - y1[key])
            active_stages['1st roots'] = interpolated_values



        progressValue = (elapsed_days-leaves_start)/(leaves_end-leaves_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[1]}")
            displayProgress(progressValue)
            y1 = stageValues['1st true leaves']
            y2 = stageValues['growing']
            interpolated_values = {}
            for key in y1:
                interpolated_values[key] = y1[key] + progressValue * (y2[key] - y1[key])
            active_stages['1st true leaves'] = interpolated_values


        progressValue = (elapsed_days-growing_start)/(growing_end-growing_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[2]}")
            displayProgress(progressValue)
            y1 = stageValues['growing']
            y2 = stageValues['preflowering']
            interpolated_values = {}
            for key in y1:
                interpolated_values[key] = y1[key] + progressValue * (y2[key] - y1[key])
            active_stages['growing'] = interpolated_values


        progressValue = (elapsed_days-preflowering_start)/(preflowering_end-preflowering_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[3]}")
            displayProgress(progressValue)
            y1 = stageValues['preflowering']
            y2 = stageValues['flowering']
            interpolated_values = {}
            for key in y1:
                interpolated_values[key] = y1[key] + progressValue * (y2[key] - y1[key])
            active_stages['preflowering'] = interpolated_values
        
        progressValue = (elapsed_days-flowering_start)/(flowering_end-flowering_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[4]}")
            displayProgress(progressValue)
            y1 = stageValues['flowering']
            y2 = stageValues['ripening']

            interpolated_values = {}
            for key in y1:
                interpolated_values[key] = y1[key] + progressValue * (y2[key] - y1[key])
            active_stages['flowering'] = interpolated_values

        progressValue = (elapsed_days-ripening_start)/(ripening_end-ripening_start)
        if progressValue > 0 and progressValue < 1:
            st.write(f"### {stageKeys[5]}")
            displayProgress(progressValue)
            y1 = stageValues['ripening']
            interpolated_values = {}
            for key in y1:
                if key ==  'ECmin(mS)':
                    interpolated_values[key] = y1[key] - 0.7*progressValue * (y1[key])
                elif key == 'ECmax(mS)':
                    interpolated_values[key] = y1[key] - 0.1*progressValue * (y1[key])
                else:
                    interpolated_values[key] = y1[key] - 0.6*progressValue * (y1[key])
            active_stages['ripening'] = interpolated_values
            
        if active_stages == {}:
            active_values = stageValues['cleaning']
        else:
            active_values = calculate_average_values(active_stages)
        active_stages.clear()

        st.write(f"### Intervals settings (days)")
        st.write(f"Elapsed days: :blue[{elapsed_days}]")

        #stage settings sliders
        roots_start, roots_end = st.slider(f"{stageKeys[0]}", min_value=0, max_value=250, value=(slider_values.get("roots_start", 0), slider_values.get("roots_end", 13)))
        leaves_start, leaves_end = st.slider(f"{stageKeys[1]}", min_value=0, max_value=250, value=(slider_values.get("leaves_start", 13), slider_values.get("leaves_end", 25)))
        growing_start, growing_end = st.slider(f"{stageKeys[2]}", min_value=0, max_value=250, value=(slider_values.get("growing_start", 25), slider_values.get("growing_end", 68)))
        preflowering_start, preflowering_end = st.slider(f"{stageKeys[3]}", min_value=0, max_value=250, value=(slider_values.get("preflowering_start", 68), slider_values.get("preflowering_end", 90)))
        flowering_start, flowering_end = st.slider(f"{stageKeys[4]}", min_value=0, max_value=250, value=(slider_values.get("flowering_start", 90), slider_values.get("flowering_end", 122)))
        ripening_start, ripening_end = st.slider(f"{stageKeys[5]}", min_value=0, max_value=250, value=(slider_values.get("ripening_start", 122), slider_values.get("ripening_end", 148)))
                        
        #save button
        if st.button("Save new intervals"):
            if roots_end > leaves_end or leaves_end > growing_end or growing_end > preflowering_end or preflowering_end > flowering_end or flowering_end > ripening_end:
                st.error("The sequence of stage ends must not be changed up")
            elif roots_start > leaves_start or leaves_start > growing_start or growing_start > preflowering_start or preflowering_start > flowering_start or flowering_start > ripening_start:
                st.error("The sequence of stage starts must not be changed up")
            else:
                slider_values = {
                "roots_start": roots_start,
                "roots_end": roots_end,
                "leaves_start": leaves_start,
                "leaves_end": leaves_end,
                "growing_start": growing_start,
                "growing_end": growing_end,
                "preflowering_start": preflowering_start,
                "preflowering_end": preflowering_end,
                "flowering_start": flowering_start,
                "flowering_end": flowering_end,
                "ripening_start": ripening_start,
                "ripening_end": ripening_end,
                }
                
                
                save_slider_values(slider_values)
                st.success("The new stage intervals were succesfully changed")
            st.rerun()

        
        last_refill = load_last_button_press_time()
        st.write(f"## Nutrient dosing 🧪")
        dosing_frequency = st.slider("Set the frequency of nutrition supplementation (days)", min_value=5, max_value=30, value=last_refill["dosing_frequency"])
        current_date = datetime.datetime.now()
        datetime_obj = datetime.datetime.strptime(last_refill["last_press_time"], "%Y-%m-%d %H:%M:%S")
        hours_until_next_dosage = (int(current_date.strftime("%H")) - int(datetime_obj.hour))
        days_until_next_dosage = (datetime_obj + timedelta(days=dosing_frequency) - current_date).days
        if days_until_next_dosage >1:
            st.write(f":violet[{days_until_next_dosage} days] until the scheduled dosing")
        elif days_until_next_dosage == 1:
            st.write(f":red[1 day] and :red[{hours_until_next_dosage} hour(s)] until the scheduled dosing !")
        elif days_until_next_dosage == 0:
            st.write(f"Nutrient dosing in :red[{hours_until_next_dosage} hour(s)] !!!")
        else:
            st.write(f":violet[{days_until_next_dosage} days] until the scheduled dosing")
            st.warning(f"Resetting the dosing frequency to :blue[{dosing_frequency} days] will trigger a nutrient dosing procedure soon!", icon="🚨")
            #st.write(f"Setting :blue[{dosing_frequency}] as a new dosing frequency will trigger a nutrient refill procedure soon!")
        if st.button("Set new dosing frequency"):
            newValues = {"last_press_time": datetime_obj, "dosing_frequency": dosing_frequency}
            save_last_button_press_time(newValues)
            st.success(f"The dosing frequency was set to :blue[{dosing_frequency} days]")
        

        st.write(f"## Light 1 💡")
        on_timer1, off_timer1 = st.slider("Set On and Off Timers (h)",
                                min_value=0, max_value=24, value=(timer_values["lights_on_timer1"], timer_values["lights_off_timer1"]), key=0)
        #on off timers
        st.write(f":blue[{off_timer1-on_timer1}] hours lights"+f" :orange[on] per day")

        st.write(f"## Light 2 💡")
        on_timer2, off_timer2 = st.slider("Set On and Off Timers (h)",
                                min_value=0, max_value=24, value=(timer_values["lights_on_timer2"], timer_values["lights_off_timer2"]), key=1)
        #on off timers
        st.write(f":blue[{off_timer2-on_timer2}] hours lights"+f" :orange[on] per day")

        st.write(f"## Timers ⏲️")
        st.write("Set the power on cycle lengths in minutes")
        ventilators_on_timer = st.slider("Ventilators On ratio (min/h)",
                                min_value=0, max_value=60, value=(timer_values["ventilators_on_timer"]))

        pump_on_timer = st.slider("Water pump On ratio (min/h)",
                                min_value=0, max_value=60, value=(timer_values["pump_on_timer"]))

        compressor_on_timer = st.slider("Compressor On ratio (min/h)",
                                min_value=0, max_value=60, value=(timer_values["compressor_on_timer"]))

        #save button
        if st.button("Save timer values"):
            timer_values = {
                "lights_on_timer1": on_timer1, 
                "lights_off_timer1": off_timer1, 
                "lights_on_timer2": on_timer2, 
                "lights_off_timer2": off_timer2, 
                "ventilators_on_timer": ventilators_on_timer, 
                "pump_on_timer": pump_on_timer, 
                "compressor_on_timer": compressor_on_timer
            }
                
                
            save_timer_values(timer_values)
            st.success("The new timer values were succesfully saved!")    

    st.write(f"## Temperatures 🌡️")
    st.write("Set the power off temperature in degrees Celsius")
    heater_on_temp = st.slider("Water heater On temp (°C)",
                                min_value=0, max_value=35, value=(button_states["Set Temperature"]))
    if st.button("Set Temperature"):
            button_states["Set Temperature"] = heater_on_temp
            st.success(f"Heater set to :orange[{heater_on_temp}°C]!")

    st.write("Water temperature:")
    #display water temperature chart
        #load data
    sensor_data = load_sensor_data()
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Water temperature (°C)': [entry[7] for entry in sensor_data]
        })
    
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Water temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Water temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    # Combine the line and points into a layered chart
    chart = (line + points).interactive()

    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Air temperature:")
    #display air temperature chart
    data = pd.DataFrame({
        'timestamp': [entry[0] for entry in sensor_data],
        'Air temperature (°C)': [entry[8] for entry in sensor_data]
        })
    
    # Create Altair chart
    line = alt.Chart(data).mark_line(color='#F0FAFF', strokeWidth=1.5).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500,
    )

    points = alt.Chart(data).mark_circle(color='#F0FAFF', filled=True, size=100).encode(
        x='timestamp',
        y='Air temperature (°C)'
    ).properties(
        width=500,
        height=500
    )

    # Combine the line and points into a layered chart
    chart = (line + points).interactive()

    # Add axis labels
    chart = chart.configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12
    )
    st.altair_chart(chart, use_container_width=True)
    
def load_email_address():
  """Loads the email address from the JSON file if it exists."""
  try:
    with open("email_address.json", "r") as file:
      data = json.load(file)
      return data
  except (FileNotFoundError, json.JSONDecodeError):
    return None

def save_email_address(email_address):
  """Saves the email address to the JSON file."""
  with open("email_address.json", "w") as file:
    json.dump(email_address, file)



def notifications_and_alarms():
    import streamlit as st
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText


    #css definition
    css = """
    <style>
    .custom-text {
        background-color: #262730;
        color: #FAFAFA;
        padding: 10px;
        border-radius: 0px; /* Set border radius for rounded corners */
    }
    </style>
    """

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        Page for maintenance logs and notifications
        """
    )

    

    st.write(css, unsafe_allow_html=True)
    st.write(":red[system errors] and alarms:")
    loaded_alarms = load_alarms()
    if loaded_alarms == None or loaded_alarms == []:
        loaded_alarms = "[Currently there are no active alarms]"
        st.markdown(f'<div class="custom-text">{loaded_alarms}</div>', unsafe_allow_html=True)
    else:
        for alarm in loaded_alarms:
            st.markdown(f'<div class="custom-text">{alarm}</div>', unsafe_allow_html=True)
    st.write("")
    clear_alarms_clicked = st.button("Clear alarms")
    if clear_alarms_clicked:
        clear_alarms()
        st.success("Alarms have been deleted.")
        st.rerun()
    st.write("\n")

    st.write(":blue[logs:]")
    loaded_logs = load_logs()
    if loaded_logs == None or loaded_logs == []:
        loaded_logs = "[No data logs could be loaded]"
        st.markdown(f'<div class="custom-text">{loaded_logs}</div>', unsafe_allow_html=True)
    else:
        for log in loaded_logs:
            st.markdown(f'<div class="custom-text">{log}</div>', unsafe_allow_html=True)
    st.write("\n")
    clear_logs_clicked = st.button("Clear logs")
    if clear_logs_clicked:
        clear_logs()
        st.success("Logs have been deleted.")
        st.rerun()
    st.write("\n")

    # load previous email address from json
    email_address = load_email_address()

    new_email_input = st.text_input("New email address:", value="")
    if new_email_input:
        st.info("Click the \"Set Email Address\" button to save the new address")
        
    # Save email address button
    if st.button("Set Email Address"):
        save_email_address(new_email_input)
        st.success("Email address saved successfully!")
        email_address = new_email_input
    # display the saved email address (optional)
    if email_address:
        st.write("Alarms will be sent to:", email_address)

def calculate_green_pixels(frame):
    import cv2
    import numpy as np

    hsl_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    
    h, s, l = cv2.split(hsl_frame)

    green_mask = np.logical_and((h >= 40), (h <= 82))
    green_pixels = np.count_nonzero(green_mask)

    total_pixels = frame.shape[0] * frame.shape[1]
    greenPixels = (green_pixels / total_pixels)

    return greenPixels, h

def webcamera():
    import cv2
    import streamlit as st
    import time


    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This page connects to the webcam.
        """
    )

    num_webcams = 3  # (max) number of webcams available

    # Create a radio button select to choose the webcam
    selected_webcam = st.sidebar.radio('Select Webcam', range(num_webcams))



    #Frame
    FRAME_WINDOW = st.empty()  
    camera = cv2.VideoCapture(selected_webcam)
    if camera is None or not camera.isOpened():
        st.write(":red[Error: Failed to capture image from webcam. Most probably due to no existing webcam with the selected index]")
        camera.release()
        cv2.destroyAllWindows()
        st.stop()
    else:
        try:
            green_pixels = 0
            while True:
                ret, frame = camera.read()
                if not ret:
                    st.write(":red[Error: Failed to capture image from webcam. Most probably due to no existing webcam with the selected index] ")
                    st.stop()
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                green_pixels, h_values = calculate_green_pixels(frame)

                #update frame
                FRAME_WINDOW.image(frame, caption=f'[Green pixels on display:{"{:.2f}".format(green_pixels*100)}%]')
                # Wait for 5 seconds
            camera.release()
            cv2.destroyAllWindows()
            

        except cv2.error as e:
            st.write(f'OpenCV error: {e}')
            st.write(":red[An error occurred while processing the image.]")
            camera.release()
            cv2.destroyAllWindows()
        except AssertionError as e:
            st.write(f'Assertion error: {e}')
            st.write('An assertion error occurred while processing the image.')
            camera.release()
            cv2.destroyAllWindows()
    

page_names_to_funcs = {
    "Recorded sensor data 📈": data_plots,
    "Controls 📱": controls, 
    "System logs and alarms 🚨": notifications_and_alarms,
    "Webcamera 📷": webcamera
}

demo_name = st.sidebar.radio("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
