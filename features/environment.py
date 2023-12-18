import configparser
import datetime
import os
import json
from selenium import webdriver
from selenium.common import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as chrome_option
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.options import Options as firefox_option
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.safari.options import Options as safari_option
from selenium.webdriver.safari.service import Service as safari_service
from appium import webdriver as appium_driver
from Utilities.action_web import ManagementFile
from Utilities.read_configuration import read_configuration
from project_runner import logger, project_folder
from sauceclient import SauceClient


def before_all(context):
    context.dict_save_value = {}
    context.driver = None
    context.root_path = project_folder
    config_file_path = os.path.join(context.root_path, 'config_env.ini')
    file = open(config_file_path, 'r')
    context.config_env = configparser.RawConfigParser(allow_no_value=True)
    context.config_env.read_file(file)
    context.platform = context.config_env.get("drivers_config", "platform").upper()
    context.highlight = context.config_env.get("drivers_config", "is_highlight").lower()
    context.project_folder = project_folder
    context.stage_name = context.config_env.get("drivers_config", "stage").upper()
    if context.config_env.has_option("drivers_config", "browser"):
        context.browser = context.config_env.get("drivers_config", "browser")
    else:
        context.browser = "chrome"
    context.env = read_configuration().read(context.stage_name)


def before_scenario(context, scenario):
    if context.platform != 'API':
        device = context.env['devices']
        context.device = list(filter(
            lambda device: device['platformName'] == context.platform, device
        ))
        if len(context.device) == 0:
            logger.error('Framework only is support for chrome, firefox and safari..., trying open with chrome')
        context.device = context.device[0]
        match context.device['platformName'].upper():
            case "WEB":
                if context.device['is_headless']: context.highlight = 'false'
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    cross_browser_with_web(context, context.device)
                else:
                    launch_browser(context, context.device, context.browser)
            case "ANDROID":
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    cross_browser_with_mobile(context, context.device)
                else:
                    launch_mobile(context, context.device, context.config_env)
                    context.wait = context.device['wait']
                    context.highlight = 'false'
            case "IOS":
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    cross_browser_with_mobile(context, context.device)
                else:
                    launch_mobile(context, context.device, context.config_env)
                    context.wait = context.device['wait']
                    context.highlight = 'false'
            case fail:
                logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
                assert False, "Framework only is support for chrome, firefox and safari..., trying open with chrome"
        context.url = context.env['link']

    context.apiurls = context.env['apifacets']['link']
    context.endpoints = read_configuration().read_api_endpoints()
    logger.info(f'Scenario {scenario.name} started')
    context.dict_yaml = ManagementFile().get_dict_path_yaml()
    context.dict_page_element = {}


def launch_browser(context, device, browser):
    option = get_option_from_browser(browser, device)
    if device['auto_download_driver'] is False:
        get_driver_from_path(context, browser, device, option)
    else:
        match browser:
            case 'chrome':
                context.driver = webdriver.Chrome(options=option)
            case 'firefox':
                context.driver = webdriver.Firefox(options=option)
            case 'safari':
                context.driver = webdriver.Safari()
            case fail:
                logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
                context.driver = webdriver.Chrome(options=option)
    context.wait = device['wait']
    context.time_page_load = device['time_page_load']
    context.driver.maximize_window()

def launch_mobile(context, device, config):
    try:
        desired_caps = get_data_config_mobile(context, device)
        context.wait = device['wait']
        context.driver = appium_driver.Remote(desired_caps['appium_url'], desired_capabilities=desired_caps)
    except SessionNotCreatedException as ex:
        logger.error('Config file updated based on user provided command line arguments')
        print("not connect with remote saucelab, please check configuration again!")
        assert False, f'{ex.msg}'

def after_step(context, step):
    if step.status == 'failed':
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(
            current_time.microsecond)
        context.driver.get_screenshot_as_file(context.evidence_path + '/' + step.name + '_' + date_time + '.png')

def after_scenario(context, scenario):
    if context.driver:
        context.driver.quit()
        if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
            config = read_config_remote()
            sauce_client = SauceClient(config.get("remote", "username"), config.get("remote", "accessKey"))
            test_status = scenario.status == 'passed'
            sauce_client.jobs.update_job(context.driver.session_id, passed=test_status)
    logger.info(f'Scenario {scenario.name} Ended')

def after_all(context):
    if context.driver and context.platform == 'WEB':
        logger.info('Closing driver from After_ALL')
        context.driver.close()
        context.driver.quit()

def get_driver_from_path(context, browser, device, option):
    # //change due to update form selenium 4.10.0 , removed executable_path
    # https://github.com/SeleniumHQ/selenium/commit/9f5801c82fb3be3d5850707c46c3f8176e3ccd8e
    if browser == 'chrome':
        service = chrome_service(
            executable_path=project_folder + '\\' + device['driver_path'])
        context.driver = webdriver.Chrome(service=service, options=option)
    elif browser == 'firefox':
        service = firefox_service(
            executable_path=project_folder + '\\' + device['driver_path'])
        context.driver = webdriver.Firefox(service=service, options=option)
    elif browser == 'safari':
        service = safari_service(
            executable_path=project_folder + '\\' + device['driver_path'])
        context.driver = webdriver.Safari(service=service, options=option)
    else:
        logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
        service = chrome_service(
            executable_path=project_folder + '\\' + device['driver_version'])
        context.driver = webdriver.Chrome(service=service, options=option)

def get_option_from_browser(browser, device):
    supported_browsers = {
        'chrome': chrome_option,
        'firefox': firefox_option,
        'safari': safari_option,
    }
    option = supported_browsers.get(browser.lower(), chrome_option)()
    if device['is_headless'] and browser.lower() in ['chrome', 'firefox']:
        option.add_argument('--headless')
    return option
def cross_browser_with_web(context, device):
    config = read_config_remote()
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
    context.wait = device['wait']
    context.device = device
    context.time_page_load = device['time_page_load']
    context.driver.maximize_window()


def cross_browser_with_mobile(context, device):
    config = read_config_remote()
    caps = get_data_config_mobile(context, device)
    caps['sauce:options'] = {}
    caps['sauce:options']['appiumVersion'] = '2.0.0'
    caps['sauce:options']['username'] = config.get("remote", "username")
    caps['sauce:options']['accessKey'] = config.get("remote", "accessKey")
    caps['sauce:options']['build'] = config.get("remote", "build")
    caps['sauce:options']['name'] = config.get("remote", "name")
    caps['sauce:options']['deviceOrientation'] = 'PORTRAIT'
    context.wait = device['wait']
    context.device = device
    context.driver = appium_driver.Remote(config.get("remote", "url"), desired_capabilities=caps)

def get_data_config_mobile(context, device):
    config_file_path = os.path.join(context.root_path, device['config_file'])
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    return data
def read_config_remote():
    config_file_path = os.path.join(project_folder, 'remote_config.ini')
    file = open(config_file_path, 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read_file(file)
    return config