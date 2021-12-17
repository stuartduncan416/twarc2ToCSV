# twarc2ToCSV 

This is a simple Python script that converts the JSON output from a twarc2 archive search to a simple CSV file. When processing the [twarc2](https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/) JSON output, I found I was missing the full username data and that the output didn’t include the full tweet text, if the tweet was a retweet. 

The outputted CSV file contains columns for tweet id, user id, username, created date (YYYY-MM-DD HH:MM:SS format), twitter conversation id, full tweet text, amount of retweets, amount of replies, amount of likes, amount of quotes and a boolean flag indicating if the tweet is a retweet. A sample of the output CSV is included in the repository. As are two sample JSON output from twarc2, one of 100 tweets and a second of 1000 tweets. 

The script requires command line arguments for the twarc2 json file and the desired output name of the CSV file. For example: 

python twarc2ToCSV.py -j snow.jsonl -o snowresults.csv

Would read data from snow.jsonl and output to snowresults.csv

If you would like more verbose output while running the script add the -v command line argument as such : 

python twarc2ToCSV.py -j snow.jsonl -o snowresults.csv -v

and the script will print individual tweet data as it runs. 
