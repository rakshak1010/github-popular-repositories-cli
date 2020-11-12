import requests
import json


class GitHubPopularRepositories:
    # initialsing URL values
    def __init__(self, access_token):
        self.github_url = "https://api.github.com/"
        self.org_url = "orgs/"
        self.search_repo_url = "search/repositories"
        self.access_token = access_token

    # generate URL to verify organization
    def generate_valid_organization_url(self, organization):
        return (
            self.github_url
            + self.org_url
            + organization
            + "?access_token="
            + self.access_token
        )

    # generate URL to fetch most popular repositories
    def generate_popular_repo_url(self, organization, sort_on, page):
        return (
            self.github_url
            + self.search_repo_url
            + "?q=user:"
            + organization
            + "&sort="
            + sort_on
            + "&page="
            + str(page)
            + "&access_token="
            + self.access_token
        )

    # generate URL to fetch top committees
    def generate_top_committee_url(self, repo_id, page):
        return (
            self.github_url
            + "repositories/"
            + str(repo_id)
            + "/contributors"
            + "?page="
            + str(page)
            + "&access_token="
            + self.access_token
        )

    # to check if organization is valid
    def is_valid_organization(self, organization):
        url = self.generate_valid_organization_url(organization)
        print("Verifying Organization URL: " + url)
        response = requests.get(url)
        print("Status Code: ", response.status_code)
        return response.status_code  # To check the status code of response

    # To get the top 'n' repositories sorted on the number of forks
    def get_popular_repositories(self, organization, sort_on, repo_count):
        results = []  # initialise an empty results list
        page = 1  # intialise the query page
        # keep fetching until we find desired results OR no more repos exist
        while True:
            repo_url = self.generate_popular_repo_url(organization, sort_on, page)
            print("Fetching repository results from: " + repo_url)
            response = requests.get(repo_url)
            repo_json_response = json.loads(response.text)
            # exit if no more repos present
            if len(repo_json_response["items"]) == 0:
                print("<---- No more repositories found ---->\n")
                break
            for repo in repo_json_response["items"]:
                results.append((repo["id"], repo["name"], repo["forks"]))
                # exit when top 'n' repos found
                if len(results) == repo_count:
                    return results
            page += 1
        return results

    # To get the top 'm' committees
    def get_top_committees(self, repo_id, committee_count):
        results = []  # initialise an empty results list
        page = 1  # intialise the query page
        # keep fetching until we find desired results OR no more committees exist
        while True:
            committee_url = self.generate_top_committee_url(repo_id, page)
            print("Fetching committee results from: " + committee_url)
            response = requests.get(committee_url)
            contributors_json_response = json.loads(response.text)
            # exit if no more committees present
            if len(contributors_json_response) == 0:
                print("<---- No more committees found ---->")
                break
            for contributor in contributors_json_response:
                results.append((contributor["login"], contributor["contributions"]))
                # exit when top 'm' committees found
                if len(results) == committee_count:
                    return results
            page += 1
        return results


def printError(response_code):
    print("\n-----------------------")
    print("Error: ", response_code)
    if response_code == 401:  # invalid access code
        print("Unauthorized: Invalid Access Code")
    elif response_code == 403:  # rate limit exceed
        print("Forbidden: API Rate Limit Exceeded")
    elif response_code == 400:  # bad request
        print("Bad Request: 'N' and 'M' must be integers")
    else:  # invalid organization
        print("Not Found: Invalid Organization.")
    print("-----------------------\n")


if __name__ == "__main__":
    access_token = input(
        "Enter the GitHub API access token (Press ENTER to proceed without an access token):  "
    )
    organization_name = input("Enter the organization name:  ")
    organization_name = organization_name.lower()

    # initialise the class
    fetch_repositories = GitHubPopularRepositories(access_token)

    # if org name is valid then fetch repos
    response_code = fetch_repositories.is_valid_organization(organization_name)
    if response_code == 200:
        print(organization_name + " is a valid organization.\n")

        # input repo_count (n) & committee_count (m)
        repo_count = input("Enter the number of repositories (n):  ")
        committee_count = input("Enter the number of committees per repository (m):  ")
        print()

        # check for valid inputs of 'n' and 'm'
        if not repo_count.isnumeric() or not committee_count.isnumeric():
            printError(400)
            exit()

        sort_on = "forks"  # define the sorting parameter for repositories

        # list of popular repositories
        popular_repos_org = fetch_repositories.get_popular_repositories(
            organization_name, sort_on, int(repo_count)
        )
        print(
            "Top "
            + repo_count
            + " most popular repositories of "
            + organization_name
            + " and their fork counts:"
        )
        repos_iterator = 1
        for repo in popular_repos_org:
            print(str(repos_iterator) + ". Repository Name: ", repo[1])
            repos_iterator += 1
            print("Forks Count: ", repo[2])
            print()
            # list of top committees in respective repositories
            top_committees = fetch_repositories.get_top_committees(
                repo[0], int(committee_count)
            )
            print(
                "\nTop "
                + committee_count
                + " most popular committees and their respective commit counts:"
            )
            committees_iterator = 1
            for committee in top_committees:
                print(
                    str(committees_iterator)
                    + ". "
                    + str(committee[0])
                    + " -> "
                    + str(committee[1])
                )
                committees_iterator += 1
            print("\n-----------------------------------------------------------------")
            print("-----------------------------------------------------------------\n")
    else:
        printError(response_code)
