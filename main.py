from mega import Mega
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getMegaLink(url):
    if len(url) < 5:
        return ""

    # Maximum number of redirections to follow
    max_redirects = 10

    # Follow the redirections
    for _ in range(max_redirects):
        response = requests.get(url, allow_redirects=False, verify=False)
        if response.status_code in (300, 301, 302, 303, 307):
            url = response.headers['Location']
        else:
            break

    # Extract the final Mega link
    final_link = url

    # Print the final Mega link
    return final_link



def getLinks(x, url):
    mega_links = []

    temp = url.split("1", 1)
    x = int(x)

    for i in range(1, x + 1):

        temp = url.split("1", 1)
        website_url = temp[0] + str(i) + temp[1]

        response = requests.get(website_url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all elements with class "Button STPb"
        elements = soup.find_all(class_="Button STPb")


        # Iterate through each element
        for element in elements:
            # Get the href attribute value
            href = element.get("href")

            # Parse the URL
            parsed_url = urlparse(href)

            temp = getMegaLink(urlunparse(parsed_url))

            parsed_url = urlparse(temp)

            # Check if the URL is a Mega link
            if parsed_url.netloc == "mega.nz":
                mega_links.append(temp)
                break

    return mega_links


def addLinksToAccount(mega_links):
    # Mega account credentials
    mega_email = input("email: ")
    mega_password = input("password: ")

    # Initialize Mega client
    mega = Mega()

    # Login to Mega
    mega.login(mega_email, mega_password)

    for link in mega_links:
        mega.import_public_url(link)
        print(f"Imported {link} to Mega.")


def main():
    num = input("number of episodes: ")
    link = input("first episode link: ")
    addLinksToAccount(getLinks(num, link))


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main()
