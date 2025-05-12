# social-bingo
Socializing tool based off "Kennenlernbingo" as provided by CogSci students from TU Darmstadt. Generates tables to fill in by meeting new people.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/social-bingo.git
    cd social-bingo
    ```

2. Create a conda environment (optional but recommended):
    ```bash
    conda create --name social-bingo python=3.13
    conda activate social-bingo
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your input data:
    - Modify the `entries.json` file to include your custom bingo statements, title, and header.

2. Run the script to generate bingo sheets:
    ```bash
    python bingo.py
    ```

3. Follow the prompts to specify the number of bingo sheets to generate. The output will be saved as a PDF file (default: `sheets.pdf`).

## Development

This is a quick and dirty utility script done shortly before the event the project was built for.
Feel free to share your improvements to the code or fun additions to the list of entries via pull request.

## File Descriptions

- `bingo.py`: Main script to generate bingo sheets.
- `entries.json`: Contains the title, header, and statements for the bingo sheets.
- `requirements.txt`: Lists the dependencies required for the project.
- `README.md`: Documentation for the project.

## Acknowledgements

This script is a re-implementation of a social bingo created and provided for a cognitive science event at TU Darmstadt. Big thanks to the Cognitive Psyence Fachschaft there for doing that and for sending me the bingo entries.