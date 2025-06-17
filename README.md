# MQTT-Health-care-system
A healthcarA real-time health monitoring system using MQTT and Streamlit. It simulates wearable sensors, visualizes heart, brain, kidney, and blood pressure data, and sends alerts via DingTalk when abnormalities are detected.

## Core Features

- Real-time simulation and publishing of health sensor data via MQTT
- Topic-based message routing using an MQTT broker
- Subscriber module for data evaluation and alert triggering
- DingTalk Bot integration for health warnings
- User login and BMI calculation
- Interactive health data visualization using Streamlit
- MySQL database for storing user and health records

## MQTT Topics

- `/public/hr` – Heart rate
- `/public/bp` – Blood pressure
- `/public/kidney` – Kidney function
- `/public/brain` – Brainwave data
- `/alarm` – System alerts

## Technologies Used

- Python
- MQTT (paho-mqtt)
- Streamlit
- MySQL
- DingTalk Bot API
