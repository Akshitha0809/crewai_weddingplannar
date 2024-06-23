import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Set the API keys and model selection as environment variables

os.environ["SERPER_API_KEY"] = os.getenv('SERPER')

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI')

os.environ["OPENAI_MODEL_NAME"]=os.getenv('MODEL')

# Import custom agents and tasks

from agent import anaylsing_agent, locationfinderagent, capacityfinderagent, Budgetfinderagent, writer, timeplanner
from task import analysing_task, Location_task, capacityfindertask, Budgetfindertask, writer_task, time_task

# Import Crew and Process classes from crewai
from crewai import Crew, Process

# Create the first crew with a set of agents and tasks
crew = Crew(
  agents=[anaylsing_agent, locationfinderagent, capacityfinderagent, Budgetfinderagent, timeplanner, writer],
  tasks=[analysing_task, Location_task, capacityfindertask, Budgetfindertask, time_task, writer_task],
  process=Process.sequential,  # Specify sequential task execution
  embedder={"provider": "gpt-3.5-turbo"},  # Set the embedder to use GPT-3.5-turbo
  share_crew=True  # Allow sharing the crew
)

# Import tasks for the second crew
from tasks2 import analysing_task, Location_task, capacityfindertask, Budgetfindertask, writer_task

# Create the second crew with new tasks but the same set of agents
crew2 = Crew(
  agents=[anaylsing_agent, locationfinderagent, capacityfinderagent, Budgetfinderagent, timeplanner, writer],
  tasks=[analysing_task, Location_task, capacityfindertask, Budgetfindertask, time_task, writer_task],
  process=Process.sequential,  # Specify sequential task execution
  embedder={"provider": "gpt-3.5-turbo"},  # Set the embedder to use GPT-3.5-turbo
  share_crew=True  # Allow sharing the crew
)

# MongoDB setup
from pymongo import MongoClient

# Function to check if a username already exists in the database
def check_name_exists(name):
    query = {'name': name}
    result = collection.find_one(query)
    return result is not None

# Connect to the local MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the database named 'akshi_crewai'
db = client['akshi_crewai']

# Access the collection named 'userdata'
collection = db['userdata']

# Create a unique index on the 'name' field to ensure usernames are unique
collection.create_index([('name', 1)], unique=True)

# Ask the user if they are an existing user or a new user
usertype = input('Are you an existing user? If yes, write your username, if no, type no')

# If the user is new or their username does not exist in the database
if(not check_name_exists(usertype) or usertype == 'no'):
    cityname = input('Enter your city location')  # Get city location from user
    capacity = input('Enter your number of guests')  # Get number of guests from user
    budget = input('Enter your budget')  # Get budget from user
    day = input('Enter number of days')  # Get number of days from user
    
    # Kick off the first crew with user inputs
    result = crew.kickoff(inputs={'cityname': cityname, 'budget': budget, 'capacity': capacity, 'noofdays': day})
    print(result)  # Print the result of the crew kickoff

    a = 1
    name = input('Enter the username you like')  # Ask the user to enter a desired username

    while(a == 1):
        if(check_name_exists(name)):  # Check if the username already exists
            name = input('The username already exists. Try a new username, or attach some numbers to the existing username')
        else:
            # Read the final report and insert the user data into the MongoDB collection
            with open('final_report.md', 'r') as file:
                content = file.read()
                document = {
                    'name': name,
                    'data': content,
                    'cityname': cityname,
                    'capacity': capacity,
                    'budget': budget,
                    'day': day
                }
                result = collection.insert_one(document)
                a = 0  # Exit the loop

# If the user is an existing user
else:
    typee = input('Enter 1 if you want to change the city itself (all things will be changed in this option), enter 2 if you want to change locations only')
    if(typee == '1'):
        # If the user wants to change the city and other details
        cityname = input('Enter your location')
        capacity = input('Enter the number of guests')
        budget = input('Enter your budget')
        day = input('Enter number of days')
        
        # Kick off the first crew with new inputs
        result = crew.kickoff(inputs={'cityname': cityname, 'budget': budget, 'capacity': capacity, 'noofdays': day})
        
        # Read the final report and update the user data in the MongoDB collection
        with open('final_report.md', 'r') as file:
            content = file.read()
            query = {'name': usertype}
            update = {
                '$set': {
                    'data': content,
                    'cityname': cityname,
                    'capacity': capacity,
                    'budget': budget,
                    'day': day
                }
            }
            result = collection.update_one(query, update)
    
    # If the user wants to change only specific locations
    else:
        datas = collection.find({'name': usertype})
        eventchanges = input('Enter the event names that need to be changed, separated by commas')
        
        # Write the previous data and event changes to a file
        with open('perviousdata.txt', 'w') as file:
            content = file.write(datas[0]['data'] + '\n' + 'Events which require location changes: ' + eventchanges)

        cityname = datas[0]['cityname']
        capacity = datas[0]['capacity']
        budget = datas[0]['budget']
        day = datas[0]['day']

        # Kick off the second crew with updated inputs
        result = crew2.kickoff(inputs={'cityname': cityname, 'budget': budget, 'capacity': capacity, 'eventnames': eventchanges, 'noofdays': day})
        
        # Read the final report and update the user data in the MongoDB collection
        with open('final_report.md', 'r') as file:
            content = file.read()
            query = {'name': usertype}
            update = {
                '$set': {
                    'data': content,
                }
            }
            result = collection.update_one(query, update)





            

        

        

    
           


   















































