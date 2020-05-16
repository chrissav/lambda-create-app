import json
import os

from github import Github


git_token = os.getenv('GITHUB_TOKEN')
github = Github(git_token)
chrissav = github.get_user()


def create_repo(event, context):
  repo_name = event['app_name']

  try:
    result = chrissav.create_repo(repo_name)
  except Exception as e:
    result = str(e.data)

  return {
      "statusCode": 200,
      "headers": {
          "Access-Control-Allow-Origin": "http://localhost:3000",
      },
      "body": json.dumps({
          "message": result,
      }),
  }


def get_all_repos(user):
  try:
    repos = user.get_repos(affiliation='owner')
  except Exception as e:
    return e

  data = []
  for repo in repos:
    data.append(repo.raw_data)

  return data


def lambda_handler(event, context):
  repos = get_all_repos(chrissav)

  return {
      "statusCode": 200,
      "headers": {
          "Access-Control-Allow-Origin": "http://localhost:3000",
      },
      "body": json.dumps({
          "message": repos,
      }),
  }
