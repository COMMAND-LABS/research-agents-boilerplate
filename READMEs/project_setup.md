# TLDR

Recording the steps of setting up the project from scratch based on the https://github.com/thaddavis/research-agents-supercharged repo

## Step 1

```sh
python3 --version # 3.13.1
pyenv -v # 2.5.0
pyenv global 3.12.8
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv init
uv run hello.py
rm hello.py
```

## Scaffold out project structure

Behold the organization!

```sh
mkdir config # for holding some of our configuration
mkdir helpers # we will put the more useful functions powering our application here
mkdir prompts # here is where we will store most of our A.I. prompts
mkdir pydantic_types # Pydantic is a tool that allows us to specify the data our application will handle and provides us with feature for making sure our code aligns with the data we expect to pass through our application. We will store most of the Pydantic related code we write here
mkdir test # not of particular importance but if we wanted to write code for testing our application in an automated manner we would put it here
mkdir tools # Here is where we will put the code that defines the "tools" our Agents can use
```

Gorgeous!

## Flesh out the project files

```sh
touch config/agents.yaml # populate
# FYI: https://docs.crewai.com/concepts/agents
touch config/tasks.yaml # populate
# FYI: https://docs.crewai.com/concepts/tasks
touch helpers/execute_task_async.py
touch helpers/format_news_for_email.py
touch helpers/is_valid_email.py
touch helpers/send_email_ses.py
# populate the helper functions now
touch pydantic_types/news_results.py
# populate the pydantic-related functions now 
# REFLECT on the "NewsResults" data type
touch tools/url_qa.py
touch tools/custom_scrape_website.py
# populate the pydantic-related functions now 
touch prompts/analyst_task_description_tmplt.py
touch prompts/research_task_description_tmplt.py
# populate the prompt templates
touch main.py # finally the main.py
```

## Install PyPI packages

```sh
uv add agentops crewai crewai-tools pydantic boto3 python-dotenv
```

## Final setup - Non-default LLM, OPENAI_API_KEY, AGENTOPS_API_KEY

- https://platform.openai.com/docs/overview
- `touch .env`
- `echo "OPENAI_API_KEY=" >> .env`
- `echo "AGENTOPS_API_KEY=" >> .env`
- `echo "MAILING_LIST=" >> .env`
- `echo "AWS_REGION=" >> .env`
- `echo "AWS_ACCESS_KEY_ID=" >> .env`
- `echo "AWS_SECRET_KEY=" >> .env`
- https://platform.openai.com/settings/organization/api-keys
- https://docs.crewai.com/concepts/llms
- https://docs.litellm.ai/docs/providers/openai

## Test running the application

- `uv run main.py` # WORKS √

## .gitignore

```.gitignore
.env
agentops.log
```