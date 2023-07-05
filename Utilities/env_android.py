from appium.webdriver.common.appiumby import AppiumBy
def get_by_android(driver, type, value):
    if type.__eq__("ID"):
        element = driver.find_element(AppiumBy.ID, value)
    elif type.__eq__("NAME"):
        element = driver.find_element(AppiumBy.NAME, value)
    elif type.__eq__("XPATH"):
        element = driver.find_element(AppiumBy.XPATH, value)
    elif type.__eq__("LINK TEXT"):
        element = driver.find_element(AppiumBy.LINK_TEXT, value)
    elif type.__eq__("PARTIAL LINK TEXT"):
        element = driver.find_element(AppiumBy.PARTIAL_LINK_TEXT, value)
    elif type.__eq__("CLASS NAME"):
        element = driver.find_element(AppiumBy.CLASS_NAME, value)
    elif type.__eq__("CSS"):
        element = driver.find_element(AppiumBy.CSS_SELECTOR, value)
    else:
        raise Exception("Not support type in framework")
    return element
def get_locator_for_wait(type, value):
        if type.__eq__("ID"):
            locator = (AppiumBy.ID, value)
        elif type.__eq__("NAME"):
            locator = (AppiumBy.NAME, value)
        elif type.__eq__("XPATH"):
            locator = (AppiumBy.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            locator = (AppiumBy.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            locator = (AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            locator = (AppiumBy.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            locator = (AppiumBy.CSS_SELECTOR, value)
        else:
            raise Exception("Not support type in framework", type)
        return locator
