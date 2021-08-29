# Caato+ to Tim Translator

Utility to convert exported CSV data from [Caato+](https://www.caato.de/timetracker+), to a compatible JSON format for [Tim](https://tim.neat.software/).

**This is not an official script, use at your own risk.*

## Usage

Export some data from Caato+ using *commas* `,` as delimiters.

Using Python 3, run the script in a Terminal, passing the exported Caato+ `.csv` file as an argument. e.g.: `python3 caatoToTimTranslator.py All-Projects-All-time.csv`

- **Folders** will be *disregarded*.
- **Projects** will be converted to **Groups**
- **Activities** will be converted to **Tasks**.

The script will **print** the **JSON** output to console. To _save_ it to a file you can redirect the standard output to a file using: `python3 caatoToTimTranslator.py All-Projects-All-time.csv > All-Projects-All-time.json`
