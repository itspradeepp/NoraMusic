from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv

# Path to ChromeDriver
CHROME_DRIVER_PATH = 'C:\\Users\\palpr\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

def scrape_billboard_data(url):
    # Set up Selenium WebDriver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)  # Allow time for the page to fully load
    
    data = []
    
    try:
        # Find all relevant article elements containing songs
        articles = driver.find_elements(By.XPATH, "//article[contains(@class, 'c-gallery-vertical-featured-image')]")
        
        for article in articles:
            # Extract the song and artist info using the XPath within each article
            h2 = article.find_element(By.XPATH, ".//h2")
            text = h2.text.strip()
            
            # Split the text into rank, artist, and song title
            parts = text.split('. ', 1)
            if len(parts) == 2:
                rank = parts[0]
                artist_song = parts[1]
                if '“' in artist_song and '”' in artist_song:
                    artist, song = artist_song.split('“', 1)
                    song = song.replace('”', '').strip()
                    artist = artist.strip()
                    data.append({"Rank": rank, "Artist": artist, "Song Title": song})
                    print(f"Rank: {rank} | Artist: {artist} | Song Title: {song}")
            else:
                print(f"Unexpected format: {text}")
    
    finally:
        driver.quit()
    
    return data

def save_to_csv(data, filename):
    
    headers = ["Rank", "Artist", "Song Title"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    billboard_url = "https://www.billboard.com/lists/best-pop-songs-all-time-hits/"
    song_data = scrape_billboard_data(billboard_url)
    
    if song_data:
        csv_filename = "billboard_songs.csv"
        save_to_csv(song_data, csv_filename)
        print(f"\nData saved to {csv_filename}")
    else:
        print("No data scraped!")
