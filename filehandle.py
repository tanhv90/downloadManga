import zipfile
import os
from requests import get as requestsGet

def zip_file(files, filename):
	zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
	for file in files:
		zipf.write(file)
		os.remove(file)	
	zipf.close()

def download_file(url, filename):
	req = requestsGet(url, stream=True)
	with open(filename, 'wb') as f:
		for chunk in req.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return filename
