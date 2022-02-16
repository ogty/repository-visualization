import ast
import json
from typing import List, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, HTTPError


class LambdaException(Exception):
    
    def __init__(self, status_code: int, error_message: str) -> None:
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        return {
            "statusCode": self.status_code,
            "errorMessage": self.error_message
        }

class GenerateTree:
    
    def __init__(self, username: str, repository_name: str, default_branch: str) -> None:
        self.username = username
        self.repository_name = repository_name
        self.default_branch = default_branch

    def tmp(self) -> List[str]:
        pass

    def scraping(self) -> List[str]:
        repository_path = f"/{self.username}/{self.repository_name}"
        url = urljoin("https://github.com/", repository_path)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        paths_for_repository = [i.get("href") for i in soup.find_all("a")]
        
        blob_path = f"{repository_path}/blob/{self.default_branch}/"
        tree_path = f"{repository_path}/tree/{self.default_branch}/"

        result = []
        for url in paths_for_repository: 
            if url.startswith(blob_path) or url.startswith(tree_path):
                if url.count("/") == 5:
                    result.append(url)

        return result
    
    def __call__(self) -> Dict[str]:
        pass


def lambda_handler(event, content):
    data = ast.literal_eval(event["body"])
    username = data["userName"]
    repository_name = data["repositoryName"]

    response = requests.get('https://api.github.com/users/ogty/requirements.txt-generator')
    try:
        response.raise_for_status()
    except HTTPError as e:
        raise LambdaException(403, str(e))
    except RequestException as e:
        raise LambdaException(404, str(e))
    else:
        data = response.json()
        default_branch = data[0]["default_branch"]
        GenerateTree(username, repository_name, default_branch)
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dump()
        }

if __name__ == "__main__":
    print(GenerateTree("ogty", "requirements.txt-generator", "master").scraping())
