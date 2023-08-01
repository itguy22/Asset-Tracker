Asset-Tracker
Asset Tracker is a web application created using Python, Flask for the backend, and HTML/CSS for the frontend. It is designed for Managed Service Providers (MSPs) and IT departments, allowing them to track various assets such as hardware and software licenses.

Installation
To install the app and its dependencies, follow these steps:

Prerequisites
Ensure Python 3.6+ is installed on your system. You can download it from the official Python website.
You need pip installed. If you have Python 3.6+, pip should have been installed with it. If not, you can follow the instructions from the pip installation guide.

Steps
Clone the repository:
Clone the Asset-Tracker repository to your local machine using the following command:

bash
Copy code
git clone <repository-url>
Replace <repository-url> with the URL of this repository.

Create a virtual environment (Optional but Recommended):
Create a new Python virtual environment to manage the dependencies for this project. You can use venv module which is included in standard Python distribution:

bash
Copy code
python3 -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy code
.\venv\Scripts\activate
On Unix or MacOS:
bash
Copy code
source venv/bin/activate
Install dependencies:
Navigate to the root directory of the project (where the requirements.txt file is located), and run the following command to install the necessary packages:

bash
Copy code
pip install -r requirements.txt
Running the Application
After installing, you can run the app in one of two ways:

Debug mode: Use the following command to run the app in debug mode:

bash
Copy code
python run.py
Standard mode: Use the following command to run the Flask app in standard mode:

bash
Copy code
flask run
Now, open your web browser and navigate to localhost:5000 to see the application running.

Enjoy using Asset Tracker! If you encounter any problems or have any suggestions, feel free to open an issue on the repository.
