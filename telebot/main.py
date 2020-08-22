import requests
import bs4 as bs


class Google:
	@staticmethod
	def search(query):
		URLs = []
		fQuery = query.replace(" ", "+")
		response = requests.get(f"https://www.google.com/search?q={fQuery}")
		soup = bs.BeautifulSoup(response.content, 'lxml')

		for i in soup.find_all('a'):
			hrefs = i.get('href')
			if hrefs[0:4] == "/url":
				pureHref = hrefs[7:]
				newUrl = ""
				for char in pureHref:
					if char != "&":
						newUrl += char
					else:
						break
				if len(URLs) <= 6:
					URLs.append(newUrl)

		return URLs


class Lyrics:
	@staticmethod
	def search(query):
		lyrics = []
		fQuery = query.replace(" ", "+")
		response = requests.get(f"https://search.azlyrics.com/search.php?q={fQuery}")
		soup = bs.BeautifulSoup(response.content, 'lxml')

		panel = soup.find_all('div', attrs={'class':'panel'})
		for i in panel:
			if "Song results" in i.text:
				for j in i.find_all('a'):
					if not j.has_attr('class') and len(lyrics) <= 1:
						lyrics.append([j.text, j.get('href')])

		return Lyrics.getLyrics(lyrics[0][0], lyrics[0][1])


	@staticmethod
	def getLyrics(label, link):
		r = requests.get(link)
		s = bs.BeautifulSoup(r.content, 'lxml')
		lyrics = s.find_all('div', attrs={'class':"", 'id':""})

		return label+"\n"+lyrics[0].text


# 0918111210
class Word:
	@staticmethod
	def translate(word):
		query = word.replace(" ", "+")
		url = f"https://www.amharicpro.com/index.php?dr=100&searchkey={query}"
		response = requests.get(url)
		soup = bs.BeautifulSoup(response.content, 'lxml')

		links = soup.find_all('a')
		formatted_word = ''

		for i in links:
			if i.has_attr('data-ng-click'):
				unformatted_words = i.get('data-ng-click')
				for j in unformatted_words[21:]:
						if j != "'":
							formatted_word += j
						else:
							formatted_word += " "
							break

		word_list = [i for i in formatted_word.split(" ")]
		for i in word_list:
			if word_list.count(i) > 1 or i == "":
				word_list.remove(i)
		
		if len(word_list) > 0:
			return word_list
		else:
			return ["NO WORD FOUND!"]


