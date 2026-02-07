# Manzai Generator Project

This project utilizes Python and Claude AI agents to generate manzai (Japanese stand-up comedy) performances. It also incorporates audio synthesis using AWS Polly for generating speech from text.

## Main Files

1. **manzai.py**: This is the main script that handles the generation of manzai performances. It integrates with Claude AI to create comedic dialogue and sketches.
2. **generate.py**: This file is responsible for initiating the generation process and managing the overall workflow of the project, calling functions from `manzai.py` as needed.
3. **manzai_script.txt**: This text file serves as storage for the generated manzai scripts, allowing users to review and modify the output as necessary.

## How to Use

1. **Clone the Repository**: Start by cloning the repository to your local machine.
   ```bash
   git clone https://github.com/zzzzico12/qiita-manzai.git
   cd qiita-manzai
   ```

2. **Install Required Packages**: Ensure you have all necessary Python packages installed. You may need to set up a virtual environment and install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Generator**: Execute the `generate.py` script to start generating manzai performances.
   ```bash
   python generate.py
   ```

4. **Listen to the Performance**: After the script has completed, use the audio files generated alongside the manzai scripts to listen to the performances created by AWS Polly.

Feel free to modify the scripts as necessary to tailor the performances to your liking!