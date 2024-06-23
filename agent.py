from tools import search_tool, file_search_tool, scrapewebtool, file_search_tool2
from crewai import Agent

# Analysing Agent: This agent is responsible for breaking down and analyzing the various events in a South Indian wedding.
# It uses the 'file_search_tool2' tool to assist with its analysis. The agent is verbose, retains memory of its actions,
# and is allowed to delegate tasks to other agents if needed.
anaylsing_agent = Agent (
    role='Senior analysing_agent',
    goal='breakdown of events in a South Indian wedding',
    verbose=True,
    memory=True,
    backstory=(
        "you're very good at analysis"
    ),
    tools=[file_search_tool2],
    allow_delegation=True,
)

# Location Finder Agent: This agent's goal is to find the perfect locations for each wedding event,
# taking into consideration the required capacity. It uses the 'scrapewebtool' and 'search_tool' tools
# to gather necessary information about potential locations. The agent is verbose, retains memory,
# and can delegate tasks to other agents.
locationfinderagent = Agent (
    role='location finder',
    goal='To find the perfect locations for each wedding event which can accommodate the given {capacity}',
    verbose=True,
    memory=True,
    backstory=(
        "Specializing in finding ideal locations for every wedding event, tailored to your vision"
    ),
    tools=[scrapewebtool, search_tool],
    allow_delegation=True,
)

# Capacity Finder Agent: This agent's goal is to find the capacity of selected resorts or function halls.
# It uses the 'scrapewebtool' and 'search_tool' tools to gather information about the venue capacities.
# The agent is verbose, retains memory, and can delegate tasks to other agents.
capacityfinderagent = Agent (
    role='capacityfinderagent',
    goal='Finding the capacity of the selected resorts or function halls.',
    verbose=True,
    memory=True,
    backstory=(
        "Utilize CapacityFinder for precise venue capacity assessments, streamlining wedding planning"
    ),
    tools=[scrapewebtool, search_tool],
    allow_delegation=True,
)

# Budget Finder Agent: This agent is tasked with determining the budget requirements for the selected resorts and function halls.
# It uses the 'scrapewebtool' and 'search_tool' tools to gather budget-related information.
# The agent is verbose, retains memory, and can delegate tasks to other agents.
Budgetfinderagent = Agent (
    role='Budgetfinderagent',
    goal='Determining the budget requirements for the selected resorts and function halls.',
    verbose=True,
    memory=True,
    backstory=(
        "Pinpointing budget needs for chosen venues ensures event success within financial bounds."
    ),
    tools=[scrapewebtool, search_tool],
    allow_delegation=True,
)

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool, FileReadTool

file_search_tool1 = FileReadTool(file_path='format.txt')

# Writer Agent: This agent's role is to format and present the selected function hall,
# including its capacity and budget, in a clear and structured manner. 
# It uses the 'file_search_tool1' tool to assist in formatting the information.
# The agent is verbose, retains memory, but is not allowed to delegate tasks to other agents.
writer = Agent(
    role='Writer',
    goal='Format and present the selected Function hall, and its capacity, and its budget in a clear and structured manner.',
    verbose=True,
    memory=True,
    backstory="An expert in formatting and presentation, you compile and format the information provided by other agents.",
    tools=[file_search_tool1],
    allow_delegation=False
)

# Time Planner Agent: This agent is responsible for efficiently allocating and managing time and resources
# to ensure all planned activities occur smoothly and on schedule within the given number of days.
# It uses the 'search_tool' and 'scrapewebtool' to gather information necessary for planning and scheduling.
# The agent is verbose, retains memory, but is not allowed to delegate tasks to other agents.
timeplanner = Agent(
    role='scheduler',
    goal='efficiently allocate and manage time and resources to ensure that all planned activities occur smoothly and on schedule in the given no.of days.',
    verbose=True,
    memory=True,
    backstory="scheduler was to ensure all planned activities occurred smoothly and on schedule. And dedication minimizing conflicts and delays was evident in every flawlessly executed event.",
    tools=[search_tool, scrapewebtool],
    allow_delegation=False
)
