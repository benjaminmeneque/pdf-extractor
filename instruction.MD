To set up a virtual environment, follow these steps:

1. **Create a Virtual Environment**: Open your terminal and run the following command to create a virtual environment named `.venv`:

    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment**: Depending on your operating system, you can activate the virtual environment. For Windows, run:

    ```bash
    .venv\Scripts\activate
    ```

    For macOS/Linux, run:

    ```bash
    source .venv/bin/activate
    ```

3. **Install Required Packages**: After activating the virtual environment, you can install the required packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Program**: To run the program, execute the following command in your terminal, replacing `"path"` with the actual path to the directory you want to scan:

    ```bash
    python task.py "path"
    ```

Replace `"path"` with the actual path to the directory you want to scan.
