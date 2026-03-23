# ADK Agent and MCP Toolbox For SQL Server Database

## Step 1: Install and configure MCP Toolbox
- To install Toolbox as a binary on Windows (Command Prompt):

    set VERSION=0.30.0
    
    curl -o toolbox.exe "https://storage.googleapis.com/genai-toolbox/v%VERSION%/windows/amd64/toolbox.exe"
- visit [installing-the-server](https://googleapis.github.io/genai-toolbox/dev/getting-started/introduction/#installing-the-server)
## Step 2: Launching Toolbox UI

    ./toolbox --ui
`INFO "Toolbox UI is up and running at: http://localhost:5000/ui"`

## Visit [Toolbox UI](https://googleapis.github.io/genai-toolbox/dev/getting-started/introduction/)


## Step 3: Connect agent to MCP Toolbox
    create .env file in my_agent directory 
    GOOGLE_GENAI_USE_VERTEXAI=0
    GOOGLE_API_KEY=
    
### 1- In a new terminal, install the SDK package.
`pip install google-adk[toolbox]`

### 2- Alternatively, serve it via a web interface:
`adk web --port 8000`