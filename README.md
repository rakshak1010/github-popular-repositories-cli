# github-popular-repositories-cli

CLI program to fetch the most popular repositories of the given organization based on the number of forks and the top contributores in respective repositories based on their number of commits.


## Problem Statement
Find the **N** most popular repositories of a given organization on Github (Eg: [https://github.com/google](https://github.com/google)) based on the number of forks. For each such repo find the top **M** committees and their commit counts.

## Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- Package manager [pip](https://pip.pypa.io/en/stable/)

## Dependencies
- requests
- json

## Project Setup
- Clone the Repository to a folder
- Change your current working directory to the project folder
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements.

```bash
pip install -r requirements.txt
```
## Generate Github Personal Access Token
> **NOTE:** This is not a necessary step but GitHub allows only 60 unauthorised API calls in 1 hour which is very less for this program's purpose. To make authenticated calls we need to generate Personal Access Token to increase this limit to 5000

- Follow the steps mentioned here: [Creating a Personal Access Token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) 

## Usage

```bash
python github_popular_repositories.py
```
- The program prompts to enter the Github Personal Access Token, you can also skip this by simply pressing *ENTER*
- The user must now enter the name of the organization
- The program verifies the Organization name.
- If valid, the user is prompted to enter the Repo Count ('N') and the Committee Count ('M')
- The program checks if these are valid integers
- If valid, the program prints the list of most popular repositories along with their name and forks count and the list of top committees and their commit counts.

## Error Handling
In case of any error, the program stops after printing the error code and the error message.
- **400:** Bad Request, N and M must be integers
- **401:** Invalid Access Token
- **403:** API Rate Limit Exceeded
- **404:** Invalid Organization name

## License
[MIT](https://choosealicense.com/licenses/mit/)