# Wedding Planner with CrewAI

This project uses CrewAI to create a multi-agent system for planning South Indian weddings. The agents work together to analyze wedding events, find suitable locations, assess venue capacities, estimate budgets, and compile the information into a structured format.

## Installation and Setup

### Prerequisites

- Python 3.8 or later
- Conda (Anaconda/Miniconda)

### Installing Conda

If you do not have Conda installed, you can download and install it from [here](https://docs.conda.io/en/latest/miniconda.html).

### Setting Up the Environment

1. **Create a new Conda environment:**

    ```bash
    conda create --name wedding_planner python=3.8
    ```

2. **Activate the environment:**

    ```bash
    conda activate wedding_planner
    ```

3. **Install CrewAI and other dependencies:**

    ```bash
    pip install crewai pymongo
    ```

4. **Set the required environment variables:**

    ```python
    os.environ["SERPER_API_KEY"] = "your_serper_api_key"
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"  # Ensures use of gpt-3.5-turbo
    ```

### Directory Structure

```plaintext
.
├── README.md
├── agent.py
├── task.py
├── tools.py
├── crewai.py
└── main.py


Agents

Analyzing Agent
Role: Senior Analyzing Agent
Goal: Breakdown of events in a South Indian wedding.
Tools: file_search_tool2
Features: Verbose, retains memory, allows delegation.
Backstory: Highly skilled in analysis, this agent is adept at breaking down complex events into manageable tasks.

Location Finder Agent
Role: Location Finder
Goal: Find the perfect locations for each wedding event considering the capacity.
Tools: scrapewebtool, search_tool
Features: Verbose, retains memory, allows delegation.
Backstory: Expert in identifying ideal locations tailored to the vision of each event.

Capacity Finder Agent
Role: Capacity Finder Agent
Goal: Assess the capacity of selected resorts or function halls.
Tools: scrapewebtool, search_tool
Features: Verbose, retains memory, allows delegation.
Backstory: Ensures precise venue capacity assessments for streamlined wedding planning.

Budget Finder Agent
Role: Budget Finder Agent
Goal: Determine the budget requirements for selected venues.
Tools: scrapewebtool, search_tool
Features: Verbose, retains memory, allows delegation.
Backstory: Helps pinpoint budget needs to ensure events stay within financial bounds.

Writer Agent
Role: Writer
Goal: Format and present details about the selected venues, including capacity and budget.
Tools: file_search_tool1
Features: Verbose, retains memory, does not allow delegation.
Backstory: Expert in formatting and presentation, compiling information provided by other agents.

Time Planner Agent
Role: Scheduler
Goal: Allocate time slots for each event to ensure all activities occur smoothly within the given days.
Tools: search_tool, scrapewebtool
Features: Verbose, retains memory, does not allow delegation.
Backstory: Ensures all planned activities occur smoothly and on schedule.

Tasks

Analyzing Task
Description: Understand all aspects of wedding events from a text file.
Expected Output: Preferred locations for each wedding event.
Tools: file_search_tool
Agent: anaylsing_agent

Location Task
Description: Determine the perfect wedding location in a given city.
Expected Output: Identify the ideal wedding venue in the specified city.
Tools: scrapewebtool, search_tool
Agent: locationfinderagent
Async Execution: True

Capacity Finder Task
Description: Identify if the selected venues can accommodate the number of guests, and change locations if necessary.
Expected Output: Capacities of selected venues.
Tools: scrapewebtool, search_tool
Agent: capacityfinderagent
Context: Location_task
Async Execution: True

Budget Finder Task
Description: Ascertain the budget needed for the selected venues.
Expected Output: Budgets of the selected venues.
Tools: scrapewebtool, search_tool
Agent: Budgetfinderagent
Context: Location_task

Writer Task
Description: Compile and format the details of selected venues.
Expected Output: A clear and structured presentation of venue details.
Tools: file_search_tool1
Agent: writer
Context: Budgetfindertask, Location_task, capacityfindertask
Human Input: True

Output File: final_report.md
Time Task
Description: Allocate time slots for each event.
Expected Output: Time slots for each event.
Tools: file_search_tool1
Agent: timeplanner
Context: analysing_task
Human Input: False




Crew Setup
Crew 1

from crewai import Crew, Process

crew = Crew(
  agents=[anaylsing_agent, locationfinderagent, capacityfinderagent, Budgetfinderagent, timeplanner, writer],
  tasks=[analysing_task, Location_task, capacityfindertask, Budgetfindertask, time_task, writer_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  embedder={"provider": "gpt-3.5-turbo"},
  share_crew=True
)

crew 2 also similar with changes in prompts



Working of the Wedding Planner
Analyzing the Wedding Events:

The anaylsing_agent reads and analyzes the wedding events from a text file using the analysing_task.
Finding Locations:

The locationfinderagent identifies potential wedding venues in the specified city using the Location_task.
Assessing Venue Capacities:

The capacityfinderagent checks if the identified venues can accommodate the number of guests using the capacityfindertask.
Estimating Budget:

The Budgetfinderagent calculates the budget requirements for the selected venues using the Budgetfindertask.
Compiling and Formatting Information:

The writer compiles and formats the venue details into a clear report using the writer_task.
Allocating Time Slots:

The timeplanner assigns time slots to each event to ensure smooth scheduling using the time_task.
The system is designed to handle both new and existing users, allowing for changes to event details as needed. The MongoDB database is used to store and manage user data, ensuring a personalized and efficient wedding planning experience.




