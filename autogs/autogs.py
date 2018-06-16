# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import gmtime, strftime
import time
import random
import subprocess
import os
import urllib


#definitions
NUMBER_OF_RESULTS_PER_PAGE = 20;
NUMBER_OF_RESULTS_PER_PAGE_FIRST = NUMBER_OF_RESULTS_PER_PAGE - 1;
TIMEOUT_AFTER_VISITING_PAGE = 2;
TIMEOUT_BROWSING_THROUGH_RESULTS = 1;
WAITING_TIME_FOR_PAGE_LOAD = 2;
WAITING_TIME_FOR_VPN_AGENT_START = 35;
WAITING_TIME_FOR_BROWSER_START = 4;
NUMBER_OF_PAGE_RESULTS_CHECKED = 10;
NUMBER_OF_INTERNAL_LINKS = 3;
NUMBER_OF_EXTERNAL_LINKS = 1;
TIME_SPENT_ON_A_LINK_WHILE_BROWSING = 5;

def get_external_id_address():
	external_ip = urllib.urlopen('https://ident.me').read();
	return external_ip;
#creating and opening the log file
logfile = open("./logs/logfile_" + strftime("%Y%m%d%H%M%S", gmtime()) + ".txt","w+");
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Starting the TorGuard Agent...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Starting the TorGuard Agent...\n");
#start the TorGuard Agent
proc = subprocess.Popen(['C:\\Program Files (x86)\\VPNetwork LLC\\TorGuard\\TorGuardDesktopQt.exe'], shell=True);
time.sleep(WAITING_TIME_FOR_VPN_AGENT_START);
current_ip_address = get_external_id_address();
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "The current external IP address is:" + current_ip_address + "\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "The current external IP address is:" + current_ip_address + "\n");
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Starting the browser...\n");
#make the google search using mozilla firefox
#profile = webdriver.FirefoxProfile("C:/Users/uidk4225/AppData/Roaming/Mozilla/Firefox/Profiles/i4bd3u2x.default");
profile = webdriver.FirefoxProfile("C:/Users/mihai/AppData/Roaming/Mozilla/Firefox/Profiles/18w4rpcq.default");
driver = webdriver.Firefox(firefox_profile=profile);
url = 'http://www.google.com/#q=';
expression = 'vulcanizari';
target_url = 'timexpres.ro';
driver.get(url + expression + "&num=" + str(NUMBER_OF_RESULTS_PER_PAGE));
time.sleep(WAITING_TIME_FOR_BROWSER_START);

def url_parser( url ):
	start_position = url.find('//');
	end_position = url.find('/', start_position + 2);
	url_extracted = url[start_position + 2: end_position];
	www_exists = url_extracted.find('www.');
	if www_exists !=-1:
		url_extracted = url_extracted[(www_exists + 4):];
	return url_extracted;

def user_browses_internal_links(NUMBER_OF_INTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver):
	number_of_executed_links = 0;
	while (number_of_executed_links < NUMBER_OF_INTERNAL_LINKS):
		all_the_links = driver.find_elements_by_tag_name("a");
		total_number_of_files = len(all_the_links);
		#determine randomly a valid internal link
		invalid = 1;
		while(invalid == 1):
			link_to_visit = random.randint(0, total_number_of_files);
			current_link = all_the_links[link_to_visit].get_attribute("href");
			if url_parser(url) == url_parser(current_link) and valid_link_exceptions(current_link) == 1:
				invalid = 0;	
		time.sleep(4);
		all_the_links[link_to_visit].click();
		time.sleep(TIME_SPENT_ON_A_LINK_WHILE_BROWSING);
		driver.back();
		time.sleep(5);
		number_of_executed_links = number_of_executed_links + 1;	

def user_browses_external_links(NUMBER_OF_EXTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver):
	number_of_executed_links = 0;
	while (number_of_executed_links < NUMBER_OF_EXTERNAL_LINKS):
		all_the_links = driver.find_elements_by_tag_name("a");
		total_number_of_files = len(all_the_links);
		#determine randomly a valid internal link
		invalid = 1;
		while(invalid == 1):
			link_to_visit = random.randint(0, total_number_of_files);
			current_link = all_the_links[link_to_visit].get_attribute("href");
			if url_parser(url) != url_parser(current_link):
				invalid = 0;
		print("Found external link: " + current_link);	
		time.sleep(4);
		all_the_links[link_to_visit].click();
		time.sleep(TIME_SPENT_ON_A_LINK_WHILE_BROWSING);
		number_of_executed_links = number_of_executed_links + 1;	
	
def visit_pages(iteration, target_url):
	#search the next valid result
	while (iteration > 0):
		actions = ActionChains(driver);
		actions.send_keys(u'\ue015');
		actions.perform();
		actions.reset_actions();
		time.sleep(TIMEOUT_BROWSING_THROUGH_RESULTS);
		iteration = iteration-1;	
	actions = ActionChains(driver);
	actions.send_keys(u'\ue007');
	actions.perform();
	actions.reset_actions();
	time.sleep(WAITING_TIME_FOR_PAGE_LOAD);
	url = driver.current_url;	
	TIME_SPENT_ON_THE_PAGE = 0;
	parsed_url = url_parser( url );
	logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Visiting domain " + parsed_url + "\n");
	print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Visiting domain " + parsed_url + "\n");
	if parsed_url == target_url:
		TIME_SPENT_ON_THE_PAGE = 20;
		logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Target domain found\n");
		print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Target domain found\n");
		user_browses_internal_links(NUMBER_OF_INTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver);
		user_browses_external_links(NUMBER_OF_EXTERNAL_LINKS, TIME_SPENT_ON_A_LINK_WHILE_BROWSING, driver);
	else:
		TIME_SPENT_ON_THE_PAGE = 1;
	time.sleep(TIME_SPENT_ON_THE_PAGE);
	driver.back();
	return;
	
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Starting the search results browsing...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Starting the search results browsing...\n");
numberOfTabs = 1;
j=1;
while(numberOfTabs<=NUMBER_OF_PAGE_RESULTS_CHECKED):
	i = 1;
	if numberOfTabs == 1:
		NUMBER_OF_RESULTS_USED = NUMBER_OF_RESULTS_PER_PAGE_FIRST;
	else:
		NUMBER_OF_RESULTS_USED = NUMBER_OF_RESULTS_PER_PAGE;
	while( i < NUMBER_OF_RESULTS_USED ):
		visit_pages(i, target_url);
		time.sleep(TIMEOUT_AFTER_VISITING_PAGE);
		i = i + 1;
	numberOfTabs = numberOfTabs + 1;
	actions = ActionChains(driver);
	actions.key_down(Keys.ALT).send_keys(u'\u004E');
	actions.perform();
	actions.reset_actions();
	time.sleep(5);

logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Ending session...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Ending session...\n");
time.sleep(30);
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing the browser...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing the browser...\n");
driver.close();
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing TorGuard...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing TorGuard...\n");
os.system("TASKKILL /F /IM TorGuardDesktopQt.exe");
logfile.write(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing the logfile...\n");
print(strftime("%Y-%m-%d %H:%M:%S  ", gmtime()) + "Closing the logfile...\n");
logfile.close();