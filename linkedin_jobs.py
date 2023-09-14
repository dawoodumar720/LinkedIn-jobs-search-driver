import csv
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize Colorama to add color to console text
init(autoreset=True)

# Define a function to scrape job data
def scrape_job_data(webpage, page_number, max_pages):
    # Check if we have reached the maximum number of pages to scrape
    if page_number >= max_pages:
        return

    # Construct the URL for the next page
    next_page = f"{webpage}&start={page_number}"

    # Define headers to mimic a web browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    try:
        # Send an HTTP GET request to the next page
        response = requests.get(next_page, headers=headers)

        # Check if the response contains an HTTP error
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all job listings on the page using CSS selectors
        jobs = soup.find_all(
            "div",
            class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
        )

        for job in jobs:
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            job_company = job.find(
                "h4", class_="base-search-card__subtitle"
            ).text.strip()
            job_location = job.find(
                "span", class_="job-search-card__location"
            ).text.strip()
            job_link = job.find("a", class_="base-card__full-link")["href"]

            # Write the job data to a CSV file
            writer.writerow([job_title, job_company, job_location, job_link])

        # Print a success message in green
        print(f"{Fore.GREEN}Scraped page {page_number + 1}{Style.RESET_ALL}")

        # Increment page_number for the next page
        page_number += 1

        # Recursively call the function for the next page
        scrape_job_data(webpage, page_number, max_pages)

    except requests.exceptions.RequestException as e:
        # Handle request-related errors and print an error message in red
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

# Define a function to print the scraped job data
def print_job_data():
    with open("AI-jobs.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            # Print job data in green
            print(f"{Fore.GREEN}Title: {row[0]}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Company: {row[1]}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Location: {row[2]}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Apply: {row[3]}{Style.RESET_ALL}")
            print("\n")


if __name__ == "__main__":
    with open("AI-jobs.csv", "a", newline="", encoding="utf-8") as file:
        # Open the CSV file for writing job data
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Apply"])

        # Set the maximum number of pages to scrape
        max_pages_to_scrape = 5 

        # Set the initial page number
        start_page = 0

        # create a f'string variable for job search
        job_search = "AI" + "%20" + "Engineer"

        # Define the LinkedIn job search URL with search parameters
        webpage = f"https://www.linkedin.com/jobs/search?keywords={job_search}&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

        # Start scraping job data
        scrape_job_data(webpage, start_page, max_pages_to_scrape)

    # Print a message in green indicating that the file is closed
    print(f"{Fore.GREEN}File closed{Style.RESET_ALL}")

# Call the print_job_data function to print the scraped job data
print_job_data()
