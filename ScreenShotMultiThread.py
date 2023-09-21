#!/usr/bin/python3

import threading
import time
from queue import Queue
import requests
import urllib3
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def exceptionToFile(url):
    while exceptionToFile.locked():
        sleep(0.01)
        continue

    global_lock_exceptionToFile.acquire()

    with open("exceptionfile.txt", "a+") as file:
        file.write(url)
        file.write("\n")
        file.close()

    global_lock_exceptionToFile.release()


def make_request(url):
    try:
        options = Options()
        options.headless = True
        t = time.time()
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(90)
        print("Requesting " + url)
        driver.get('http://' + str(url))
        screenshot = driver.save_screenshot(url + ".png")
        driver.quit()
    except TimeoutException:
        print("insie of timeout exception.")
        driver.execute_script("window.stop();")
        print(i +" Time consuming: ", time.time() - t)
        driver.quit()
        exceptionToFile(url)
        pass
    except:
        print("Exception for: " + url)
        pass


def manage_queue():
    """Manages the url_queue and calls the make request function"""
    while True:

        # Stores the URL and removes it from the queue so no 
        # other threads will use it. 
        current_url = url_queue.get()
        #print(current_url)

        # Calls the make_request function
        make_request(current_url)


        # Tells the queue that the processing on the task is complete.
        url_queue.task_done()

if __name__ == '__main__':

    # Set the number of threads.
    number_of_threads = 3
    
    # Needed to safely print in mult-threaded programs.
    # https://stackoverflow.com/questions/40356200/python-printing-in-multiple-threads
    print_lock = threading.Lock()
    
    # Initializes the queue that all threads will pull from.
    url_queue = Queue()

    # The list of URLs that will go into the queue.
    #urls = ["https://www.google.com"] * 30

    i = open("sites.txt").readlines()
    urls = [s.rstrip("\'$'\n\'") for s in i]
    
    
    # Start the threads.
    for i in range(number_of_threads):

        # Send the threads to the function that manages the queue.
        t = threading.Thread(target=manage_queue)

        # Makes the thread a daemon so it exits when the program finishes.
        t.daemon = True
        t.start()
    
    start = time.time()

    # Puts the URLs in the queue
    for current_url in urls:
        url_queue.put(current_url)

    # Wait until all threads have finished before continuing the program.
    url_queue.join()
    os.system('./combine.sh')

    print("Execution time = {0:.5f}".format(time.time() - start))
