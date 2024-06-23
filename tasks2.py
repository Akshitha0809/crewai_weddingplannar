



# Importing the necessary classes and tools
from crewai import Task
from tools import search_tool, file_search_tool, scrapewebtool, file_search_tool2
from agent import anaylsing_agent, writer, file_search_tool1

# Creating an analyzing task to understand wedding events from a text file
analysing_task = Task(
  description=(
    "Understanding all aspects after reading the txt file and getting an idea of the wedding events, and provide the event names to the next agent when required changes. Event names are {eventnames}, remaining data should not be changed."
  ),
  expected_output='Provide preferred locations for each wedding event to other agent, event names which location need to be changed.',
  tools=[file_search_tool2],
  agent=anaylsing_agent,
)

# Importing additional tools
from tools import search_tool

# Importing the location finder agent
from agent import locationfinderagent

# Creating a task to determine the perfect wedding location in a given city
Location_task = Task(
  description=(
    "To determine the perfect location for a wedding event in my city, {cityname}, which requires changes. For remaining, keep it as it is."
  ),
  expected_output='To identify the ideal wedding venue in {cityname}.',
  tools=[scrapewebtool, search_tool],
  agent=locationfinderagent,
  async_execution=False,
)

# Importing additional tools and agents
from tools import search_tool, file_search_tool
from agent import capacityfinderagent, Budgetfinderagent

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
