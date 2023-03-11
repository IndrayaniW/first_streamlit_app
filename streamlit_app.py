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
streamlit.header('Fruityvice Fruit Advice!') # positioning makes a difference in the display
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon") # fixed value watermelon

#removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
#streamlit.text(fruityvice_response)# this only returns the response '<Response [200]>' on the webpage

# adding .json() to show the contents of the json file instead of the response 200
#streamlit.text(fruityvice_response.json())


## making the Fruityvice Data Looking a Little Nicer

# putting the json data format into a pandas dataframe / taking the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it in the screen as a table / dataframe
streamlit.dataframe(fruityvice_normalized)

# adding new section to display fruityvice api response
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') # using text input
streamlit.write('The user entered ', fruit_choice)
