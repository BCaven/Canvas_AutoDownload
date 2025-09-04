#!/bin/python3

"""
Grab files for a specific assignment


"""
import os, sys
from dotenv import load_dotenv
import logging
import requests
from argparse import ArgumentParser
import json

load_dotenv()
API_KEY = os.getenv("CANVAS_API_KEY")
if not API_KEY:
    logging.warning("API key was not found in the environment")
    sys.exit(1)
DEFAULT_COURSE_ID = os.getenv("COURSE_ID")
if not DEFAULT_COURSE_ID:
    # if there is not a course id in the environment, setting it to -1
    DEFAULT_COURSE_ID = -1
CANVAS_BASE_URL = os.getenv("CANVAS_URL")
if not CANVAS_BASE_URL:
    logging.warning("Canvas url not found in environment")
    sys.exit(1)

parser = ArgumentParser(
            prog='autodownload.py',
            description='Download files from canvas',
            epilog='Designed for downloading submissions on assignments')
parser.add_argument('assignment_id', type=str, default="-1")
parser.add_argument('--id', action="store_true")
parser.add_argument('--class_id', type=str, default=DEFAULT_COURSE_ID)
parser.add_argument('--all_students', '-a', action="store_true")
parser.add_argument('--list_assignments', action="store_true")
parser.add_argument('--list_courses', action="store_true")

def main():
    args = parser.parse_args()
    uri = f"{CANVAS_BASE_URL}/api/graphql"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    if args.list_courses:
        query = {
            'query': 'query GetClasses {allCourses {id, name}}'
        }
        response = requests.post(
            uri,
            headers=headers,
            json=query
        )
        response_dict = json.loads(response.text)
        if 'error' in response_dict:
            print(response_dict)
        else:
            for item in response_dict['data']['allCourses']:
                print(f"{item['name']} - id: {item['id']}")

    if args.list_assignments:
        query = {
            'query': "query GetAllAssignments { node(id: \"%s\") { ... on Course { id, name, assignmentsConnection { nodes { name, id, dueAt, gradedSubmissionsExist } } } } }" % args.class_id
        }
        response = requests.post(
            uri,
            headers=headers,
            json=query
        )
        response_dict = json.loads(response.text)
        if 'error' in response_dict:
            print(response_dict)
        else:
            for item in response_dict['data']['node']['assignmentsConnection']['nodes']:
                if not item['gradedSubmissionsExist']:
                    print(f"{item['name']} - id: {item['id']}")
    
    found_id = args.assignment_id
    if args.assignment_id != "-1" and not args.id:
        # get assignment by its human name
        query = {
            'query': "query GetAllAssignments { node(id: \"%s\") { ... on Course { id, name, assignmentsConnection { nodes { name, id, dueAt, gradedSubmissionsExist } } } } }" % args.class_id
        }
        response = requests.post(
            uri,
            headers=headers,
            json=query
        )
        response_dict = json.loads(response.text)
        if 'error' in response_dict:
            print(response_dict)
        else:
            for item in response_dict['data']['node']['assignmentsConnection']['nodes']:
                if item['name'] == args.assignment_id:
                    found_id = item['id']
                    break
        if found_id == args.assignment_id:
            logging.error("Did not find assignment {args.assignment_id} in {response_dict['data']['node']['name']}")
            return
        # then do the query like normal

    if found_id != "-1":
        query = {
            'query': "query MyQuery {  node(id: %s) { ... on Assignment { id, name, submissionsConnection { nodes { id, attachment { url } } } } } }" % args.class_id
        }
        response = requests.post(
            uri,
            headers=headers,
            json=query
        )
        response_dict = json.loads(response.text)
        if 'error' in response_dict:
            print(response_dict)
        else:
            for item in response_dict['data']['node']['submissionsConnection']['nodes']:
                print(item)
                # TODO: grab url for file(s) and download with student id included in file
    
    
    

if __name__ == "__main__":
    main()