import re
import pandas as pd

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[a|p]m\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['date'] = df['date'].str.replace(' -', '', regex=False)
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p')

    users = []
    messages = []

    for msg in df["user_message"]:
        if ": " in msg:
            user, message = msg.split(": ", 1)
        else:
            user = "group notification"
            message = msg
        users.append(user)
        messages.append(message)

    # Add new columns to the dataframe
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df