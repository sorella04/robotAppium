# -*- coding: utf-8 -*-
import os
import sys,requests,json
from time import sleep
from appium import webdriver
import subprocess
import appium_setup
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

env = BuiltIn().get_variable_value("${env}")
parallel = BuiltIn().get_variable_value("${parallel}")


if parallel == "true":
    if env == 'int':
        server_addr = 'http://localhost:4492/wd/hub'
        
    elif env == 'stg':
        server_addr = 'http://localhost:4493/wd/hub'
     
    elif env == 'pro':
        server_addr = 'http://localhost:4494/wd/hub'
    elif env == 'pro2':
        server_addr = 'http://localhost:4495/wd/hub'
else:
    server_addr = 'http://localhost:4723/wd/hub'
        
class AndroidAppiumLibrary(object):
    """Android Appium library for Robot Framework"""
    driver = webdriver.Remote(server_addr, appium_setup.desired_caps)
    
    def get_server_addr_if_parallel(self):
        if env == 'int':
            server = '127.0.0.1:4492'
            return server
        
        elif env == 'stg':
            server = '127.0.0.1:4493'
            return server
     
        elif env == 'pro':
            server = '127.0.0.1:4494'
            return server

    def relay_number(self):
	'''
	Method sets relay number depending on environment
	'''
	if env == 'int':
	    relay = 'rel1'
	    return relay

	elif env == 'stg':
	    relay = 'rel2'
	    return relay

	elif env == 'pro':
	    relay = 'rel3'
	    return relay

    def initiate_appium(self):
        AndroidAppiumLibrary.driver = webdriver.Remote(server_addr, appium_setup.desired_caps)  

    def quit_appium(self):
        """
        Method tries to kill current driver session.
        """
        try:
            AndroidAppiumLibrary.driver.quit()
        except Exception as e:
            print "Can not quit driver session, error message: {}.".format(e.args)

    def set_implicit_wait(self,timeout):
        '''Set selenium implicit wait value'''
        AndroidAppiumLibrary.driver.implicitly_wait(timeout)
        print "Implicit wait value= ",timeout       
    
    def clear_input(self, name):
        """
        Method clears input form.
        @param name - element content description
        @type name str
        """       
        element = AndroidAppiumLibrary.driver.find_element_by_name(name)
        try:
            element.clear()
        #problems on appium 1.3.7 - below is a  workaround in case of failure
        except Exception: 
            try:
                element.clear()
            except Exception:
                clear_text_with_backspace()   
    
    def find_element_by_name(self,name):
        return AndroidAppiumLibrary.driver.find_element_by_name(name)   
    
    def find_elements_by_xpath(self,xpath):
        return AndroidAppiumLibrary.driver.find_element_by_xpath(xpath)

    def find_element_by_id(self,id):
        return AndroidAppiumLibrary.driver.find_element_by_id(id)
    
    def enter_text(self,text,name):
        '''Enter given text into field with given content description '''
        AndroidAppiumLibrary.driver.find_element_by_name(name).send_keys(text)    
    
    def clear_text_field(self,name):            
        '''problems with on appium 1.3.7'''   
        field=AndroidAppiumLibrary.driver.find_element_by_name(name)
        field.clear()
        if (field.text!=""): field.clear()
          
    def clear_text_with_backspace(self,name):
        '''Method is a workaround for 'clear_text_field' method not working sometimes'''
        field=AndroidAppiumLibrary.driver.find_element_by_name(name)    
        field.click()
        for i in range(0, len(field.text)): 
            AndroidAppiumLibrary.driver.press_keycode(22) #right arrow key     
        for i in range(0, len(field.text)): 
            AndroidAppiumLibrary.driver.press_keycode(67) #backspace key
        
    def click_element_by_name(self,name):
        '''Click element with given content description or text'''
        AndroidAppiumLibrary.driver.find_element_by_name(name).click()

    def click_element_by_id(self,id):
        '''Click element with given id'''
        AndroidAppiumLibrary.driver.find_element_by_id(id).click()
    
    def wait_until_element_equals(self,conDesc,text,timeout):
        for i in range(timeout):
            try:
                element=AndroidAppiumLibrary.driver.find_element_by_name(conDesc).text
                if element == t:
                    return True
                sleep(1)
                print i
            except Exception:
                print Exception.message
                pass
        raise AssertionError
    
    def check_if_element_is_visible(self,name,text):
        '''check if element with given text is visible in display'''
        el=AndroidAppiumLibrary.driver.find_element_by_name(name)
        logger.info(el.text)
        element = self.remove_nb_spaces(el.text)
        if element==text:
            print "Text found"
            return True
        else:
            raise Exception("Element is not visible")

    def check_if_element_is_visible_by_id(self,id,text):
        '''
        check if element with given text is visible in display
        Method uses id for finding element
        '''
        el=AndroidAppiumLibrary.driver.find_element_by_id(id)
        logger.info(el.text)
        element = self.remove_nb_spaces(el.text)
        if element==text:
            print "Text found"
            return True
        else:
            raise Exception("Element is not visible")
        
    def check_if_element_is_present(self,name):
        '''check if element with given content description (and without text)
        is available in display'''
        return AndroidAppiumLibrary.driver.find_element_by_name(name)
    
    def press_back_hardkey(self):
        '''Instrumentation of pressing Android 'Back' hardkey'''
        sleep(1)
        AndroidAppiumLibrary.driver.back()
        print "Back hardkey has been pressed"   

    def press_enter_softkey(self):
        '''Instrumentation of pressing Android 'Enter' softkey'''
        AndroidAppiumLibrary.driver.press_keycode(66)
        print "Enter softkey has been pressed"
        
    def send_request_to_server(self,server,method,uri):
        '''
        Allows to send JSONWire request directly to Appium server
        For more details please see: http://code.google.com/p/selenium/wiki/JsonWireProtocol
        '''
        url="http://"+server+"/wd/hub/session/"+AndroidAppiumLibrary.driver.session_id+uri
        r = requests.request(method,url)
        return r
    
    def is_checkbox_checked(self,name,server):
        '''
        Check what is the status of checkbox with given content description
        (checked = True, not checked = False).
        '''
        if parallel == 'true':
            server = self.get_server_addr_if_parallel()
        checkbox=AndroidAppiumLibrary.driver.find_element_by_name(name).id
        checked="/element/"+checkbox+"/attribute/checked"
        r = self.send_request_to_server(server, 'GET', checked)
        js = json.loads(r.content)
        if(js['value']=="true"):
            return True
        else:
            return False

    def is_checkbox_checked_xpath(self,xpath):
        '''
        Check what is the status of checkbox with given xpath
        (checked = True, not checked = False).
        '''
        checkbox=AndroidAppiumLibrary.driver.find_element_by_xpath(xpath)
        if checkbox.get_attribute('checked') == 'true':
            print("is already checked")
            #print checkbox.get_attribute('checked')
        else:
            print("checking")
            #print checkbox.get_attribute('checked')
            checkbox.click()

    def is_checkbox_checked_by_name(self,name):
        '''
        Check what is the status of checkbox with given name
        (checked = True, not checked = False).
        '''
        checkbox=AndroidAppiumLibrary.driver.find_element_by_name(name)
        if checkbox.get_attribute('checked') == 'true':
            print("is already checked")
            #print checkbox.get_attribute('checked')
        else:
            print("checking")
            #print checkbox.get_attribute('checked')
            checkbox.click()

    def scroll_display(self,startX,startY,endX,endY):
        '''
        Scroll display. Coordinates can be given as percentage of display or pixels 
        with point (0,0) in left upper corner
        '''
        AndroidAppiumLibrary.driver.swipe(startX, startY, endX, endY)

    def move_screen(self, startX, startY, endX, endY):
        '''Method moves screen'''
        AndroidAppiumLibrary.driver.swipe(startX, startY, endX, endY)
	  
    def swipe_gesture(self, startX, startY, endX, endY):
        js_snippet = "mobile: swipe"
        args = {'startX':startX, 'startY':startY, 'endX':endX, 'endY':endY}
        AndroidAppiumLibrary.driver.execute_script(js_snippet, args)
        
    def take_appium_snapshot(self,path):
        success = AndroidAppiumLibrary.driver.get_screenshot_as_file(path)
        logger.warn(path)
        path=path.split("/")[-1]
        logger.warn('<a href="{0}"><img src="{0}" width="500"></a>'.format(path), html=True)
        
    def take_snapshot(self,path):
        subprocess.call(["monkeyrunner",path+"snapshot.py"])
        
    def get_text_if_element_is_present(self,name):
        '''get text of element if element with given content description (and without text)
        is available in display'''
        return AndroidAppiumLibrary.driver.find_element_by_name(name).text
    
    def get_text_if_element_is_present_by_id(self,id):
        '''get text of element if element with given id (and without text)
        is available in display'''
        item=AndroidAppiumLibrary.driver.find_element_by_id(id)
        item_text = self.remove_nb_spaces(item.text)
        return item_text
    
    def remove_nb_spaces(self,text):
        text = text.encode('UTF-8')
        result=text.replace('\xc2\xa0', ' ')
        result=result.strip()
        result=unicode(result,'utf-8')
        return result
    
    def find_elements_by_name(self,name):
       return AndroidAppiumLibrary.driver.find_elements_by_name(name)
   
    def touch_gesture(self, touchX, touchY):
        js_snippet = "mobile: tap"
        args = {'x':touchX, 'y':touchY}
        AndroidAppiumLibrary.driver.execute_script(js_snippet, args)
        
    def get_children_count_of_element(self, xpath):
        children_list = AndroidAppiumLibrary.driver.find_elements_by_xpath(xpath);
        return  len(children_list)
    
    def get_count_of_element(self, id):
        children_list = AndroidAppiumLibrary.driver.find_elements_by_id(id);
        return  len(children_list)         
  
    def get_logcat_from_device(self,path):
        log = AndroidAppiumLibrary.driver.get_log("logcat")
        with open(path, 'w+') as logfile:
            logfile.write("\n".join(str(x) for x in log))
            open(path+'_retrofit','w').writelines([ line.replace("u'", "'").replace(", 'level': 'ALL'", "") for line in open(path) if 'Retrofit' in line])
            logger.warn('<a href="{0}" style="width:1000px; height:20px">Retrofit log</a>'.format(path+'_retrofit')+'<br><div style="width:1000px;height:450px;line-height:1.5em;overflow:scroll; padding:5px;border:1px solid black; background:#FFFFE0;">{0}</div>'.format(open(path+'_retrofit').read()), html=True)
            logger.warn('<a href="{0}" style="width:1000px; height:20px">Full logcat</a>'.format(path), html=True)
            
    def hide_keyboard(self):
        AndroidAppiumLibrary.driver.hide_keyboard()

 
