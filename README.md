# Welcome to Architect, a CustomNPCs Script Generator 
Architect is a fully customizable program that leverages the power of LangChain and OpenAI to generate scripts for CustomNPCs 1.12.2. This tool is designed to assist Minecraft modders in creating scripts for NPCs, blocks, and other entities within the game.

## Setup and Usage
To get started with this tool, follow these simple steps:

1. Fork this repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a .env file in the root directory of the project with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```

5. Run the script.py file:
```
python script.py
```

6. Open your web browser and navigate to the localhost link provided in the terminal (usually http://127.0.0.1:5000/).


## Capabilities 
This tool is optimized for generating beginner to intermediate level scripts and can also assist in debugging more advanced scripts. When using the tool, ensure that you provide precise prompts to the model to generate and debug scripts effectively.


## Why did I make this? 
Currently, you can copy/paste some example scripts into ChatGPT or some other AI model and ask it to generate a script based on those examples, with decent success. This tool offers a more powerful alternative, as you have control over many aspects of the NLP process: you can customize how the PDF is split into chunks, how big those chunks are, how the similarity search works, the vectorizations process, you can even change the AI model if you'd like. You have a lot of control over how exactly the AI will process and respond to the context of your data, not to mention you can provide it a lot more data, an amount that greatly exceeds the current context window of all AI models. 