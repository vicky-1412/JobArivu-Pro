import requests
from bs4 import BeautifulSoup

def fetch_jobs():
    # Example for Demonstration
    # Real-time-la Beautifulsoup vachi UPSC/TNPSC fetch pannalaam
    jobs = [
        {"Agency": "TNPSC", "Post": "Group 4 VAO", "Link": "https://tnpsc.gov.in", "Edu": "10th"},
        {"Agency": "SSC", "Post": "MTS Multi Tasking", "Link": "https://ssc.gov.in", "Edu": "10th"},
        {"Agency": "Banking", "Post": "IBPS PO Officer", "Link": "https://ibps.in", "Edu": "Degree"},
        {"Agency": "Railway", "Post": "RRB NTPC", "Link": "https://indianrailways.gov.in", "Edu": "12th"}
    ]
    return jobs