import requests
from bs4 import BeautifulSoup
import sqlite3
import re

#Define a class to scrape campus events
class CampusEventScraper:
    """
    A class for scraping campus event data from the Adrian College website.

    Attributes:
        base_url (str): The base URL of the events page to scrape.
        conn (sqlite3.connect): Establishes connection to sqlite database.
        cursor (sqlite3.cursor): Creates cursor to execute SQL commands.

    Methods:
        scrape_event_links (): Gets and returns a list of event links.
        clean_text (text): Cleans text by removing extra whitespace.
        scrape_event_page (url): Extracts event details from individual event pages.
        save_event (event): Inserts event data into external_events table.
        run (): Runs the full scraping and storage workflow. 
    """
    #Define constructor and store base url, connect to database, and create cursor to execute SQL commands
    def __init__(self, base_url="https://www.adrian.edu/calendar"):
        """
        Acts as a constructor for the CampusEventScraper object, with the base URL, and establishes 
        a connection to the database.

        Args:
            base_url (str): The URL of the main events calendar webpage.
        """
        self.url = base_url
        self.conn = sqlite3.connect("db/campusconnect.db")
        self.cursor = self.conn.cursor()

    #Define a method to collect event links from main page, send get request, and parse HTML response
    def scrape_event_links(self):
        """
        Scrapes main event calendar webpage to extract individual event page links.

        Returns: 
            A list of unique individual event page URLs.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        #Create empty list to store scraped links
        links = []
        #Loop through anchor tags to find elements with an href attribute 
        for a in soup.find_all("a", href=True):
            href = a["href"]
            #Target "/calendar/" in href to ensure urls are for events
            if "/calendar/" in href and len(href.split("/")) >= 5:
                full_url = "https://www.adrian.edu" + href
                #Ensure duplicates aren't entered in list
                if full_url not in links:
                    links.append(full_url)
        #Return list of links for event pages
        return links

    #Define a method to clean text by removing extra whitespace
    def clean_text(self, text):
        """
        Cleans text by removing extra whitespace.

        Args:
            text (str): The raw text scraped.

        Returns: 
            str or None: Cleaned text or None if there is no text available.
        """
        return re.sub(r"\s+", " ", text).strip() if text else None

    #Define a method to scrape individual event page and ensure that it is an event page
    def scrape_event_page(self, url):
        """
        Scrapes an individual event page and extracts event details.

        Args:
            url (str): The URL of the event page.
        
        Returns:
            dict or None: A dictionary with event details, including title, date, location, description, and URL.
            Returns None if the webpage is not a valid event.

        """
        if "/calendar/" not in url:
            return None  
        #Request and parse HTML from event page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        #Target, scrape, and clean event title
        title_tag = soup.find("h1") or soup.find(class_="title")
        title = self.clean_text(title_tag.get_text()) if title_tag else None

        #Target, scrape, and clean date text
        date_tag = soup.find("p", class_="dates")
        date = self.clean_text(date_tag.get_text()) if date_tag else None
        #Target description text
        description_block = soup.find(id="content-7030")
        #Placeholder for event description and location
        description = None
        location = None
        #Only continues if there is description text, extracts all text, and splits into separate lines
        #Used ChatGPT to help figure out how to separate location from description
        if description_block:
            text = description_block.get_text("\n", strip=True)
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            #Create empty list to store cleaned lines
            cleaned_lines = []
            #Loop through lines in description text
            for i, line in enumerate(lines):
                #Find address using zip code patterns and venue by targeting text above address
                if re.search(r"\d{3,}.*MI\s+\d{5}", line):
                    address = line
                    venue = lines[i - 1] if i > 0 else None
                    #Combines venue and address into location
                    if venue:
                        location = f"{venue}, {address}"
                    else:
                        location = address
                    #Skips adding location in description
                    continue  
                #Skip to next line if current line includes address information
                if i < len(lines) - 1 and re.search(r"\d{3,}.*MI\s+\d{5}", lines[i + 1]):
                    continue
                #Keep lines without location information in description text
                cleaned_lines.append(line)
            #Join cleaned description lines
            description = self.clean_text(" ".join(cleaned_lines))
            #Filter out non-event pages  
            if not title or title.lower() in ["why adrian?", "undergraduate studies", "graduate studies"]:
                return None
        #Return event data as a dictionary
        return {
            "title": title,
            "date": date,
            "location": location,
            "description": description,
            "url": url
        }
    #Save event data, skipping empty events
    def save_event(self, event):
        """
        Saves event data into the sqlite database.

        Args:
            event (dict): A dictionary with event details.

        Returns:
            None.
        """
        if not event:
            return
        #Insert event data in external_events table
        self.cursor.execute("""
            INSERT INTO external_events (title, date, location, description)
            VALUES (?, ?, ?, ?)
        """, (
            event["title"],
            event["date"],
            event["location"],
            event["description"]
        ))
        #Save changes to database
        self.conn.commit()

    #Define method to scrape event links, event data, and save events
    def run(self):
        """
        Runs the full scraping process, collecting event links, extracting event data from each event page,
        and storing valid event results in the database.

        Returns:
            None.
        """
        links = self.scrape_event_links()

        for link in links:
            event = self.scrape_event_page(link)
            
            if event:
                self.save_event(event)
#Run CampusEventScraper
if __name__ == "__main__":
    scraper = CampusEventScraper()
    scraper.run()