#################################################
###
### Methods below are not working on appium 1.3.7
###
#################################################
    def find_elements_by_tag_name(self,tag_name):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        return AndroidAppiumLibrary.driver.find_elements_by_tag_name(tag_name)
    def enter_text_by_tag_name(self,index, text):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        index = int(index)
        AndroidAppiumLibrary.driver.find_elements_by_tag_name("EditText")[index].send_keys(text)      
    def click_button_by_tag_name(self,index):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''Click x button in the display. Indexed from 0'''
        index = int(index)
        AndroidAppiumLibrary.driver.find_elements_by_tag_name("Button")[index].click()
    def click_spinner_by_tag_name(self,index):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''Click x spinner in the display. Indexed from 0'''
        index = int(index)
        AndroidAppiumLibrary.driver.find_elements_by_tag_name("Spinner")[index].click()
    def click_checkbox_by_tag_name(self,index):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        index = int(index)
        AndroidAppiumLibrary.driver.find_elements_by_tag_name("CheckBox")[index].click()
    def wait_until_popup_appears(self,text,timeout,buttons):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''Perform x iterations till pop-up with given title will appear and check if it contains correct buttons'''
        for x in range(timeout):
            try:            
                if t == AndroidAppiumLibrary.driver.find_element_by_tag_name("TextView").text:
                    print "Text found"
                    but=AndroidAppiumLibrary.driver.find_elements_by_tag_name("Button")
                    for i in range(len(but)):
                        assert but[i].text == buttons[i]
                    return True
                sleep(1)
            except Exception:
                print Exception.message
                pass
        raise AssertionError
    def wait_until_element_appears(self,elType,text,timeout):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        timeout = int(timeout)
        for i in range(timeout):
            try:
                elements=AndroidAppiumLibrary.driver.find_elements_by_tag_name(elType)
                for el in elements:
                    if el.text == t:
                        return True
                sleep(1)
            except Exception:
                print Exception.message
                pass
        raise AssertionError
    def wait_until_display_appears(self,tit,timeout):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''Perform x iterations till display with given title will appear'''
        for i in range(timeout):
            try:
                title=AndroidAppiumLibrary.driver.find_elements_by_tag_name("TextView")
                if title[0].text == tit:
                    return True
                sleep(1)
            except Exception:
                print Exception.message
                pass
        raise AssertionError
    def is_checkbox_checked_by_tag_name(self,number,server):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''
        Check what is the status of checkbox when content description is unknown
        (checked = True, not checked = False).
        '''
        if parallel == 'true':
            server = self.get_server_addr_if_parallel()
        number = int(number)
        checkbox=AndroidAppiumLibrary.driver.find_elements_by_tag_name("CheckBox")[number].id
        checked="/element/"+checkbox+"/attribute/checked"
        r = self.send_request_to_server(server, 'GET', checked)
        js = json.loads(r.content)
        if(js['value']=="true"):
            return True
        else:
            return False
    def checkboxes_quantity(self):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        try:
            return len(AndroidAppiumLibrary.driver.find_elements_by_tag_name("CheckBox"))
        except  Exception:
            return 0
    def get_text_if_element_is_present_by_tag(self,tag,index):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        '''get text of element if element with given tag (and without text)snapshot_
        is available in display'''
        index=int(index)
        item=AndroidAppiumLibrary.driver.find_elements_by_tag_name(tag)[index]
        item_text = self.remove_nb_spaces(item.text)
        return item_text
    def check_item_text_by_tag_name(self,tag,index,text):
        '''Method depreciated - finding element by tag name selector has been removed from appium'''
        index=int(index)
        item=AndroidAppiumLibrary.driver.find_elements_by_tag_name(tag)[index]
        item_text = self.remove_nb_spaces(item.text)
        logger.info("Element's text:"+item_text)
        logger.info("Given text:"+text)
        if item_text==text:
            return True
        else:
            raise AssertionError
        
    def initiate_appium_test(self):
        AndroidAppiumLibrary.driver = webdriver.Remote(server_addr, appium_setup.desired_caps1)
