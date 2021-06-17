from bs4 import BeautifulSoup
import requests
from googlesearch import search
from datetime import date
import json
from os import system
from termcolor import colored

courses_last = {"source": "geeksgod", "courses": []}

def coupon_scraper(url):
	content = requests.get(url).text
	soup = BeautifulSoup(content, 'lxml')
	coupon = soup.find('p', class_ = 'elementor-heading-title elementor-size-default').text
	return coupon

def udemy_link(title):
	query = title+' udemy course'
	for j in search(query, tld="com", num=1, stop=1, pause=1):
		return j

urls = ['https://geeksgod.com/category/freecoupons/udemy-courses-free/']

#banner
system('figlet -f slant Freedemy | lolcat')
print(colored('- BY GOKUL -'.center(50),'green'))
system("echo '\033[0;37m'")

print('='*110)
print('\n\n')

for i in urls:
	content = requests.get(i).text
	soup = BeautifulSoup(content, 'lxml')

	courses = soup.find_all('div', class_ = 'item-details')

	for course in courses:
		course_json = dict()

		try:
			coupon = coupon_scraper(course.a["href"])
			if coupon == None:
				continue

			title = course.h3.text
			dat = course.time.text
			udemylink = udemy_link(title)
			print(f'Course Title : {title}')
			print(f"Link         : {udemylink}")
			print(f'Date         : {dat}')
			print(f'coupon       : {coupon}')
			print(f'Enroll_link  : {udemylink}?couponCode={coupon}')
			print('\n')
			print("="*110)
			print('\n')

			course_json['title'] = title
			course_json['link'] = udemylink
			course_json['date'] = dat
			course_json['coupon'] = coupon
			course_json['enroll'] = f'{udemylink}?couponCode={coupon}'

			courses_last['courses'].append(course_json)

		except:
			pass


final = json.dumps(courses_last, indent=4)

file = open('courses.json', 'w')
file.write(final)
file.close()
