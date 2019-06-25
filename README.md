# robo-advisor
Stock Information

## Setup

### Repo Setup
Create a new repository on Github for this program, or fork this one, and be sure to include a README and .gitignore file. 

### Environment Setup
Use Anaconda to create a new virtual environment for this program. Be sure to use Python Version 3.7.

After you have activated your virtual environment, utilize Pip to install requirements.txt. 

### .env and API Setup
To utilize the Robo-Advisor, you must create and receive your personal API Key from Alphadvantage, here: https://www.alphavantage.co/

After you have acquired your API Key, create a local .env file in your root and save your API Key with the following variable name:
```
ALPHADVANTAGE_API_KEY
```

Be sure to use this variable name exactly, as the Robo-Advisor will look for this variable to call the Alphadvantage API.

Also be sure that your .gitignore file is setup to ignore your .env files. This is the default when choosing a Python .gitignore with a new repository on GitHub.