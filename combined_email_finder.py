# combined_email_finder.py

from emailfinder.core import processing
from io import StringIO
import sys
import requests
import re

from email_finder import find_emails
from emailfinder_wrapper import run_emailfinder

# FILTERING FUNCTION
def filter_emails(email_list):
    filtered_emails = [
        email for email in email_list if not (
            email.startswith(('22', 'u0027', 'jsmith', 'jdoe', 'jane.doe', 'First',
                              'John.Doe', 'FLast', 'doe', 'johnsmith', 'janedoe',
                              'Last', 'j-doe', 'LFirst', 'Jane.Doe', 'Doe',
                              'John_Smith', 'JSmith', 'JDoe', 'j_doe', 'J.Smith',
                              'JohnSmith', 'John_Doe', 'j.doe', 'Smith.John',
                              'jane@', 'd_jane', 'd-jane', 'jane_doe', 'jane.d', 'john.d'))            
        )
    ]

    cleaned_emails = []
    for email in filtered_emails:
        if email in filtered_emails:
            if email.startswith('u003'):
                email = email[4:]
            elif email.startswith('x3e'):
                email = email[3:]
            cleaned_emails.append(email)
        
    cleaned_emails = [email for email in cleaned_emails if not re.match(r'^[a-zA-Z]@', email)]
    return cleaned_emails

# METHOD COMBINATION

def get_combined_emails(domain):
    """
    Returns a merged, deduplicated list of emails from both methods
    """
    direct_emails = find_emails(domain)
    finder_emails = run_emailfinder(domain)

    all_emails = set(direct_emails) | set(finder_emails)
    valid_emails = filter_emails(all_emails)
    return valid_emails or ["No emails found."]

if __name__ == "__main__":
    emails = get_combined_emails("gunvorgroup.com")
    print("Found emails:")
    for email in emails:
        print (email)