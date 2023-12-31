# MiniBloggingApp using Python-Flask and mongo
> A backend API built using Python Flask and MongoDB for the database. This API can be consumed using the console application with setup predefined commands.
## Installation and Setup

### **Local Setup**

#### Required

- Python 3.7+
- Pip
- MongoDB
- Redis
    - instance running on localhost port 6379

1. Clone this repository and cd to the folder
    ```
        git clone https://github.com/hawkinswinja/MiniBloggingApp-test.git

        cd MiniBloggingApp-test
    ```
2. Create a virtual environment and activate it:
    ```
        python -m venv blog
        source venv/bin/activate # On Windows, use venv\Scripts\activate
    ```
3. Install the required packages
    ```
        pip install -r requirements.txt
    ```
4. Create an `.env` file with the following content
    ```
        MONGODB_URI=''
        MONGODB_DB=''
        URL='' # http://127.0.0.1:5000 (Flask app URL)
    ```

5. Setup the database and Redis:
    - MongoDB should be configured based on your `.env` file.
    - Ensure Redis points to `localhost` and port `6379`.
        - You can change it inside the `routes/__init__.py` file if needed.

6. Run the Flask app
    ```
        flask run
    ```

7. A success message on url `http://127.0.0.1:5000/status` indicates success

8. Access the documentation from the endpoint: `http://127.0.0.1:5000/apidocs`

### **The Containers way**
- Alternatively you can leverage the docker compose script which starts up the different services at once.
- cd into the repo directory
- Run the below command to spin up the application
    ```
        docker compose up -d
    ```
## Usage
- Run the console.py script in another tab (no need to use another tab if using docker compose)
- Type help to display commands and their usage
- CTRL + C is a keyboard interrupt and ends the program
- Upon login store the returned token as you'll need to pass it as an arg for most requests. 
    - Example of logging out the current user with token 12345678
    ```
    blog-app> logout 12345678
    ```
### Running tests (local setup)
-   ```
       python -m unittest discover tests
    ```



        



