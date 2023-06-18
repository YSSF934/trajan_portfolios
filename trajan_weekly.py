# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import time

#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")
#---------------------------------#
# Title

image = Image.open('logo1.jpg')

st.image(image, width = 500)

st.title('Trajan Wealth Portfolio Dashboard')
st.markdown("""
**data as of 6/20/2023**

""")
#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Instructions:** Use the sidebar on the left to adjust the number of funds and time frame to analyze
* **Data source:** [Factset ](https://www.factset.com/).
* **email yaron.shamash@trajanwealth.com with any inquiries or suggestions**
""")


#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

def load_data():

    df = pd.read_csv('dash061823.csv')

    return df

# load csv
df = load_data()


## Sidebar - Fund selections
sorted_fund = sorted( df['nickname'] )
selected_fund = col1.multiselect('Click to remove Fund from analysis', sorted_fund, sorted_fund)

df_selected_fund = df[ (df['nickname'].isin(selected_fund)) ] # Filtering data

## Sidebar - Number of coins to display
num_fun = col1.slider('Display Top N Funds', 1, 54, 54)
df_funds = df_selected_fund[:num_fun]

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['1 Week','1 Month','3 Month','YTD'])
percent_dict = {"1 Week":"1 Week" ,"1 Month":'1 Month',"3 Month":"3 Month","YTD":"YTD"}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Funds and Indexes')
col2.write('Data Dimension: ' + str(df_selected_fund.shape[0]) + ' rows and ' + str(df_selected_fund.shape[1]) + ' columns.')

col2.dataframe(df)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_fund), unsafe_allow_html=True)

#---------------------------------#
# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')

df_change = pd.concat([df_funds['nickname'], df_funds['1 Week'], df_funds['1 Month'], df_funds['3 Month'], df_funds['YTD'] ], axis=1)
df_change = df_change.set_index('nickname')
df_change['positive_percent_change_1 Week'] = df_change['1 Week'] > 0
df_change['positive_percent_change_1 Month'] = df_change['1 Month'] > 0
df_change['positive_percent_change_3 Month'] = df_change['3 Month'] > 0
df_change['positive_percent_change_YTD'] = df_change['YTD'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == 'YTD':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['YTD'])
    col3.write('*YTD period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['YTD'].plot(kind='barh', color=df_change['positive_percent_change_YTD'] .map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '3 Month':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['3 Month'])
    col3.write('*3 Month period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['3 Month'].plot(kind='barh', color=df_change['positive_percent_change_3 Month'].map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '1 Month':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['1 Month'])
    col3.write('*1 Month period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['1 Month'].plot(kind='barh', color=df_change['positive_percent_change_1 Month'].map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['1 Week'])
    col3.write('*1 Week period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['1 Week'].plot(kind='barh', color=df_change['positive_percent_1 Week'].map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
