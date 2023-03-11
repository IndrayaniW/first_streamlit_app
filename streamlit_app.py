import streamlit
import pandas
import requests

#streamlit.title('My Parents New Healthy Diner - Changes made')
streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
 
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
 
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
 
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# pulling the data into a pandas dataframe
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# setting an index on Fruit for the interactive selector, so it shows fruit names instead on numbers
my_fruit_list = my_fruit_list.set_index('Fruit')

# ask the streamlit library to display it on the page
#streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer
# below: preselecting some fruits
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

# showing only the selected fruits in the table by connecting the table with the pick list
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the selected fruits only
streamlit.dataframe(fruits_to_show)

# 11.3.23 new section to display fruityvice api response. Shows <Response [200]> in the streamlit-created web-app
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)

streamlit.header('Fruityvice Fruit Advice!')
