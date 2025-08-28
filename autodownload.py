#!/bin/python3

"""
Grab files for a specific assignment


"""
import os, sys
from dotenv import load_dotenv
import logging
import requests
from argparse import ArgumentParser
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
parser.add_argument('assignment_id', type=int)
parser.add_argument('--class_id', type=int, default=DEFAULT_COURSE_ID)
parser.add_argument('--all_students', '-a', action="store_true")
parser.add_argument('--list_assignments', action="store_true")

def main():
    args = parser.parse_args()
    if (args.list_assignments):
        response = requests.get(
            f"{CANVAS_BASE_URL}/api/courses/{args.class_id}/assignments",
            headers={

            } 
        )
        print(response)

    pass    
    
    
    

if __name__ == "__main__":
    main()