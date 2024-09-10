import csv
from bs4 import BeautifulSoup
import requests
import re
import time
from termcolor import colored
from gem import job



def remove_common_chars(string):
    # Replace the HTML character entities with their corresponding characters
    string = string.replace("&lt;", "")
    string = string.replace("&gt;", "")

    # Replace the closing tags with empty strings
    string = string.replace("&lt;/strong&gt;", "")
    string = string.replace("&lt;/u&gt;", "")
    string = string.replace("&lt;/li&gt;", "")
    string = string.replace("</li>", "")
    string = string.replace("<li>", "")
    string = string.replace("</strong>", "")
    string = string.replace("</u>", "")
    string = string.replace("</p>", "")
    string = string.replace("</b>", "")
    string = string.replace("</a>", "")
    string = string.replace("/p", "")
    string = string.replace("/", "")
    string = remove_before_substring(string, '"description":"strong')

    # Replace the remaining HTML elements with empty strings
    string = string.replace("&lt;br&gt;", "")
    string = string.replace("&lt;li&gt;", "")

    return string
def remove_before_substring(string, substring):
    # Partition the string around the substring
    if substring in string:
        _, _, after_substring = string.partition(substring)
        return after_substring
    return string  # If substring is not found, return the original string
def contains_experience_keywords(string, experience_keywords):
    string = string.lower()
    for keyword in experience_keywords:
        if keyword.lower() in string:
            return True
    return False

def get_links(url, num,big_num):
    delay=1
    if num > 45000:
        return
    print(f"Number of links to get: {num}")
    
    if num != 0:
        url += f"&start={num}"

    print(f"Getting links from: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Find all <a> tags and extract hrefs
    tags = soup.find_all('a')
    hrefs = [tag.get('href') for tag in tags if tag.get('href')]

    with open('jobPost.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write CSV header only once
        if num == 0:
            writer.writerow(['Link', 'Description'])

        for link in hrefs:
            if link.startswith("https://www.linkedin.com/jobs/"):
                print(f"Processing job link: {link}")
                job_page = requests.get(link)

                # Retry on failure
                if job_page.status_code >= 400:
                    print(colored("Error fetching job page, retrying...", 'red'))
                    time.sleep(10)
                    job_page = requests.get(link)

                if job_page.status_code == 200:
                    print(colored("Successfully fetched job page", 'green'))
                    sub_soup = BeautifulSoup(job_page.content, 'html.parser')
                    
                    # Find job description content
                    job_description_script = sub_soup.find("script", text=re.compile("description"))

                    if job_description_script:
                        # Extract text from script tag containing job description
                        job_description = job_description_script.get_text(strip=True)
                        job_description = remove_common_chars(job_description)
                        
                     
        
                    if (not job(job_description)):
                        print(colored(f"Skipping job with experience requirement: {link}", 'yellow'))
                        with open('fakeJobs.txt', 'a') as file2:
                            file2.write(link+":"+job_description+"\n")
                            continue
                        ...
                        # Save valid job link and description to CSV file
                    print(colored(f"Valid job saved: {link}", 'green'))
                    writer = csv.writer(file)
                    writer.writerow([link,job_description])

    
    import random

    num += 25
    delay = random.uniform(0.5, 2.0)  # Random delay between 0.5 and 2 seconds
    if num < big_num:
        big_num+=500
        print(colored("tottaly not suspisous nap, whaaaa whats webscraping","blue"))

        time.sleep(num * delay)
        get_links(url, num,big_num)
    else:
        print(colored("tottaly not suspisous nap, whaaaa whats webscraping","purple"))
        time.sleep(150)  # Longer delay after a large batch
        get_links(url, num,big_num)
# Start scraping from the given URL
get_links(
"https://www.linkedin.com/jobs/search/?currentJobId=3978890270&distance=25&f_E=2%2C3&geoId=103644278&keywords=entry%20level%20software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true",    0,500
)
