from github import Auth
from github import Github
import argparse
import os
import sys
import json

def create_branch(target_repo_name, source_branch, target_branch):
    repo = g.get_repo(target_repo_name)
    sb = repo.get_branch(source_branch)
    repo.create_git_ref(ref=f'refs/heads/{target_branch}', sha=sb.commit.sha)


def create_file(target_repo_name, target_branch, source_file):
    repo = g.get_repo(target_repo_name)
    with open(source_file) as file:
        data = file.read()
    repo.create_file(source_file, f"{source_file} created", data, branch=target_branch)


def create_pr(target_repo_name, source_branch, target_branch, title, body):
    repo = g.get_repo(target_repo_name)
    pr = repo.create_pull(base=source_branch, head=target_branch, title= title, body=body)


def main(args):
    ''' Method to getting the arguments and calling the copy_module function'''
    parser = argparse.ArgumentParser(description='File arguments for file creation in repos')
    parser.add_argument("--source_repo", help="source_repo")
    parser.add_argument("--target_branch", help="target_branch")
    parser.add_argument("--source_file", help="source_file")
    args = parser.parse_args()
    title = "Pr Title workflow Added "
    body = '''
    Added the github workflow for checking the PR Title
    '''
    with open('target_repos.json') as f:
        target_repo_list = json.load(f)
        
    for target_repo in target_repo_list:
        target_repo_name = "ruskinb1/" + target_repo["name"]
        target_repo_default_branch_name = target_repo["defaultBranchRef"]["name"]
        print(target_repo_name)
        print(target_repo_default_branch_name)
        
        create_branch(target_repo_name, target_repo_default_branch_name, args.target_branch)
        create_file(target_repo_name, args.target_branch, args.source_file)
        create_pr(target_repo_name, target_repo_default_branch_name, args.target_branch, title, body)

if __name__ == "__main__":
    token = os.environ["SECRET_TOKEN"]
    g = Github(token)
    main(sys.argv)
