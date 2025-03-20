import requests
from bs4 import BeautifulSoup
import time
import re

# Starting URL
base_url = "https://zamboanga.com/chavacano/a-2/"

# Open text files for writing
with open("english_cont.txt", "w") as english_file, open("chavacano_cont.txt", "w") as chavacano_file:
    while base_url:
        # Request the page content
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the second row of each target table
        tables = soup.find_all("table", class_=False)
        for table in tables:
            rows = table.find_all("tr")
            if len(rows) > 1:
                second_row = rows[1]
                columns = second_row.find_all("td")

                # Ensure there are at least two columns
                if len(columns) >= 2:
                    # Get English and Chavacano text
                    english_text = columns[0].get_text(strip=True)
                    chavacano_text = columns[1].get_text(strip=True)

                    # Remove all occurrences of numbering (e.g., "1. ", "2. ")
                    english_text = re.sub(r'\d+\.\s*', '', english_text)
                    chavacano_text = re.sub(r'\d+\.\s*', '', chavacano_text)

                    # Split sentences based on punctuation
                    english_sentences = re.split(r'(?<=[.!?])\s+', english_text)
                    chavacano_sentences = re.split(r'(?<=[.!?])\s+', chavacano_text)

                    # Write and print each sentence on a new line in the respective file
                    for sentence in english_sentences:
                        sentence = sentence.strip()
                        if sentence:  # Only write non-empty sentences
                            english_file.write(sentence + "\n")
                            print("English:", sentence)
                    for sentence in chavacano_sentences:
                        sentence = sentence.strip()
                        if sentence:  # Only write non-empty sentences
                            chavacano_file.write(sentence + "\n")
                            print("Chavacano:", sentence)

        # Find the "next" button link under div class "nav-next"
        next_link = soup.find("div", class_="nav-next")
        if next_link:
            next_page = next_link.find("a", href=True)
            if next_page:
                base_url = next_page['href']
                if not base_url.startswith("http"):
                    base_url = "https://zamboanga.com" + base_url
            else:
                base_url = None
        else:
            base_url = None

        # Delay to prevent overwhelming the server
        time.sleep(1)