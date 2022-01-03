import sys, getopt, math, json, requests, pandas as pd, glob, time
import urllib.parse
from linkheader_parser import parse

def runQuery(query):
    flag = 1
    while flag == 1:
        try:
            print("Querying: " + query )
            headers = {
              'Authorization': 'Token PASTE_HERE'
            }
            response = requests.request("GET", query, headers=headers)
            txt = json.loads(response.text)
            message = txt['message']
        except (KeyError,TypeError) as e:
            return response
        if "exceeded" in message:
            print("Limit exceeded: Trying query again in 30 seconds ...")
            time.sleep(30)
            flag = 1
        else:
            return response
    return response
    
def getNextLink(response):
    response.headers.setdefault('Link', 'no-link')
    nextLink = urllib.parse.unquote(response.headers['Link'])
    #print("Total records: ",txt['total_count'])
    #print(nextLink)
    if nextLink != "no-link":
        result = parse(nextLink) # Parses header as JSON object
        try:
            return result['next']['url']
        except KeyError:
            return "no-link"
    return "no-link"
    
def dumpResponse(response,outputFile):
    with open(outputFile, "w") as outfile:
        txt = json.loads(response.text)
        json.dump(txt, outfile)
    print("JSON file printed to: " + outputFile)

def dumpData(data,outputFile):
    with open(outputFile, "w") as outfile:
        json.dump(data, outfile)
    print("Object dumped to: " + outputFile)

def queryAndroidApps(outputFileAndroidPath):
    print('Started querying')
    query = "https://api.github.com/search/code?q=oncreate+in:file+language:Java&page=1"
    nextLink = ""
    apps = []
    while nextLink != "no-link":
        response = runQuery(query)
        responseJson = json.loads(response.text)
        for item in responseJson['items']:
            link = item['repository']['html_url']  #looks like: https://github.com/mohammedhossam95/ToDoApp
            commitsUrlToken = link.split("https://github.com/")[1] # looks like: mohammedhossam95/ToDoApp
            temp = commitsUrlToken.split("/") # looks like: {mohammedhossam95,ToDoApp}
            user = temp[0] #looks like: mohammedhossam95
            repo = temp[1] #looks like: ToDoApp
            commitsUrl = "https://api.github.com/repos/"+commitsUrlToken+"/commits"
            repoRecord = {"repositoryUrl":"NA","author":"NA","repository":"NA", "commitsUrl":commitsUrl ,"commits":"NotRetrieved"}
            repoRecord["repositoryUrl"] = link
            repoRecord["author"] = user
            repoRecord["repository"] = repo
            apps.append(repoRecord)
        nextLink = getNextLink(response)
        query = nextLink
        print(nextLink)
        
    data = {"apps":apps}
    dumpData(data,outputFileAndroidPath)
    
        
def fetchAllCommits(query,commitsList,nextLink):
    response = runQuery(query)
    nextLink = getNextLink(response)
    if nextLink == "no-link":
        return commitsList
    commitMetaList = json.loads(response.text)
    for commitMeta in commitMetaList:
        commitsList.append(commitMeta['sha'])
    commitsList = fetchAllCommits(nextLink,commitsList,"")
    return commitsList
    
def queryCommits(inputFileAndroidPath,outputUserPath):
    recordNumber = 1
    commitsList = []
    nextLink = ""
    with open(inputFileAndroidPath, 'r') as openfile:
        androidApps = json.load(openfile)
        for app in androidApps['apps']:
            commitsLink = app['commitsUrl']
            commitsList = []
            commits = fetchAllCommits(commitsLink,commitsList,nextLink) # Recusive method
            app['commits'] = commits
            dumpData(app,outputUserPath + "/" + str(recordNumber) + ".json")
            app['commits'] = len(commits)
            recordNumber = recordNumber + 1
        dumpData(androidApps,outputUserPath + "/androidAppsCommits.json")

def queryRateLimit():
    print(runQuery("https://api.github.com/rate_limit").text)
    
def main(argv):
    try:
      opts, args = getopt.getopt(argv,"ho:")
    except getopt.GetoptError as e:
      print(argv)
      print("script.py -o <outputCsvPath>")
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print("script.py -o <outputCsvPath>")
         sys.exit()
      if opt == '-o':
         outputCsvPath = arg
         
    print("outputCsvPath file is: " + outputCsvPath)
    outputFileAndroidPath = outputCsvPath + "/androidApps.json"
    testFile = outputCsvPath + "/test.json"
    #queryRateLimit()
    queryAndroidApps(outputFileAndroidPath)
    inputFileAndroidPath = outputFileAndroidPath
    outputUserPath = outputCsvPath
    #queryCommits(inputFileAndroidPath,outputUserPath)
    #response = runQuery("https://api.github.com/repos/ArtemVasilenko/vasyaMaps/commits")
    #reply = json.loads(response.text)
    #dumpData(reply,testFile)

if __name__ == "__main__":
   main(sys.argv[1:])
