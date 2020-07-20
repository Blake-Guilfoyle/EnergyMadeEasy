"""This doc contains a few functions to plan out my energy made easy script"""
"""Deciding that the script will take in dataframe of distrubtors as keys and postcodes as values"""
#First Step: Imports
#Second Step: Define Global Variables, Variables, dictionaries and functions
#Third Step: run functions/define structure

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import numpy as np
from openpyxl import Workbook
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import ElementClickInterceptedException
import json
import re
import sys



#Second Step:
    #Define Variables
    #Define Dictionaries
    #Define Functions

#Variables:
global driver
driver = webdriver.Chrome('C:/Users/Blake/Downloads/chromedriver.exe')

#Dictionaries:

DbByPostcode = {
    'Energex':4215,
    'Ergon':4350,
    'Ausgrid':2000,
    'Endeavour':2115,
    'Essential Energy':2311,
    'Evoenergy':2600,
    'SA Power Networks': 5000,
    'TasNetworks':7000}

DbRetailers = {
   'Energex':[],
    'Ergon':[],
    'Ausgrid':[],
    'Endeavour':[],
    'Essential Energy':[],
    'Evoenergy':[],
    'SA Power Networks':[],
    'TasNetworks':[]}

DbListOfPlans = {
    'Energex':[],
    'Ergon':[],
    'Ausgrid':[],
    'Endeavour':[],
    'Essential Energy':[],
    'Evoenergy':[],
    'SA Power Networks':[],
    'TasNetworks':[]}


#Functions:
def GetRetailers(DbByPostcode, Type):
    """A function that scrapes start page of energy made easy and loops through input dic
    Args:
        DbByPostcode: A predefined dictionary of a single postcode in each distribution network
        Type: A string either resi (residential) or com (commercial)
        
    Returns:
        dictionary (DbRetailers): retailers in each distribution network
        """
    for key,value in DbByPostcode.items():
               
        driver.get("https://www.energymadeeasy.gov.au/start")
        driver.find_element_by_name("electricity").click()
        driver.find_element_by_id("autocomplete-postcode").click()
        form = driver.find_element_by_id("autocomplete-postcode")
        form.send_keys(value)
        sleep(3)
        driver.find_element_by_class_name("autocomplete__results__item").click()
        if Type == "Resi":
            driver.find_element_by_name("1Person").click()
            driver.find_element_by_name("noUsage").click()
        if Type == "Com":
            driver.find_element_by_name("smallBusiness").click()
            driver.find_element_by_name("manual").click()
           
        
        sleep(3)
        driver.find_element_by_name("electricity-retailer").click()
        RawRetailers = driver.find_element_by_name("electricity-retailer").text
        RawRetailers = RawRetailers.split("\n")
        RawRetailers = RawRetailers[2:]
        dictrawretailers = dict.fromkeys(RawRetailers,)

        DbRetailers[key] = dictrawretailers

    return(DbRetailers)

