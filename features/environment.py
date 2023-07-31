import configparser
import datetime
import logging
import os
import appium
from appium.webdriver.appium_service import AppiumService
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_option
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.options import Options as firefox_option
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.safari.options import Options as safari_option
from selenium.webdriver.safari.service import Service as safari_service
from Utilities.action_web import ManagementFile
from Utilities.read_configuration import read_configuration


def before_all(context):
    context.dict_save_value = {}
    context.driver = None
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_env.ini')
    file = open(config_file_path, 'r')
    context.config_env = configparser.RawConfigParser(allow_no_value=True)
    context.config_env.read_file(file)
    context.platform = context.config_env.get("drivers_config", "platform")
    context.stage_name = context.config_env.get("drivers_config", "stage")
    if context.config_env.has_option("drivers_config", "browser"):
        context.browser = context.config_env.get("drivers_config", "browser")
    else:
        context.browser = "chrome"
    context.env = read_configuration().read()
    context.arr_stage = context.env.get_list_stage()

def before_scenario(context, scenario):
    logging.info(f'Scenario {scenario.name} started')
    for stage_config in context.arr_stage:
        if stage_config.get_stage_name() == context.stage_name:
            arr_device = stage_config.get_list_devices()
            for device in arr_device:
                if context.platform == "WEB" and device.get_platform_name() == context.platform:
                    if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                        cross_browser_with_saucelabs(context, device)
                    else:
                        launch_browser(context, device, context.browser)
                    break
                elif context.platform == "ANDROID" and device.get_platform_name() == context.platform:
                    print("android")
                    launch_android(context, device, context.config_env)
                    context.wait = device.get_wait()
                    context.time_page_load = device.get_time_page_load()
                    break
                elif context.platform == "IOS" and device.get_platform_name() == context.platform:
                    print("IOS")
                    context.wait = device.get_wait()
                    context.time_page_load = device.get_time_page_load()
                    break
            context.url = stage_config.get_list_link()
            break
    context.dict_yaml = ManagementFile().get_dict_path_yaml()
    context.logging_format = context.config_env.get('Logging', 'logging_format')


def launch_browser(context, device, browser):
    option = get_option_from_browser(browser, device)
    if device.get_auto_download_driver() is False:
        get_driver_from_path(context, browser, device, option)
    else:
        if browser == 'chrome':
            context.driver = webdriver.Chrome(options=option)
        elif browser == 'firefox':
            context.driver = webdriver.Firefox(options=option)
        elif browser == 'safari':
            context.driver = webdriver.Safari()
        else:
            logging.info("Framework only is support for chrome, firefox and safari..., trying open with chrome")
            context.driver = webdriver.Chrome(options=option)
    context.wait = device.get_wait()
    context.device = device
    context.time_page_load = device.get_time_page_load()
    context.driver.maximize_window()


def launch_android(context, device, config):
    desired_caps = {
        'platformName': device.get_platform_name(),
        'udid': device.get_udid(),
        'appPackage': device.get_app_package(),
        "appActivity": device.get_app_activity()
    }
    url = "http://" + config.get("drivers_config", "APPIUM_HOST") + ":" + str(
        config.get("drivers_config", "APPIUM_PORT")) + "/wd/hub"
    print(url)
    context.device = device
    context.wait = device.get_wait()
    context.driver = appium.webdriver.Remote(url, desired_caps)


def after_step(context, step):
    if step.status == "failed":
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day) + "_" + str(
            current_time.microsecond)
        context.driver.get_screenshot_as_file(context.evidence_path + '/' + step.name + "_" + date_time + ".png")


def after_scenario(context, scenario):
    if context.driver is not None:
        print('Closing driver from After_Scenario')
        context.driver.close()
        context.driver.quit()
    logging.info(f'Scenario {scenario.name} ended')


def after_all(context):
    if context.driver is not None:
        print('Closing driver from After_ALL')
        context.driver.close()
        context.driver.quit()
    print('------ Displaying Dictionary keys ------')
    for keys, value in context.dict_save_value.items():
        print(keys, value)
    print('------ Printed Dictionary keys ------')


def get_driver_from_path(context, browser, device, option):
    # //change due to update form selenium 4.10.0 , removed executable_path
    # https://github.com/SeleniumHQ/selenium/commit/9f5801c82fb3be3d5850707c46c3f8176e3ccd8e
    if browser == "chrome":
        service = chrome_service(
            executable_path=os.path.dirname(os.path.dirname(__file__)) + '\\' + device.get_driver_from_path())
        context.driver = webdriver.Chrome(service=service, options=option)
    elif browser == "firefox":
        service = firefox_service(
            executable_path=os.path.dirname(os.path.dirname(__file__)) + '\\' + device.get_driver_from_path())
        context.driver = webdriver.Firefox(service=service, options=option)
    elif browser == "safari":
        service = safari_service(
            executable_path=os.path.dirname(os.path.dirname(__file__)) + '\\' + device.get_driver_from_path())
        context.driver = webdriver.Safari(service=service, options=option)
    else:
        logging.info("Framework only is support for chrome, firefox and safari..., trying open with chrome")
        service = chrome_service(
            executable_path=os.path.dirname(os.path.dirname(__file__)) + '\\' + device.get_driver_from_path())
        context.driver = webdriver.Chrome(service=service, options=option)


def get_option_from_browser(browser, device):
    supported_browsers = {
        'chrome': chrome_option,
        'firefox': firefox_option,
        'safari': safari_option,
    }

    option = supported_browsers.get(browser.lower(), chrome_option)()

    if device.get_is_headless() and browser.lower() in ['chrome', 'firefox']:
        option.add_argument("--headless")

    return option
def cross_browser_with_saucelabs(context, device):
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'remote_config.ini')
    file = open(config_file_path, 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read_file(file)
    options = get_option_from_browser(config.get("remote", "browser"), device)
    options.browser_version = 'latest'
    options.platform_name = config.get("remote", "platform_name")
    sauce_options = {}
    sauce_options['username'] = config.get("remote", "username")
    sauce_options['accessKey'] = config.get("remote", "accessKey")
    sauce_options['build'] = config.get("remote", "build")
    sauce_options['name'] = config.get("remote", "name")
    options.set_capability('sauce:options', sauce_options)
    url = config.get("remote", "url")
    context.driver = webdriver.Remote(command_executor=url, options=options)
    context.wait = device.get_wait()
    context.device = device
    context.time_page_load = device.get_time_page_load()
    context.driver.maximize_window()
