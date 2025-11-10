import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
import numpy as np
import unicodedata


def clean_name(name):
    """Remove accents and special characters for URL"""
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ASCII', 'ignore').decode('ASCII')
    name = name.replace("'", "").replace(".", "")
    return name


# Headers to avoid rate limiting
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Load players
print("Loading NBA players from 2000-2020...")
dfNames = pd.read_csv("../../Data/Training Set/NBA_2000_2020.csv")

# Get unique player names to avoid duplicates
unique_players = dfNames["PLAYER"].unique()
print(f"Total unique players: {len(unique_players)}")

# Prepare names for scraping
firstLast = []
for name in unique_players:
    parts = name.split()
    if len(parts) >= 2:
        first = clean_name(parts[0])
        last = clean_name(parts[-1])
        firstLast.append([first, last, name])  # Keep original name
    else:
        print(f"Skipping player with incomplete name: {name}")

print(f"Players to scrape: {len(firstLast)}\n")

# Initialize
df2 = pd.DataFrame()
count = 0
success_count = 0
failed_players = []

# Scraping loop
for first, last, original_name in firstLast:
    cont = True
    url = f'https://www.sports-reference.com/cbb/players/{first}-{last}-1.html'

    try:
        # Wait before request
        lag = np.random.uniform(low=10, high=15)  # Longer wait to avoid 429
        time.sleep(lag)

        page = requests.get(url, headers=headers, timeout=15)

        # Check for rate limiting
        if page.status_code == 429:
            print(f"⚠️  Rate limited! Waiting 5 minutes...")
            time.sleep(300)
            page = requests.get(url, headers=headers, timeout=15)

        if page.status_code != 200:
            print(f"✗ {original_name}: HTTP {page.status_code}")
            failed_players.append(original_name)
            count += 1
            continue

        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table', id='players_per_game')

        # Check comments if table not found
        if table is None:
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                if 'id="players_per_game"' in comment:
                    comment_soup = BeautifulSoup(comment, 'html.parser')
                    table = comment_soup.find('table', id='players_per_game')
                    if table:
                        break

        # If still no table, player didn't play college
        if table is None:
            failed_players.append(original_name)
            cont = False

        # Extract data
        if cont:
            df = pd.read_html(str(table))[0]
            df = df.dropna(how='all')  # Drop completely empty rows
            df["Name"] = original_name  # Use original name with proper capitalization
            df2 = pd.concat([df2, df], ignore_index=True)
            success_count += 1
            print(f'✓ [{count + 1}/{len(firstLast)}] {original_name} - waiting {round(lag, 1)}s')
        else:
            print(f'✗ [{count + 1}/{len(firstLast)}] {original_name} - No college data')

        count += 1

        # Save progress every 50 players
        if count % 50 == 0:
            print(f"\n{'=' * 60}")
            print(f"Progress: {count}/{len(firstLast)} players processed")
            print(f"Successful: {success_count}, Failed: {len(failed_players)}")
            print(f"{'=' * 60}\n")

    except Exception as e:
        print(f'✗ [{count + 1}/{len(firstLast)}] {original_name} - Error: {e}')
        failed_players.append(original_name)
        count += 1
        continue

# AFTER THE LOOP - Process the data
print("\n" + "=" * 60)
print("SCRAPING COMPLETE")
print("=" * 60)
print(f"Total processed: {count}")
print(f"Successful: {success_count}")
print(f"Failed: {len(failed_players)}")

if len(df2) > 0:
    print("\nProcessing final year data...")

    # Get final year only (not career totals)
    df_final = df2[~df2['Season'].str.contains("Career", na=False)]
    df_final = df_final.groupby('Name').tail(1).reset_index(drop=True)

    # Drop unnecessary columns
    columns_to_drop = ["Season", "Team", "Conf", "Class", "Pos", "Awards"]
    df_final = df_final.drop(columns=[col for col in columns_to_drop if col in df_final.columns])

    print(f"Total players with college data: {len(df_final)}")
    print("\nFirst 10 players:")
    print(df_final[['Name', 'G', 'PTS', 'TRB', 'AST']].head(10))

    # Save
    output_path = "../../Data/Training Set/NCAA_2000_2020.csv"
    df_final.to_csv(output_path, index=False)
    print(f"\n✓ Saved to: {output_path}")

    # Save failed players list
    if len(failed_players) > 0:
        failed_df = pd.DataFrame({'Player': failed_players})
        failed_df.to_csv("../../Data/Training Set/Failed_Players_2000_2020.csv", index=False)
        print(f"✓ Failed players saved to: Failed_Players_2000_2020.csv")
        print(f"\nSample failed players (likely international):")
        for player in failed_players[:10]:
            print(f"  - {player}")
else:
    print("\n⚠️  No data scraped! Check for errors above.")