def GetPlans(DbByPostcode,Type):
    """A Parent Function that Scrapes main results page on Energy Made Easy
    Args:
        DbByPostcode: A predefined dictionary of a single postcode in each distrubition network
        type: the type of premise to be scraped, either resi (Residential) or com (Commercial)

    Returns:
        dictionary (DbListOfPlans): links to each electricity plan by distributor
    """
    for key,value in DbByPostcode.items():
               
        driver.get("https://www.energymadeeasy.gov.au/start")
        driver.find_element_by_name("electricity").click()
        driver.find_element_by_id("autocomplete-postcode").click()
        form = driver.find_element_by_id("autocomplete-postcode")
        form.send_keys(value)
        sleep(3)
        driver.find_element_by_class_name("autocomplete__results__item").click()
        
        ##Change of button options for Residential
        if Type == "Resi":
            #Completes Resi Form
            driver.find_element_by_name("1Person").click()
            driver.find_element_by_name("noUsage").click()
            sleep(0.5)
            driver.find_element_by_name('solarPanels-No').click()
            if len(driver.find_elements_by_name('pool-No')) > 0:
                driver.find_element_by_name('pool-No').click()
            sleep(0.5)
            if len(driver.find_elements_by_name('underfloorHeating-No')) > 0:
                driver.find_element_by_name('underfloorHeating-No').click()
            sleep(0.5)
            if len(driver.find_elements_by_name("gasMethod-Don't have gas")) > 0:
                driver.find_element_by_name("gasMethod-Don't have gas").click()

            driver.find_element_by_name('smartMeter-Not sure').click()
            driver.find_element_by_name('electricity-retailer').click()
            driver.find_element_by_xpath("/html/body/div/div[2]/div/main/div/div/div/div[3]/div[3]/div/section[1]/section/fieldset/div/select/option[2]").click()
            
        ##Change of button options for Residential
        if Type == "Com":
            #Completes Com Form
            driver.find_element_by_name("smallBusiness").click()
            driver.find_element_by_name("manual").click()
            sleep(0.5)
            driver.find_element_by_name('electricity-retailer').click()
            driver.find_element_by_xpath("/html/body/div/div[2]/div/main/div/div/div/div[3]/div[3]/div/section[1]/section/fieldset/div/select/option[2]").click()
            
            driver.find_element_by_name('solarPanels-No').click()
            if len(driver.find_elements_by_name('peakOffpeakRates-No')) > 0:
                driver.find_element_by_name('peakOffpeakRates-No').click()
            sleep(0.5)
            if len(driver.find_elements_by_name('controlledLoad-No')) > 0:
                driver.find_element_by_name('controlledLoad-No').click()
            sleep(0.5)
            driver.find_element_by_name('smartMeter-Not sure').click()
        
            driver.find_element_by_id('dateInputelectricity-bill-start-date').click()
            driver.find_element_by_xpath('/html/body/div/div[2]/div/main/div/div/div/div[3]/div[3]/div/section[3]/section/fieldset/div/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[3]/button').click()
            driver.find_element_by_id('dateInputelectricity-bill-end-date').click()
            driver.find_element_by_xpath('/html/body/div/div[2]/div/main/div/div/div/div[3]/div[3]/div/section[3]/section/fieldset/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[4]/button').click()
            InputUsage = driver.find_element_by_name('energyInputelectricityTotalUsage')
            InputUsage.click()
            InputUsage.send_keys(80)
            
        #Accept Terms and conditions:
        driver.find_element_by_class_name('image-checkbox__label').click()
        driver.find_element_by_class_name('btn.btn--green.btn--large.btn-compare-plans').click()
        
        #Waiting for url Change to start scrape:
        while driver.current_url == 'https://www.energymadeeasy.gov.au/start':
            if driver.current_url == 'https://www.energymadeeasy.gov.au/results':
                break
        sleep(1)
        driver.find_element_by_class_name('main-filters-button-desktop').click()

        driver.find_element_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[2]/div[1]/label").click()

        driver.find_element_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[2]/div[3]/label").click()
        driver.find_element_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[6]/div[2]/div[3]/label").click()
        driver.find_element_by_id('applyFilters').click()
        driver.find_element_by_id('showAllPlans').click()
        while len(driver.find_elements_by_class_name("show-more-button.btn")) > 0:
            driver.find_element_by_class_name("show-more-button.btn").click()
            
        NumOfPlans = len(driver.find_elements_by_class_name("plan-results-tile"))+ 1
        Plans = []
        for x in range(1,NumOfPlans):
            if len(driver.find_elements_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[3]/div[4]/div["+str(x)+"]/div/div[2]/div[1]/a")) > 0:
                Plans.append(driver.find_element_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[3]/div[4]/div["+str(x)+"]/div/div[2]/div[1]/a").get_attribute("href"))

            if len(driver.find_elements_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[3]/div[3]/div["+str(x)+"]/div/div[2]/div[1]/a")) > 0:
                Plans.append(driver.find_element_by_xpath("/html/body/div/div[2]/div/main/section/div[1]/div/div[3]/div[3]/div["+str(x)+"]/div/div[2]/div[1]/a").get_attribute("href"))

        RawRetailerLinks = Plans
        DbListOfPlans[key] = RawRetailerLinks 
        

    return(DbListOfPlans)

def GetPlanDetails(DbListOfPlans, Type):
    """A Parent Function that Scrapes BIPD's (Basic Information Plan Documents) on the Energy Made Easy
    Args:
        DbListOfPlans: the return dictitonary of GetPlans function
        DbRetailers: the return dictitonary of GetRetailers function

    Returns:
        dictionary (EnergyMadeEasyPlans): BPID details by distrubtor and energy retailer
        """
    for key,value in DbListOfPlans.items():
        
        print('ll')#driver.get('www.google.com')
        #EnergyMadeEasyPlans = {}

    return()#EnergyMadeEasyPlans)

def save_dict(dictionary,name):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open("C:/Users/Blake/Desktop/Output/"+name+".json", 'w') as f: 
        json.dump(dictionary, default=set_default, sort_keys=True, fp = f )
    return('Successfully saved ' + name)

##Third Step: Run Functions

#Running GetRetailers Function
ResiDbRetailers = GetRetailers(DbByPostcode,"Resi")
ComDbRetailers = GetRetailers(DbByPostcode,"Com")
#Saving Dictionaries
save_dict(ResiDbRetailers,"ResiDbRetailers")
save_dict(ComDbRetailers,"ComDbRetailers")

#Running GetPlans Function
ResiDbListOfPlans = GetPlans(DbByPostcode,"Resi")
ComDbListOfPlans = GetPlans(DbByPostcode,"Com")
#Saving Dictionaries
save_dict(ResiDbListOfPlans,"ResiDbListOfPlans")
save_dict(ComDbListOfPlans,"ComDbListOfPlans")

#Running GetPlansDetails Function
ResiPlanDetails = GetPlanDetails(ResiDbListOfPlans, "Resi")
ComPlanDetails = GetPlanDetails(ComDbListOfPlans, "Com")
#Saving Dictionaries
save_dict(ResiPlanDetails,"ResiPlanDetails")
save_dict(ComPlanDetails,"ComPlanDetails")

sys.exit()