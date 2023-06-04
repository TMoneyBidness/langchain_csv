from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
import environ
import csv
import os

# env = environ.Env()
# environ.Env.read_env()
# API_KEY = env("apikey")

st.write("API_KEY:", st.secrets["apikey"]

def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = OpenAI(openai_api_key=API_KEY)

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)


def query_agent(agent, agent_context, describe_dataset, objectives, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        agent_context: This is the description of the strengths and purpose of the agent. Remember, you are a professional data scientist and data analysis agent.
        describe_dataset: This is the description of the dataset.
        objectives: The objectives of the analysis.
        query: The question/query to ask the agent about the data.

    Returns:
        The response from the agent as a string.
    """

    prompt = f"""
        You are DataFrameAI, the most advanced dataframe analysis agent on the planet. You are collaborating with a company to provide skilled, in-depth data analysis on a large table. They are looking to gain competitive business insights from this data in order to gain an edge over their competitors. They are looking to analyze trends, ratios, hidden insights, and more.

        Here is the context about the agent:

        {agent_context}: This is the description of the strengths and purpose of the agent. Remember, you are a professional data scientist and data analysis agent.
        {describe_dataset}: This is the description of the dataset.
        {objectives}: These are the objectives of the analysis.
        -----

        For the following query, if it requires drawing a table, reply as follows:
        {{"table": {{"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}}}

        If the query requires creating a bar chart, reply as follows:
        {{"bar": {{"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}}}

        If the query requires creating a line chart, reply as follows:
        {{"line": {{"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}}}

        There can only be two types of charts, "bar" and "line".

        If it is just asking a question that requires neither, reply as follows:
        {{"answer": "answer"}}
        Example:
        {{"answer": "The title with the highest rating is 'Gilead'"}}

        If you do not know the answer, reply as follows:
        {{"answer": "I do not know."}}

        Return all output as a string.

        All strings in "columns" list and data list should be in double quotes,

        For example: {{"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}}

        Let's think step by step.

        OUTPUT: Provide detailed, actionable insights. I am not looking for one or two sentences. I want a paragraph at least, including statistics, totals, etc. Be very specific and analyze multiple columns or rows against each other. Whatever is required to provide the most advanced information possible!

        Below is the query.

        Query: {query}
    """

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return str(response)



