#!/bin/python3

"""
Grab files for a specific assignment


"""
import os, sys
from dotenv import load_dotenv
import logging

def main():
    load_dotenv()
    API_KEY = os.getenv("CANVAS_API_KEY")
    if not API_KEY:
        logging.warning("API key was not found in the environment")
        sys.exit(1)
    
    

if __name__ == "__main__":
    main()