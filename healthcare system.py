import numpy as np
import streamlit as st
import pandas as pd
import pymysql
import time
from DingDing import getDingMes
import os
import hashlib  # 新增：导入哈希库


# 页面设置
st.set_page_config(
    page_title="Health-Care Monitoring System",
    page_icon="❄️️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "This app monitors your health data!"}
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    .metric-label {
        font-size: 16px;
    }
    .metric-value {
        font-size: 26px;
        color: #10b981;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.2em;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_login(username, password):
    db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
    cursor = db.cursor()
    sql = "SELECT password_hash FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    db.close()

    if result:
        stored_hash = result[0]
        return hash_password(password) == stored_hash
    return False

def register_user(username, password):
    password_hash = hash_password(password)
    try:
        db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
        cursor = db.cursor()
        sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(sql, (username, password_hash))
        db.commit()
        db.close()
        return True
    except pymysql.err.IntegrityError:
        return False  # 用户名已存在


# DingTalk 报警函数
def send_alert_with_advice(message: str, advice: str):
    full_message = f"{message}\nAdvice: {advice}"
    getDingMes(full_message)

# 登录或注册界面
if 'user' not in st.session_state:
    st.title("🔐 Login to Health-Care System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if check_user_login(username, password):
                st.session_state['user'] = username
                st.success(f"Welcome, {username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("New Username", key="register_username")
        new_password = st.text_input("New Password", type="password", key="register_password")

        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists. Try another one.")

    st.stop()


if 'user' not in st.session_state:
    st.warning("🚨 You are not logged in. Please login first.")
    st.stop()

# 身高体重输入界面
if 'height' not in st.session_state or 'weight' not in st.session_state:
    st.title("📝 Enter Your Information")
    height = st.text_input('Height (cm):')
    weight = st.text_input('Weight (kg):')
    if st.button("Submit"):
        if height and weight:
            st.session_state['height'] = height
            st.session_state['weight'] = weight
            st.success("Info saved successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Please enter both height and weight.")
    st.stop()

# 数据获取函数
def get_data_hr():
    db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "SELECT * FROM hr WHERE id = (SELECT MAX(id) FROM hr)"
    df = pd.read_sql(sql, con=db)
    db.close()
    return df

def get_data_k():
    db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "SELECT * FROM kidney WHERE id = (SELECT MAX(id) FROM kidney)"
    df = pd.read_sql(sql, con=db)
    db.close()
    return df

def get_data_bq():
    db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "SELECT * FROM bp WHERE id = (SELECT MAX(id) FROM bp)"
    df = pd.read_sql(sql, con=db)
    db.close()
    return df

def get_data_brain():
    db = pymysql.connect(host="localhost", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "SELECT * FROM brain WHERE id = (SELECT MAX(id) FROM brain)"
    df = pd.read_sql(sql, con=db)
    db.close()
    return df

def update_dataframe():
    new_data = pd.DataFrame(np.random.randint(15, 25, size=(10, 4)), columns=['alpha', 'beta', 'theta', 'gamma'])
    df_container.dataframe(new_data.style.highlight_max(axis=0), width=1300)

# 主界面
col1, col2 = st.columns((6, 1))
col1.title("🐻‍ Health-Care Monitoring System 🐻‍️")
st.markdown("---")

st.sidebar.markdown("## 👋 Welcome!")
st.sidebar.success(f"🐻‍❄ Hello, **{st.session_state['user']}**! I am your doctor bear.")
st.sidebar.info("🩺 I will help monitor your health-care data.")
st.sidebar.warning("⭐️ Abnormal situations will be reported via **DingTalk** robot.")

# 显示基础信息
col1, col2, col3 = st.columns(3)
col1.metric(label="Height (cm)", value=int(st.session_state['height']), delta=0)
col2.metric(label="Weight (kg)", value=int(st.session_state['weight']), delta=0)
col3.metric(
    label="BMI",
    value=np.round(
        int(st.session_state['weight']) * 10000 / (int(st.session_state['height']) ** 2), 2),
    delta=0
)

if st.button("🚦 Start Monitoring"):
    with st.spinner('🧪 Starting... Please wait a moment...'):
        os.system("sh run.sh")
        time.sleep(3)

    info = st.empty()
    df_container = st.empty()

    last_rows_bq = pd.DataFrame({
        'time': [time.strftime("%H:%M:%S")],
        'blood pressure': [110],
        'diastolic pressure': [118],
        'systolic pressure': [90],
        'high': [120],
        'low': [60]
    })

    last_rows_hr = pd.DataFrame({
        'heart rate': [70],
        'time': [time.strftime("%H:%M:%S")]
    })

    last_rows_k = pd.DataFrame({
        'right kidney': [40],
        'left kidney': [32],
        'time': [time.strftime("%H:%M:%S")]
    })

    st.write("Brain Wave Results:")
    df_b = pd.DataFrame(np.random.randint(15, 25, size=(10, 4)), columns=['alpha', 'beta', 'theta', 'gamma'])
    df_container.dataframe(df_b.style.highlight_max(axis=0), width=1300)

    st.write("Blood Pressure Results:")
    chart_bq = st.line_chart(last_rows_bq.set_index('time'))

    st.write("Heart Rate Results:")
    chart_hr = st.area_chart(last_rows_hr.set_index('time'))

    st.write("Kidney Indicators Results:")
    chart_k = st.bar_chart(last_rows_k.set_index('time'))

    while True:
        info.success("Monitoring: Brain Waves, Heart Rate, Blood Pressure, and Kidney Indicators...")

        # 脑电波
        df = get_data_brain()
        update_dataframe()

        # 血压
        df = get_data_bq()
        bp = round(df.loc[0, 'bqlow'] / 3 + df.loc[0, 'bqhigh'] * 2 / 3)
        df2 = pd.DataFrame({
            'time': [df.loc[0, 'time']],
            'blood pressure': [bp],
            'diastolic pressure': [df.loc[0, 'bqhigh']],
            'systolic pressure': [df.loc[0, 'bqlow']],
            'high': [120],
            'low': [60]
        })
        last_rows_bq = pd.concat([last_rows_bq, df2])
        chart_bq.line_chart(last_rows_bq.set_index('time'))

        if df.loc[0, 'bqlow'] < 60:
            send_alert_with_advice("Warning: Low blood pressure detected!",
                                   "Please rest, drink water, and avoid intense activity. Seek medical attention if this persists.")
        elif df.loc[0, 'bqhigh'] > 130:
            send_alert_with_advice("Warning: High blood pressure detected!",
                                   "Reduce salt intake, stay calm, and consult a doctor if it remains high.")

        # 心率
        df = get_data_hr()
        df2 = pd.DataFrame({'heart rate': [df.loc[0, 'heartrate']], 'time': [df.loc[0, 'time']]})
        last_rows_hr = pd.concat([last_rows_hr, df2])
        chart_hr.area_chart(last_rows_hr.set_index('time'))

        if df.loc[0, 'heartrate'] < 40:
            send_alert_with_advice("Warning: Low heart rate detected!",
                                   "You may be fatigued or over-exercised. Please rest and seek medical help if needed.")
        elif df.loc[0, 'heartrate'] > 120:
            send_alert_with_advice("Warning: High heart rate detected!",
                                   "Stop any activity, take deep breaths, and relax. Contact a doctor if symptoms persist.")

        # 肾脏
        df = get_data_k()
        df2 = pd.DataFrame({
            'time': [df.loc[0, 'time']],
            'right kidney': [df.loc[0, 'rightkidney']],
            'left kidney': [df.loc[0, 'leftkidney']],
        })
        last_rows_k = pd.concat([last_rows_k, df2])
        chart_k.bar_chart(last_rows_k.set_index('time'))

        time.sleep(2)