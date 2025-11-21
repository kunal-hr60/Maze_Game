# main.py

A compact Python utility to generate and solve mazes. This README describes purpose, requirements, installation, usage, and basic options so you can run or integrate main.py quickly.

## Overview
main.py generates rectangular mazes and can optionally solve them. It supports exporting mazes as ASCII or image files and includes at least one configurable solver.

## Features
- Generate perfect mazes (no loops) for given width/height
- Solve mazes and output the solution path
- ASCII and basic image export (PNG)
- Command-line usage for quick testing or integration

## Installation
1. Place `main.py` in your project folder.
2. (Optional) Create a virtual environment and install requirements:
    - python -m venv venv
    - source venv/bin/activate  (Windows: venv\Scripts\activate)
    - pip install pillow

## Usage
Basic command-line patterns (adjust flags to match the script's actual options):

Generate a maze and print ASCII:
```
python main.py --generate --width 20 --height 10 --format ascii
```

Generate a maze and save a PNG:
```
python main.py --generate --width 50 --height 30 --format png --output maze.png
```

Generate and solve using default solver:
```
python main.py --generate --width 20 --height 10 --solve --format ascii
```

Common flags (example; adapt to script):
- --generate           Generate a new maze
- --width N --height M Size of the maze in cells
- --solve              Solve the generated maze
- --format [ascii|png] Output format
- --output FILE        Output filename for images
- --seed N             Reproducible generation

## Algorithm notes
Typical implementations use depth-first search (recursive backtracker) or union-find for generation and BFS/A* for solving. Adjust parameters to trade off complexity and path characteristics.

## Examples
Example ASCII output (small):
```
+---+---+---+
| S     |   |
+   +---+   +
|   |   | E |
+---+---+---+
```

## Contributing
- Open issues for bugs or feature requests.
- Submit pull requests with tests and brief description.

## License
MIT License — include LICENSE file as needed.

## Contact
For questions or bug reports, open an issue on the repository or add a short description at the top of the script.

Save this content as README.md next to main.py.
