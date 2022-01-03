# Dataset of Open-source 976 iOS and 953 Android apps' code with their commits' hash
This repository contains thousands of iOS and Android apps code available on github. It also contains a script to fetch the latest data, if required.
Important note: this dataset only contains basic apps that are purely developed on the native framework. 

To access current dataset:-
For Android, look at Android/androidApps.json
For iOS, look at iOS/iosApps.json

To fetch new dataset:-
1. Create an authentication PAT token. Hint: [click here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
2. Copy and paste the authentication token in Android/query.py OR iOS/query.py, whichever you need. For pasting search for the method, `runQuery(query)` and paste your PAT in  `'Authorization': 'Token PASTE_HERE'`  
3. If you need a customized query, search for the method `query*Apps(outputFile*Path)` and replace the `query` attribute's value with your latest query.
4. Execute the `query.py` by  invoking `python3 query.py -o your_output_path` in terminal.
5. If you "really" wish to have all commit hashes for all repositories, just uncomment the `queryCommits` method call in method `main()` and run `query.py`.

Some facts:-
1. For fetching iOS apps, we are extracting all iOS apps that have the `AppDelegate` object initialized in their code. Hence the query: `https://github.com/search?q=appdelegate&type=Code` is executed.
2. For fetching Android apps, we are extracting all Android apps that have the `onCreate()` method initialized in their code. Hence the query: `https://github.com/search?l=Java&q=oncreate&type=Code` is executed.
