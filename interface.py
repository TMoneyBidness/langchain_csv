import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent


def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

describe_dataset = st.text_area("Please describe your dataset. What is it?")
objectives = st.text_area("Describe your objectives. For example, 'Provide ratios, outlying insights, and any actionable insights.'")
agent_context = st.text_area("Agent context prompt. ie. 'You are skilled in transportation pattern analysis. You look for trends, ratios, and hidden insights in the data.'")
query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    # Check if a file is uploaded
    if data is not None:
        # Create a temporary file to save the uploaded CSV
        with open("temp.csv", "wb") as f:
            f.write(data.getvalue())

        # Create an agent from the CSV file.
        agent = create_agent("temp.csv")

        # Query the agent.
        response = query_agent(agent=agent, query=query, describe_dataset=describe_dataset, objectives=objectives, agent_context=agent_context)

        # Decode the response.
        decoded_response = decode_response(response)

        # Write the response to the Streamlit app.
        write_response(decoded_response)

        # Remove the temporary file
        os.remove("temp.csv")
    else:
        st.write("Please upload a CSV file.")

