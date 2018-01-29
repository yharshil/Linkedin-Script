import csv
import parameters
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def validate_field(field):
	if field:
		pass
	else:
		field=''
	return field

def search_page(x):
	driver.get('http://google.com')
	sleep(1)

	search_query=driver.find_element_by_name('q')
	search_query.send_keys(parameters.search_query)
	sleep(0.5)
	search_query.send_keys(Keys.RETURN)
	sleep(2)
	if x!=2:
		driver.find_element_by_xpath('//*[@id="nav"]/tbody/tr/td['+str(x)+']/a').click()
		get_skill(driver,x)
	else:
		get_skill(driver,x)

def get_skill(driver,x):
	print('# Results from Page '+str(x-1)+' #')
	linkedin_urls=driver.find_elements_by_tag_name('cite')
	linkedin_urls=[url.text for url in linkedin_urls]
	sleep(1)

	for linkedin_url in linkedin_urls:
		try:
			driver.get(linkedin_url)
			sleep(2)

			sel=Selector(text=driver.page_source)

			name=sel.xpath('//h1/text()').extract_first()

			job_title=sel.xpath('//h2/text()').extract_first()

			school = sel.xpath('//*[starts-with(@class, "pv-top-card-section__school")]/text()').extract_first()

			location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

			linkedin_url = driver.current_url

			#skill=sel.xpath('//*[starts-with(@class,"pv-skill-entity__skill-name")]/text()').extract_first()

			if school:
				school=school.strip()

			name=validate_field(name)
			job_title=validate_field(job_title)
			school=validate_field(school)
			location=validate_field(location)
			linkedin_url=validate_field(linkedin_url)
			#skill=validate_field(skill)

			print ('Name: '+name)
			print ('Job Title: '+job_title)
			print ('School: '+school)
			print ('Location: '+location)
			print ('URL: '+linkedin_url)
			#print('skill '+skill)
			print ('\n')
			
			To try to connect with the people 
			try:
		        driver.find_element_by_xpath('//span[text()="Connect"]').click()
		        sleep(3)

		        driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
		        sleep(3)

		    except:
		        pass
			writer.writerow([name,
							job_title,
							school,
							location,
							linkedin_url])
		except:
			pass

writer=csv.writer(open(parameters.file_name, 'w'))
writer.writerow(['Name','Job Title','School','Location','URL'])

driver=webdriver.Chrome('/Users/harshilyadav/Downloads/chromedriver')
driver.get('http://linkedin.com')

username=driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password=driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button=driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(1)

for x in range(2,10):
	search_page(x)

driver.quit()