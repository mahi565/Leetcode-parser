from bs4 import BeautifulSoup
import requests
import csv
import time

# Function to get rank for a given username
def get_rank(username):
    url = f'https://leetcode.com/{username}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
    except requests.RequestException as e:
        print(f"Request failed for username '{username}': {e}")
        return "Error"

    soup = BeautifulSoup(response.content, 'html.parser')
    rank_element = soup.find('span', class_='ttext-label-1 dark:text-dark-label-1 font-medium')
    
    if rank_element:
        return rank_element.text.strip()
    else:
        return "Rank not found"

# Read usernames from CSV file
input_csv_file = 'usernames.csv'
output_csv_file = 'user_ranks.csv'

# Open CSV file and create a new file to write the results
with open(input_csv_file, 'r') as infile, open(output_csv_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['Username', 'Rank'])  # Write header for the output CSV
    
    # Skip the header row if present
    header = next(reader, None)  # Skip the header row if it exists

    for row in reader:
        username = row[0]
        rank = get_rank(username)
        print(f'Username: {username}, Rank: {rank}')
        writer.writerow([username, rank])
        time.sleep(1)  # Add a delay to avoid hitting the server too frequently

print(f'Rank fetching complete. Check {output_csv_file} for results.')
