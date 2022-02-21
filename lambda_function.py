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

    def __init__(self, username: str, repository_name: str, repository_path: str, default_branch: str) -> None:
        self.username = username
        self.repository_name = repository_name
        self.repository_path = repository_path
        self.default_branch = default_branch

        self.folders = []

        files_or_folders = self.get_first_level_files_or_folders()
        for file_or_folder in files_or_folders:
            self.below_second_level(file_or_folder)

    def below_second_level(self, path: str) -> None:
        file_or_folder = path \
            .replace(f"{self.repository_path}/blob/{self.default_branch}/", "") \
            .replace(f"{self.repository_path}/tree/{self.default_branch}/", "") \

        result = {
            "name": file_or_folder,
            "files": []
        }

        blob_or_tree_path = path \
            .replace(f"{self.repository_path}/tree", self.repository_path) \
            .replace(f"{self.repository_path}/blob", self.repository_path) \
            .split("/")

        blob_path = blob_or_tree_path.copy()
        tree_path = blob_or_tree_path.copy()

        blob_path.insert(3, "blob")
        tree_path.insert(3, "tree")

        blob_path = "/".join(blob_path)
        tree_path = "/".join(tree_path)

        html = requests.get(urljoin("https://github.com/", path))
        soup = BeautifulSoup(html.content, "html.parser")
        paths_for_repository = [i.get("href") for i in soup.find_all("a")]

        process = [f"url.startswith('{i}')" for i in [blob_path, tree_path]]
        process_word = " or ".join(process)
        next_paths = []
        for url in paths_for_repository:
            if eval(process_word):
                if not url.startswith(path):
                    result["files"].append({"name": url.split("/")[-1]})
                    next_paths.append(url)
                elif "/" in url.replace(path, ""):
                    result["files"].append({"name": url.split("/")[-1]})
                    next_paths.append(url)

        parent = path.split(
            "/")[-2] if path.split("/")[-2] != self.default_branch else self.repository_name
        if parent == self.repository_name:
            if not result["files"]:
                result.pop("files")
            self.folders.append(result)
        else:
            if not result["files"]:
                result.pop("files")
            else:
                self.folders.append(result)

        for next_path in next_paths:
            self.below_second_level(next_path)

    def get_first_level_files_or_folders(self) -> List[str]:
        url = urljoin("https://github.com/", self.repository_path)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        paths_for_repository = [i.get("href") for i in soup.find_all("a")]

        process = [
            f"url.startswith('{self.repository_path}/{i}/{self.default_branch}')" for i in ["blob", "tree"]]
        process_word = " or ".join(process)

        result = set()
        for url in paths_for_repository:
            if eval(process_word):
                if url.count("/") == 5:
                    result.add(url)

        return result

    def __call__(self) -> Dict[str, list]:
        for parents in self.folders:
            for search_target in self.folders:
                if search_target["name"].startswith(f"{parents['name']}/"):
                    count = 0
                    child = search_target["name"].split("/")[-1]
                    for parent in parents["files"]:
                        if parent["name"] == child:
                            parents["files"].pop(count)
                        count += 1

                    parents["files"].append({
                        "name": child,
                        "files": search_target["files"]
                    })

        self.folders = list(
            filter(lambda x: not "/" in x["name"], self.folders))

        return {
            self.repository_name: self.folders
        }


def lambda_handler(event, content):
    data = ast.literal_eval(event["body"])
    username = data["userName"]
    repository_name = data["repositoryName"]
    repository_path = f"/{username}/{repository_name}"

    response = requests.get(
        urljoin("https://api.github.com/users/", repository_path))

    try:
        response.raise_for_status()
    except HTTPError as e:
        raise LambdaException(403, str(e))
    except RequestException as e:
        raise LambdaException(404, str(e))
    else:
        data = response.json()
        default_branch = data[0]["default_branch"]
        body_cotent = GenerateTree(
            username, repository_name, repository_path, default_branch)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps(body_cotent)
        }


if __name__ == "__main__":
    import pprint
    import time

    start = time.time()
    result = GenerateTree("ogty", "requirements.txt-generator",
                          "/ogty/requirements.txt-generator", "master")
    pprint.pprint(result())
    print(time.time() - start)
