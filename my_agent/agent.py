from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.toolbox_toolset import ToolboxToolset

# --- Constants ---
GEMINI_MODEL = "gemini-2.5-flash"

# Assuming toolset is defined as in your snippet
# Ensure "execute-query" is added to your toolset server
toolset = ToolboxToolset(
    server_url="http://127.0.0.1:5000",
    toolset_name="admin" 
)

validate_information_agent = LlmAgent(
    name="validate_informationAgent",
    model=GEMINI_MODEL,
    instruction="""
    Your goal is to identify which fields are required to create a new record.
    
    1. Use 'list-tables' to find the correct table.
    2. Use 'get-table-schema' to inspect the columns.
    3. IMPORTANT: If a column has IS_IDENTITY = 1, it is auto-incremented by the database. 
       - NEVER ask the user for this value.
       - NEVER include this column in the data collection.
    4. Only ask the user for columns where IS_NULLABLE = 'NO' AND IS_IDENTITY = 0.
    5. Collect any optional columns (IS_NULLABLE = 'YES') if the user provides them, but do not require them.
    6. Once all non-identity required fields are gathered, pass the JSON object to the next agent.
    """,
    description="Identifies required fields while skipping auto-increment/identity columns.",
    output_key="validated_user_data",
    tools=[toolset],
)

add_user_agent = LlmAgent(
    name="add_userAgent",
    model=GEMINI_MODEL,
    instruction="""
    You will receive a JSON object representing user data from the previous agent.
    1. Identify the target table name.
    2. Construct a valid SQL INSERT statement using the keys and values provided.
    3. Use the 'execute-query' tool to insert this record into the database.
    4. Confirm to the user once the database operation is successful.
    """,
    description="Takes validated data and performs the SQL insertion.",
    output_key="final_confirmation",
    tools=[toolset],
)

# The pipeline that coordinates the flow
admin_pipeline = SequentialAgent(
    name="AdminPipelineAgent",
    sub_agents=[validate_information_agent, add_user_agent],
    description="Executes a sequence: discover schema, collect user info, and insert into DB.",
)

root_agent = admin_pipeline

