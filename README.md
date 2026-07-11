## How To Run

1. Download the Files.
2. In Firebase, go to **Settings**, and click **Service Accounts**.
3. Click generate new private key, and download it into the directory where the project is.
4. In the same directory, put the antibodies.csv file.
5. Create and run a Python Virtual Environment.
6. Download all dependencies with `pip install -r requirements.txt`
7. To run the API, use `uvicorn main:app --reload`, which will run it at `localhost:8000`.
