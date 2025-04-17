# emailfinder_wrapper.py

from emailfinder.core import processing
from io import StringIO
import sys
import re

def run_emailfinder(domain):
    # Redirect stdout temporarily
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    results = []

    try:
        processing(domain, proxies=None)
        output = mystdout.getvalue()
        results = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", output)
    except Exception as e:
        results = [f"EmailFinder error: {e}"]
    
    finally:
        sys.stdout = old_stdout

    return results