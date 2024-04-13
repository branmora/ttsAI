# ttsAI
TTS for AI using LLMs endpoints.

## How to Use

To set up and use this project run python version 3.10.14 and follow the steps below:

### 1. Create an `.env` file
Create a `.env` file in the project root directory to store Open AI Keys and endpoints. Add the following variables to it:

```plaintext
ELEVEN_LABS_SECRET_KEY=your_api_key_here
OPEN_AI_SECRET_KEY=your_api_key_here
```

### 2. Create a Configuration File
Create a `config.yaml` file  to maintain path settings. Include the following configurations

```
recording_path: 'your_data_path_here'
output_path: 'your_output_path_here'
eleven_labs_voice_id: 'voice_id_here'
eleven_labs_model: 'model_name_here'
eleven_labs_api_key: ${ELEVEN_LABS_SECRET_KEY}
openai_model: 'model_name_here'
openai_api_key: ${OPEN_AI_SECRET_KEY}
```

### 3. Install Required Libraries
Install the necessary Python libraries using conda. Run `conda env create -f environment.yml`

### 4. Run the Classification Script
Execute the python script `main.py`. 