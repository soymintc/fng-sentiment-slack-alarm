# fng-sentiment-slack-alarm
A sentiment alarm on slack for crypto feer and greed index

1. Parses https://alternative.me/crypto/fear-and-greed-index/#fng-history
2. Upon reading log, updates messages.log information
- You need to create ".env" file and add "SLACK_TOKEN=<your_slack_token>"
3. Recommend editing /etc/crontab for synchronized run of this script
