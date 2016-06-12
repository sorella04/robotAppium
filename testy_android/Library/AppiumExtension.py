from appium import webdriver
from robot.libraries.BuiltIn import BuiltIn


desired_caps = {
		'deviceName' : '192.168.56.101:5555',
 	        'platformName' : 'Android',
		'browserName' : '',
		'version' : '4.1.2',
		'app' : 'app=/home/marcelina/jakdojade.apk',
		'app-package' : 'com.citynav.jakdojade.pl.android',
		'app-activity' : 'SplashScreenActivity',
		
}

class AndroidAppiumLibrary(object):
    """Android Appium library for Robot Framework"""
    driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

    def find_element_by_name(self,name):
        return AndroidAppiumLibrary.driver.find_element_by_name(name)   
    
