from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from challenge_utils.ScriptBuilder import ScriptBuilder

# Constants
PROBLEM_NO = 100
CHALLENGE = "2024"
CHOSEN_LANGUAGE = "js"

AUTHOR = "Abbas Moosajee"

CONFIG_DICT = {
    "2024": ("2024", "AOC_2024.json"),
    "2023": ("2023", "AOC_2023.json"),
    "2022": ("2022", "AOC_2022.json"),
    "2021": ("2021", "AOC_2021.json"),
    "2020": ("2020", "AOC_2020.json"),
    "2019": ("2019", "AOC_2019.json"),
    "2018": ("2018", "AOC_2018.json"),
    "2017": ("2017", "AOC_2017.json"),
    "2016": ("2016", "AOC_2016.json"),
    "2015": ("2015", "AOC_2015.json"),
}

def main() -> None:
    """Main function to create challenge files."""

    repo_dir = Path(__file__).parent
    folder, config_file = CONFIG_DICT[CHALLENGE]
    challenge_dir = repo_dir / folder

    try:
        builder = ScriptBuilder(AUTHOR, challenge_dir, config_file)

        filepath = builder.create_files(
            prob_no=PROBLEM_NO,
            language=CHOSEN_LANGUAGE,
            txt_files=1,
        )

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()