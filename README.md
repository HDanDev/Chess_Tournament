# Chess Tournament Management System

This is a Chess Tournament Management System that allows you to manage players, tournaments, and results.

## Prerequisites

- Python 3.x installed
- PySide6 library installed (`pip install PySide6`)

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/HDanDev/Chess_Tournament.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Chess_Tournament
    ```

3. (Optional) Create and activate a virtual environment:

    ```bash
    py -m venv venv
    source venv/bin/activate      # On Linux or macOS
    .\venv\Scripts\activate       # On Windows
    ```

    Activating the virtual environment isolates your project dependencies.

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Program

Execute the following command to run the program:

```bash
py main.py
```

## Generating a Flake8 HTML Report

Installing flake8-html via pip:

```bash
pip install flake8 flake8-html
```

Run the flake8-html command line instruction to generate the desired files:

```bash
flake8 --max-line-length=119 --format=html --htmldir=flake8-report
```

Open the generated HTML report:

 ```bash
open flake8-report/index.html        # On macOS
start flake8-report/index.html       # On Windows
xdg-open flake8-report/index.html    # On Linux

