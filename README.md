### used for finetuning LLM in big project, contact rytian@wisc.edu for more info
#### scrape all messages in discord dm/channel
not sure of its limit, my maximum was 200k msgs in one run
1. get discord auth token
open discord in browser
open network tab in inspect elements
type in any channel
find typing request in network tab
copy value in authorization under headers
store token in private/.env as DISCORD\_AUTHORIZATION\_TOKEN
2. setup ids
channel ids can be found in discord url
save ids to a file
3. run
python scraper.py < {ids-file} > {output-file}

