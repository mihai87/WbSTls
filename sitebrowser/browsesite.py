# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import random
import os
import subprocess

WAITING_TIME_FOR_VPN_AGENT_START = 25;
#profile = webdriver.FirefoxProfile("C:/Users/uidk4225/AppData/Roaming/Mozilla/Firefox/Profiles/i4bd3u2x.default");

def valid_link_exceptions (url):
	#avoid links to review form;
	last_seven_chars = url[-7:];
	last_two_chars = url[-2:];
	if last_seven_chars == "#review" or last_two_chars =="/#":
		return 0;
	else:
		return 1;

def url_parser( url ):
	start_position = url.find('//');
	end_position = url.find('/', start_position + 2);
	url_extracted = url[start_position + 2: end_position];
	www_exists = url_extracted.find('www.');
	if www_exists !=-1:
		url_extracted = url_extracted[(www_exists + 4):];
	return url_extracted;

NUMBER_OF_INTERNAL_LINKS = 3;
TIME_SPENT_ON_A_LINK_WHILE_BROWSING = 3;
#internal links
def user_browses_internal_links(NUMBER_OF_INTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver):
	number_of_executed_links = 0;
	while (number_of_executed_links < NUMBER_OF_INTERNAL_LINKS):
		all_the_links = driver.find_elements_by_tag_name("a");
		total_number_of_files = len(all_the_links);
		#determine randomly a valid internal link
		invalid = 1;
		while(invalid == 1):
			link_to_visit = random.randint(0, total_number_of_files-1);
			current_link = all_the_links[link_to_visit].get_attribute("href");
			print(current_link);
			if url_parser(url) == url_parser(current_link) and valid_link_exceptions(current_link) == 1:
				try:
					invalid = 0;
					all_the_links[link_to_visit].click();				
				except WebDriverException:
					print("The link is not clickable, move to the next one...\n");
					invalid = 1;				
		print("Found internal link: " + current_link);
		TIME_SPENT_ON_A_LINK_WHILE_BROWSING = random.randint(35, 60);
		time.sleep(TIME_SPENT_ON_A_LINK_WHILE_BROWSING);
		driver.back();
		time.sleep(5);
		number_of_executed_links = number_of_executed_links + 1;	

NUMBER_OF_EXTERNAL_LINKS = 1;

#external links
def user_browses_external_links(NUMBER_OF_EXTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver):
	number_of_executed_links = 0;
	while (number_of_executed_links < NUMBER_OF_EXTERNAL_LINKS):
		all_the_links = driver.find_elements_by_tag_name("a");
		total_number_of_files = len(all_the_links);
		#determine randomly a valid internal link
		invalid = 1;
		while(invalid == 1):
			link_to_visit = random.randint(0, total_number_of_files-1);
			current_link = all_the_links[link_to_visit].get_attribute("href");
			if url_parser(url) != url_parser(current_link):
				invalid = 0;
		print("Found external link: " + current_link);	
		all_the_links[link_to_visit].click();
		time.sleep(4);
		#time.sleep(TIME_SPENT_ON_A_LINK_WHILE_BROWSING);
		number_of_executed_links = number_of_executed_links + 1;	

number_of_runs = 0;
while(1):
	number_of_runs = number_of_runs + 1;
	print('Run number '+ str(number_of_runs) + '\n');
	proc = subprocess.Popen(['C:\\Program Files (x86)\\VPNetwork LLC\\TorGuard\\TorGuardDesktopQt.exe'], shell=True);
	time.sleep(WAITING_TIME_FOR_VPN_AGENT_START);

	profile = webdriver.FirefoxProfile("C:/Users/mihai/AppData/Roaming/Mozilla/Firefox/Profiles/18w4rpcq.default");
	driver = webdriver.Firefox(firefox_profile=profile);
	url = 'http://www.timexpres.ro/';
	driver.get(url);
	time.sleep(5);
			
	user_browses_internal_links(NUMBER_OF_INTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver);
	user_browses_external_links(NUMBER_OF_EXTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver);

	driver.close();
	os.system("TASKKILL /F /IM TorGuardDesktopQt.exe");
	os.system("TASKKILL /F /IM firefox.exe");
	time.sleep(5);
	
