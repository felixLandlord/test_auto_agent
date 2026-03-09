# test_auto_agent

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/felixLandlord/test_auto_agent.git
   ```

2. Navigate to the project directory:
   ```bash
   cd test_auto_agent
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Project

1. Run API
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

**note: no env file is required for this project**