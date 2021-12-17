import argparse
import json
import csv
import dateutil.parser

# This script processes a the output of twarc2 json results file.
# It output the data in a easier to use csv file, with full tweet text for retweets
# and the fuller username of a user.
# Sample twarc2 command:
# twarc2 search --start-time 2021-12-01 --end-time 2021-12-07 --limit 1000 --max-results 100 --archive "snow Toronto"  snow.jsonl

def processJson(jsonFile,outputFile,verbose):

    jsonData = []

    # load json file from twarc

    with open(jsonFile) as f:
        for line in f :
            jsonData.append(json.loads(line))

    count = 1

    # create list of csv header row values
    csvHeader = ['id','userid', 'username', 'createdDate', 'conversationId',\
        'tweetText', 'retweet', 'reply', 'like','quotes',"isRetweet"]

    with open(outputFile, 'w', encoding='UTF8', newline='') as f:

        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        # write the header row to the csv file
        writer.writerow(csvHeader)

        for jsonObj in jsonData:

            # create two lists containing additional user information and tweet information
            # this additional data is contained in the includes section of the twarc json output

            userList = []
            tweetList = []

            if "includes" in jsonObj:

                if "users" in jsonObj["includes"]:
                    for user in jsonObj["includes"]["users"]:
                        userList.append({"userId":user["id"], "username":user["username"]})

                if "tweets" in jsonObj["includes"]:

                    for tweetInclude in jsonObj["includes"]["tweets"]:
                        tweetList.append({"tweetId":tweetInclude["id"], "fullText":tweetInclude["text"]})

            # read the tweet objects from the twarc json objects

            for tweet in jsonObj["data"]:

                # set default values for the variables being written to the CSV
                id = 0
                tweetText = ""
                username = ""
                userid = 0
                newDate = "1900-01-01 00:00:00"
                retweets = -100
                replys = -100
                likes = -100
                quotes = -100
                conversationId = 0
                isRetweet = False


                count = count + 1

                if "id" in tweet:
                    id = tweet["id"]

                if "text" in tweet:
                    tweetText = tweet["text"]

                if "author_id" in tweet:
                    # look up full username in our username list from the includes section of the json file
                    # otherwise you are left with only the numeric user id
                    searchUser = next((item for item in userList if item["userId"] == tweet["author_id"]), None)
                    username = searchUser["username"]
                    userid = tweet["author_id"]

                if "created_at" in tweet:
                    oldDate = dateutil.parser.parse(tweet["created_at"])
                    newDate = (oldDate.strftime("%Y-%m-%d %H:%M:%S"))

                if "public_metrics" in tweet :
                    retweets = tweet["public_metrics"]["retweet_count"]
                    replys = tweet["public_metrics"]["reply_count"]
                    likes = tweet["public_metrics"]["like_count"]
                    quotes = tweet["public_metrics"]["quote_count"]

                if "conversation_id" in tweet:
                    conversationId = tweet["conversation_id"]

                # if the tweet object contains a referenced tweet object
                # check to see if there is retweet information and if there is
                # get the full text of the original tweet, otherwise the tweet text is truncated

                if "referenced_tweets" in tweet:

                    for refTweet in tweet["referenced_tweets"]:

                        if refTweet["type"] == "retweeted":
                            isRetweet = True
                            searchTweet = next((item for item in tweetList if item["tweetId"] == refTweet["id"]), None)
                            tweetText = searchTweet["fullText"]
                        else:
                            isRetweet = False

                # if verbose is set to True print individual tweet data while processing

                if(verbose):
                    print("==================== Tweet {} ========================".format(count))
                    print("Tweet ID: {} User ID: {} Username: {} Date: {} Tweet text: {}\n".format(id, userid,username,newDate,tweetText))

                # create a list of values for the csv writer
                tweetData = [id, userid, username, newDate,conversationId, tweetText, retweets, replys, likes, quotes,isRetweet]

                writer.writerow(tweetData)

        print("Processed {} tweets. Output written to: {}".format(count,outputFile))


def main():

    # process command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json")
    parser.add_argument("-o", "--output")
    parser.add_argument("-v", "--verbose",action='store_true')

    args = parser.parse_args()

    if args.json:
        jsonFile = args.json
    else:
        print("Please include a json file using the -j <FILE> command line arguument")

    if args.output:
        outputFile = args.output
    else:
        print("Please include a CSV output file using the -o <FILE> command line arguument")

    # if both command line arguments are present process JSON file from twarc

    if args.json and args.output:
        processJson(jsonFile,outputFile,args.verbose)

if __name__ == "__main__":
    main()
