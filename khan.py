import os
import time
import threading
import argparse
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--unit_index')
parser.add_argument('-v', '--video_index')
args = parser.parse_args()

fp = webdriver.FirefoxProfile("/home/darkmatter/.mozilla/firefox/def1")
fp.set_preference("dom.webdriver.enabled", False)
fp.set_preference("useAutomationExtension", False)
fp.update_preferences()
dc = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(executable_path=Path("/home/darkmatter/geckodriver"), firefox_profile=fp, desired_capabilities=dc)
driver.get("https://www.khanacademy.org/math/algebra")

time.sleep(4)
units_div = driver.find_elements_by_xpath("//a[@data-test-id='unit-header']") # gets all the units of the current link in driver.get
units = [unit.get_attribute("href") for unit in units_div]

def main(unit_index): # for testing purposes we will only do the first unit
    driver.get(units_div[int(unit_index)].get_attribute("href"))
    time.sleep(5)

    all_videos = driver.find_elements_by_xpath("//ul[@role='list']/li/div/div/a")
    vids = [url.get_attribute("href") for url in all_videos if "/v/" in url.get_attribute("href")]
    for i in range(int(args.video_index), len(vids)):
        before_stale = vids[i]
        driver.get(before_stale)
        time.sleep(10)

        btn = driver.find_element_by_xpath("//button[@data-test-id='video-play-button']")

        if str(btn.get_attribute("aria-label")) == "Play video":
            btn.click()
            time.sleep(2)
            vid_length = driver.find_element_by_xpath("//span[@data-test-id='video-time-hidden']") # in seconds
            times = str(vid_length.text).split(":")[-2:] # [minutes, seconds]
            total_duration = (int(times[0])*60) + int(times[1])

            # vid_time_update = threading.Thread(target=log_time, args=(total_duration,all_videos[0]))
            # vid_time_update.start()
            # cr = '\r'
            for n in range(1,total_duration):
                time.sleep(1/2)
                print(f"Completed {n}/{total_duration}", end="\r")

            print('\n')
            print('\n')

main(args.unit_index)
