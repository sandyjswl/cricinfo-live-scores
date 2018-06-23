from bs4 import BeautifulSoup
import requests

# The RSS feed to get the links of live matches
rss_url="http://static.cricinfo.com/rss/livescores.xml"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Get the LIVE scorecard and status of a match.
def getScorecard(match_url):

	try:
		page = requests.get(match_url, headers=headers)
		bs=BeautifulSoup(page.content, "lxml")
		score_body=bs.find_all("div" ,{"class":"cscore_team icon-font-after"})
		details_body=bs.find_all("span",{"class":"cscore_notes_game"})

		for hit in score_body[0].findAll(attrs={'class' : 'cscore_name--short'}):
		    team1_name = hit.text

		for hit in score_body[0].findAll(attrs={'class' : 'cscore_score'}):
		    team1_score=hit.text

		for hit in score_body[1].findAll(attrs={'class' : 'cscore_name--short'}):
		    team2_name = hit.text

		for hit in score_body[1].findAll(attrs={'class' : 'cscore_score'}):
		    team2_score = hit.text

		soup_output=bs.find("span",class_="cscore_notes_game")
		match_status = soup_output.text


		print("Scorecard Summary: ")
		print(team1_name+"  :  "+team1_score)
		print(team2_name+"  :  "+team2_score)
		print("Match Status: "+match_status)

	except:
		print("Match Not Started Yet.....")


def getMatchLinks():
	global rss_url,headers

	page = requests.get(rss_url, headers=headers)
	bs=BeautifulSoup(page.content, "xml")
	match_titles=bs.find_all('title')
	match_links=bs.find_all('link')
	displayScorecard(match_titles,match_links)

def displayScorecard(match_titles,match_links):
	for i in range(1,len(match_titles)):
		print("Match:  "+match_titles[i].contents[0])
		match_url=match_links[i].contents[0]
		getScorecard(match_url)
		print("---------------------------------------------------------------------------")
		print("\n\n")


if __name__ == '__main__':
	getMatchLinks()
