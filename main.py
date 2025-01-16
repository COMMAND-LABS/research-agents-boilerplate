import json
import os
from datetime import datetime
from helpers.execute_task_async import execute_task_async
from helpers.format_news_for_email import format_news_for_email
from helpers.is_valid_email import is_valid_email
from helpers.send_email_ses import send_email_ses
from crewai import Agent, Task, LLM
import yaml
from prompts.analyst_task_description_tmplt import analyst_task_description_tmplt
from prompts.research_task_description_tmplt import research_task_description_tmplt
from pydantic_types.news_results import NewsResults
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from tools.custom_scrape_website import CustomScrapeWebsiteTool
from tools.url_qa import UrlQaTool

load_dotenv()

# Uncomment the following lines to enable debugging with debugpy
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()

# Import the AgentOps SDK
import agentops
agentops.init(os.getenv("AGENTOPS_API_KEY"))

# Mock crew output with the following lines for testing purposes
# from types import SimpleNamespace # Load mock crew output for testing
# with open('test/mocks/crew_output.json', 'r') as file:
#   mock_crew_output = json.load(file, object_hook=lambda d: SimpleNamespace(**d))

current_datetime = datetime.now()
current_date_frmttd = current_datetime.strftime("%Y-%m-%d")  # Add current date

agents_yaml = None
tasks_yaml = None
with open("config/agents.yaml", 'r') as file:
    agents_yaml = yaml.safe_load(file)
tasks_yaml = None
with open("config/tasks.yaml", 'r') as file:
    tasks_yaml = yaml.safe_load(file)

emails=(os.getenv("MAILING_LIST") or "")

# Define main script
def main():
    print('--- Supercharged News Crew ---')

    current_date = datetime.now().strftime("%Y-%m-%d")  # Add current date

    # -v-v- DEFINE AGENTS -v-v-
    researcher = Agent(
      config=agents_yaml['researcher'],
      verbose=True,
      tools=[
        CustomScrapeWebsiteTool()
      ],
      llm=LLM(model="gpt-4o")
    )
    analyst = Agent(
      config=agents_yaml['analyst'],
      tools=[CustomScrapeWebsiteTool(), UrlQaTool()],
      verbose=True,
      llm=LLM(model="gpt-4o")
    )

    # -v-v- DEFINE TASKS -v-v-
    task_research_insurtechinsights = Task(
        description=research_task_description_tmplt("https://www.insurtechinsights.com/news-insights/artificial-intelligence/", current_date),
        expected_output=tasks_yaml['research_task']["expected_output"],
        output_pydantic=NewsResults,
        agent=researcher,
    )
    task_research_insurtechnews = Task(
        description=research_task_description_tmplt("https://insurtechnews.com/", current_date),
        expected_output=tasks_yaml['research_task']["expected_output"],
        output_pydantic=NewsResults,
        agent=researcher,
    )
    task_research_insurtechdigital = Task(
        description=research_task_description_tmplt("https://insurtechdigital.com/", current_date),
        expected_output=tasks_yaml['research_task']["expected_output"],
        output_pydantic=NewsResults,
        agent=researcher,
    )

    # List of research tasks to be performed in parallel
    tasks = [
        task_research_insurtechinsights,
        task_research_insurtechnews,
        task_research_insurtechdigital
    ]

    research_results = [] # Execute tasks in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:  # You can adjust the max_workers value
        # Submit all tasks to the executor
        futures = {executor.submit(execute_task_async, task): task for task in tasks}
        # Collect results as they are completed by the "researchers"
        for future in as_completed(futures):
            result = future.result()
            if result:
                research_results.extend(result.pydantic.results)

    final_analysis = Task(
        description=analyst_task_description_tmplt(current_date, research_results),
        expected_output=tasks_yaml['final_analysis']["expected_output"],
        agent=analyst,
        output_pydantic=NewsResults,
        # output_file="report.json" # Uncomment this line to save the output to a file for testing
    )

    final_analysis_output = final_analysis.execute_sync()

    email_list = emails.split(',')
    if len(email_list) == 0:
        print("No email addresses provided.")
    for email in email_list:
        if bool(email) and is_valid_email(email):
            send_email_ses([email.strip()], "💸💼📝 Insur News Crew Update", format_news_for_email(final_analysis_output.pydantic.results, current_datetime))

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        message = (
            f"Attempt failed: {str(err)}"
        )
        print(json.dumps({"message": message, "severity": "ERROR"}))