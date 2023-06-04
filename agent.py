from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
import environ
import csv
import os

env = environ.Env()
environ.Env.read_env()

API_KEY = env("apikey")

def create_agent(filename: str, file_content: bytes):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The name of the CSV file that contains the data.
        file_content: The content of the CSV file as bytes.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = OpenAI(openai_api_key=API_KEY)

    # Save the file content to a temporary location
    temp_file_path = "temp.csv"
    with open(temp_file_path, "wb") as f:
        f.write(file_content)

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(temp_file_path, encoding='utf-8', error_bad_lines=False, quoting=csv.QUOTE_NONE)

    # Remove the temporary file
    os.remove(temp_file_path)

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


# Streamlit app code
import streamlit as st
import json

from agent import query_agent

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)

st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

uploaded_file = st.file_uploader("Upload a CSV")

describe_dataset = st.text_area("Please describe your dataset. What is it?")
objectives = st.text_area("Describe your objectives. For example, 'Provide ratios, outlying insights, and any actionable insights.'")
agent_context = st.text_area("Agent context prompt. e.g., 'You are skilled in transportation pattern analysis. You look for trends, ratios, and hidden insights in the data.'")
query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    # Check if a file is uploaded
    if uploaded_file is not None:
        # Get the filename and content of the uploaded file
        filename = uploaded_file.name
        file_content = uploaded_file.read()

        # Create an agent from the uploaded CSV file
        agent = create_agent(filename, file_content)

        # Query the agent
        response = query_agent(agent, agent_context, describe_dataset, objectives, query)

        # Decode the response
        decoded_response = decode_response(response)

        # Display the response
        st.write(decoded_response)
    else:
        st.write("Please upload a CSV file.")
