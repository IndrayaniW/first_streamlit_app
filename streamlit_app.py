import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError # library to control the flow of changes (for error message handling)

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

# create the repeatable code block (function)
def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)# for dynamic variable setting based on user input
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

# 11.3.23 new section to display fruityvice api response. Shows <Response [200]> in the streamlit-created web-app
streamlit.header('Fruityvice Fruit Advice!') # positioning makes a difference in the display
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon") # fixed value watermelon

try:
 
 # adding new section to display fruityvice api response
 #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') # using text input with preselected value Kiwi
 fruit_choice = streamlit.text_input('What fruit would you like information about?')  # using text input without preselected value
 
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
 else:
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)# for dynamic variable setting based on user input
  #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  #streamlit.dataframe(fruityvice_normalized)
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
 
except URLError as e:
 streamlit.error()
 #streamlit.write('The user entered ', fruit_choice)


#removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there)
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")# for fixed variable setting
#streamlit.text(fruityvice_response)# this only returns the response '<Response [200]>' on the webpage
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)# for dynamic variable setting based on user input

# adding .json() to show the contents of the json file instead of the response 200
#streamlit.text(fruityvice_response.json())




## making the Fruityvice Data Looking a Little Nicer

# putting the json data format into a pandas dataframe / taking the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it in the screen as a table / dataframe
#streamlit.dataframe(fruityvice_normalized)

# to avoid code being run each time the code interacts with the streamlit app, in this case inserting the same value each time, put a stop
# don't run anything past here while we troubleshoot
#streamlit.stop()



streamlit.header("The fruit load list contains:")

# adding Snowflake related functions
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from fruit_load_list")# querying actual data from SF
  return my_cur.fetchall()
 
# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)# shows table / dataframe format
 
#streamlit.stop()

# adding new section as entry box to allow adding fruits
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("insert into fruit_load_list values ('from streamlit')")
  return "Thanks for adding "+ add_my_fruit
 
 
add_my_fruit = streamlit.text_input('What fruit would you like to add?') # using text input
if streamlit.button('Add a Fruit to the List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)
streamlit.write('Thanks for adding ', fruit_added)

# Add Rows to Our Fruit List in Snowflake
# this will not work correctly, but just go with it for now
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
