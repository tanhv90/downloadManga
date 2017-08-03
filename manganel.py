from requests import get as requestsGet
from re import search as reSearch
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://manganel.com'

def get_data_from_manganel(link):
	# get HTML source from original link
	HTML = requestsGet(link).text
	# crawl
	source = besoup(HTML, 'lxml')
	# catch the title content
	title = source.find('title').text.split('Manga')[0].split('Read')[1].strip()
	# find chapter-list then find all a tag
	chapters = source.find(class_='chapter-list').find_all('a')
	# the number of chap
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	# handle data for return
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = chap['href']
		tempData['title'] = chap.contents[0]
		# each item in data is a dict with 2 keys: 'title' and 'href'
		data.append(tempData)
	return data

def save_img_from_manganel(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	# get HTML source from link chap
	HTML = requestsGet(data['href']).text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'], source.find(id='vungdoc').find_all('img'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			# download file and get filename
			files.append(filehandle.download_file(link, name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	# zip all files and remove them
	filehandle.zip_file(files, filename + '-' + "manganel.com" + '.zip')
	print('Done!')
