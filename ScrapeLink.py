from bs4 import BeautifulSoup
import requests
import re
from termcolor import colored
from urllib3 import response
import time
import fileinput

ids = []


def remove_before_substring(string, substring):
    # Partition the string around the substring
    _, _, after_substring = string.partition(substring)
    return after_substring


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


def contains_keyword(keywords, string):
    # make keywords all lowercase
    keywords = [keyword.lower() for keyword in keywords]
    # make string all lowercase
    string = string.lower()
    for keyword in keywords:
        if keyword in string:
            print(keyword + "found")
            return True
    print("no" + keywords[0] + "found")
    return False


def customLogic(Masters, BA, String):
    if contains_keyword(Masters, String):
        print("Masters FOUND LOOKING FOR BA")
        if contains_keyword(BA, String):
            print("BA FOUND")
            return True
        else:
            print("BA NOT FOUND")
            return False
    else:
        print("Masters NOT FOUND")
        return True


def getLinks(url, num):
    if (num > 450):
        return
    base_url = "https://www.linkedin.com/jobs/search/?currentJobId=3409431417&f_E=1&f_WT=2&geoId=103644278&keywords=computer%20science%20internship&location=United%20States&refresh=true"
    print("Number of links to get: " + str(num))
    if (num != 0):
        numStr = str(num)
        url = base_url + "&start=" + (numStr)
    print("Getting links from: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    strys = soup.find_all(["a", "b", "data-control-id"])
    tags = soup.find_all('a')
    hrefs = [tag.get('href') for tag in tags]
    for i in hrefs:
        if i is not None:
            substring = i[:30]
            if (substring == "https://www.linkedin.com/jobs/" and i):
                JobPage = requests.get(i)

                x = (JobPage.status_code)
                if (int(x) >= 400):
                    print(colored("Error", 'red'))
                    time.sleep(3)
                    JobPage = requests.get(i)
                else:
                    print(colored("Success", 'green'))

                    print("Updated response code: ", x)
                subSoup = BeautifulSoup(JobPage.content, 'html.parser')
                subStr = subSoup.find_all('div', {
                    'class': 'jobs-description__content jobs-description-content jobs-description__content--condensed'})
                strys = (subSoup.find_all("script"))

                cs_keywords = [
                    "computer science",
                    "Algorithms",
                    "C++",
                    "Data structures",
                    "Java",
                    "Python",
                    "Software development",
                    "HTML/CSS",
                    "JavaScript",
                    "Mobile app development",
                    "Scrum",
                    "SQL",
                    "Node",
                    "React",
                    "Flask",
                    "HTML",
                    "CSS",
                    "Web development",
                    "Full stack development",
                    "Software engineering",
                ]

                internship_spellings = ["Internship", "Internship", "internship", "INTERNSHIP", "Internship Program",
                                        "Internship Opportunity", "Internship Position", "Internship Experience",
                                        "Intern", "intern", "INTERN", "Intern Program", "Intern Opportunity",
                                        "Intern Position", "Intern Experience"]
                graduate_spellings = [
                    "Master's Degree", "Masters Degree", "Master Degree", "M.A.", "MA", "M.S.", "MS","Masters",
                    "M.Sc.", "MSc", "M.F.A.", "MFA", "M.B.A.", "MBA", "J.D.", "JD", "M.D.", "MD", "Ph.D.",
                    "PhD"]
                undergraduate_spellings = ["Bachelor's Degree", "Bachelors Degree", "Bachelor Degree", "B.A.", "BA",
                                           "B.S.", "BS"]

                banned_words = ["Banned", "Bechtel Corporation", "oracle","Sales", "Product", "Marketing", "People Operations", "Finance/Accounting", "eCommerce","xometry","bechtel","Data Science"]
                # print link into LinkdinSiteCodes.txt
                isValid = False
                if (strys):
                    strins = str(strys)
                    index = strins.find("description")
                    strins = strins[index:]
                    numStr = i.split("?")[0]
                    numStr = "".join(filter(str.isnumeric, numStr))
                    # also in the end and a conditon that checks if posting contains masters keyword and if it does check if it contains undergrad keyword and if it does return true
                    if (strins and contains_keyword(cs_keywords, strins) and contains_keyword(internship_spellings,strins) and numStr not in ids and not contains_keyword(banned_words,strins) and  customLogic(graduate_spellings, undergraduate_spellings, strins) ):
                        ids.append(numStr[-10:])
                        print(colored("Contains CS keywords and isnt used", 'blue'))
                        print(colored(i, 'cyan'))

                        isValid = True
                        with open("LinkdinSiteCodes.txt", "a") as myfile:
                            myfile.write("\n")
                            myfile.write(strins)
                            myfile.close()

                        with open("LinkdinSiteLinks.txt", "a") as myfile:
                            myfile.write("\n")
                            myfile.write(i)
                            myfile.close()

                if (isValid):
                    with open("LinkdinSiteCodes.txt", "a") as myfile:
                        myfile.write(i)
                        myfile.close()

    num = num + 25
    print("Done")
    print("sleeping for")
    if (num < 500):
        print(num * .20)
        time.sleep(num * .20)
        getLinks(url, num)
    else:
        print("300 seconds")
        time.sleep(300)
        getLinks(url, num)


getLinks(
    "https://www.linkedin.com/jobs/search/?currentJobId=3391751132&f_E=1&f_WT=2&geoId=103644278&keywords=computer%20science&location=United%20States&refresh=true",
    0)
