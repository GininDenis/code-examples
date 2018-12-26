import environ
import time

from splinter import Browser


class PaymentHostsRecorder:
    BROWSER_WINDOW_SIZE = (1024, 768)

    def __init__(self):
        env = environ.Env()
        self.controller_url = env('CONTROLLER_URL')
        self.username = env('CONTROLLER_USERNAME')
        self.password = env('CONTROLLER_PASSWORD')
        self.browser = self._setup_browser()

    @staticmethod
    def _setup_browser():
        """
        Prepare splinter browser
        :return: Browser
        """
        return Browser(driver_name='chrome', headless=False)

    def _open_page(self):
        self.browser.visit(self.controller_url)

    def _resize_window(self):
        self.browser.driver.set_window_size(*self.BROWSER_WINDOW_SIZE)

    def _do_auth(self):
        self.browser.fill('username', self.username)
        self.browser.fill('password', self.password)
        self.browser.find_by_id('loginButton').click()

    def _get_hotspot_page(self):
        self.browser.find_by_tag('unifi-settings-side-nav').click()
        time.sleep(1)
        self.browser.find_by_xpath(
            '//li[@pageutils-nav-state="manage.site.settings.guestcontrol"]').last.click()  # noqa

    def _remove_hosts(self):
        self.browser.execute_script(
            "items = document.getElementsByClassName('removeAllowedSubnet')"
        )
        self.browser.execute_script("while (items[0]) {items[0].click() }")
        self.browser.execute_script(
            "button=document.getElementsByClassName('appMainButton--success')"
        )
        self.browser.execute_script("button.item(0).click()")

    def _add_hosts(self):
        element = self.browser.find_by_xpath(
            '//button[@ng-click="repeatableFormCtrl.addItem()"]'
        ).first
        hosts_pool = open('payment_ip_pool.txt')
        host = hosts_pool.readline().replace('\n', '')
        hosts_count = 0
        while host:
            element.click()
            name = 'guestControlAllowedSubnet{}'.format(hosts_count)
            self.browser.fill(name, host)
            host = hosts_pool.readline().replace('\n', '')
            hosts_count += 1
        hosts_pool.close()
        self.browser.execute_script(
            "button=document.getElementsByClassName('appMainButton--success')")
        self.browser.execute_script("button.item(0).click()")

    def _prepare_page(self):
        self._open_page()
        self._resize_window()
        self._do_auth()
        self._get_hotspot_page()

    def fill(self):
        self._prepare_page()
        self._add_hosts()

    def delete(self):
        self._prepare_page()
        self._remove_hosts()
