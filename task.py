# Importing the necessary classes and tools
from crewai import Task
from tools import search_tool, file_search_tool, scrapewebtool
from agent import anaylsing_agent, writer, file_search_tool1, timeplanner

# Creating an analyzing task to understand wedding events from a text file
analysing_task = Task(
  description=(
    "Understanding all aspects after reading the txt file and getting an idea of the wedding events"
  ),
  expected_output='Provide preferred locations for each wedding events to other agent.',
  tools=[file_search_tool],
  agent=anaylsing_agent,
)

# Importing additional tools and agents
from tools import search_tool
from agent import locationfinderagent

# Creating a task to determine the perfect wedding location in a given city
Location_task = Task(
  description=(
    "To determine the perfect location for a wedding event in my city, {cityname}."
  ),
  expected_output='To identify the ideal wedding venue in {cityname}.',
  tools=[scrapewebtool, search_tool],
  agent=locationfinderagent,
  async_execution=False,
)

# Importing additional tools and agents
from tools import search_tool, file_search_tool
from agent import capacityfinderagent, Budgetfinderagent, anaylsing_agent

# Creating a task to find suitable venues that can accommodate the number of guests
capacityfindertask = Task(
  description=(
    "To identify the selected resorts or function hall for each event, if they cannot accommodate the number of guests, change the locations. Our number of guests is {capacity}."
  ),
  expected_output='The capacity of all selected resorts and function halls.',
  tools=[scrapewebtool, search_tool],
  agent=capacityfinderagent,
  context=[Location_task],
  async_execution=False,
)

# Creating a task to ascertain the budget for the selected venues
Budgetfindertask = Task(
  description=(
    "To ascertain the budget needed for selected resorts and function halls."
  ),
  expected_output='The budget of all selected resorts and function halls.',
  tools=[scrapewebtool, search_tool],
  agent=capacityfinderagent,
  context=[Location_task]
)

# Creating a writer task to compile and format the selected venue details
writer_task = Task(
    description="Compile and format the selected function hall, accurate capacity, and its budget. The information will be provided by other agents.",
    expected_output='A clear and structured presentation of the selected function hall, accurate capacity, and its budget, and time allocated in the given format',
    tools=[file_search_tool1],
    agent=writer,
    context=[Budgetfindertask, Location_task, capacityfindertask],
    human_input=True,
    output_file='final_report.md'
)

# Creating a time allocation task for each event
time_task = Task(
    description="Allocate time slot to each event, so that all events will be finished in given number of days {noofdays}.",
    expected_output='A time slots for each event',
    tools=[file_search_tool1],
    agent=timeplanner,
    context=[analysing_task],
    human_input=False,
)
