from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import slack
from pathlib import Path
from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError

# Parse FnG history
url = "https://alternative.me/crypto/fear-and-greed-index/#fng-history"
png_url = "https://alternative.me/crypto/fear-and-greed-index/#fng-history"
page = requests.get(url)
text = page.text
soup = BeautifulSoup(page.content, 'html.parser')

fngs = soup.find_all('div', class_='fng-circle')

fng_scores = []
for fng in fngs:
    fng_score = fng.text
    fng_scores.append(fng_score)

out_text = ("Today: %s <- Yesterday: %s (link: %s)" 
            % (fng_scores[0], fng_scores[1], png_url))
#print(out_text)


# Check log
base_dir = "/home/smchoi/projects/sentiment_alarm"
log_data = {}
log_file = '%s/messages.log' % base_dir
if os.path.exists(log_file):
    for line in open(log_file, 'r'):
        field = line.rstrip().split('\t')
        date, value = field
        log_data[date] = value
today = datetime.today().strftime('%Y-%m-%d')

flag_send_message = False
if today in log_data: 
    saved_out_text = log_data[today]
    if saved_out_text != out_text: # updated out_text
        flag_send_message = True
else: # today data not previously saved
    flag_send_message = True


# Send slack messages
if flag_send_message:
    env_path = Path(base_dir) / '.env'
    load_dotenv(dotenv_path=env_path)
    
    slack_token = os.environ['SLACK_TOKEN']
    client = WebClient(token=slack_token)
    
    try:
        response = client.chat_postMessage(
            channel="#coin_bug",
            text=out_text # FnG
        )
        with open(log_file, 'a') as fp:
            fp.write('%s\t%s\n' % (today, out_text))

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

else:
    print('%s data has already been saved in %s' % (today, log_file))
