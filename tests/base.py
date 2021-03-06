from nose.tools import assert_equals, assert_true, assert_false
from fake_webapp import EXAMPLE_APP

from find_elements import FindElementsTest
from form_elements import FormElementsTest
from click_elements import ClickElementsTest
from element_does_not_exist import ElementDoestNotExistTest
from is_element_present import IsElementPresentTest
from iframes import IFrameElementsTest
from status_code import StatusCodeTest
from async_finder import AsyncFinderTests
from is_text_present import IsTextPresentTest
from within_elements import WithinElementsTest


class BaseBrowserTests(FindElementsTest, FormElementsTest, ClickElementsTest, WithinElementsTest):

    def setUp(self):
        self.fail("You should set up your browser in the setUp() method")

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        title = self.browser.title
        assert_equals(title, 'Example Title')

    def test_can_back_on_history(self):
        "should be able to back on history"
        self.browser.visit("%s/iframe" % EXAMPLE_APP.rstrip('/'))
        self.browser.back()
        assert_equals(EXAMPLE_APP, self.browser.url)

    def test_can_forward_on_history(self):
        "should be able to forward history"
        url = "%s/iframe" % EXAMPLE_APP.rstrip('/')
        self.browser.visit(url)
        self.browser.back()
        self.browser.forward()
        assert_equals(url, self.browser.url)

    def test_should_have_html(self):
        "should have access to the html"
        html = self.browser.html
        assert '<title>Example Title</title>' in html
        assert '<h1 id="firstheader">Example Header</h1>' in html

    def test_should_reload_a_page(self):
        "should reload a page"
        title = self.browser.title
        self.browser.reload()
        assert_equals(title, 'Example Title')

    def test_should_have_url(self):
        "should have access to the url"
        url = self.browser.url
        assert_equals(url, EXAMPLE_APP)

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO').first
        assert_equals(foo['href'], '/foo')

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css('input[name="send"]').first
        assert_equals(button['name'], 'send')

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css('h1').first
        assert_equals(header['id'], 'firstheader')

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('/foo').first
        assert_equals(foo.value, 'FOO')

    def test_should_receive_browser_on_parent(self):
        "element should contains the browser on \"parent\" attribute"
        element = self.browser.find_by_id("firstheader").first
        assert_equals(element.parent, self.browser)

class WebDriverTests(BaseBrowserTests, IFrameElementsTest, ElementDoestNotExistTest, IsElementPresentTest, AsyncFinderTests, IsTextPresentTest, StatusCodeTest):

    def test_can_execute_javascript(self):
        "should execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.browser.find_by_tag("body") == ""

    def test_can_evaluate_script(self):
        "should evaluate script"
        assert self.browser.evaluate_script("4+4") == 8

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        assert_true(self.browser.find_by_id("visible").first.visible)

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        assert_false(self.browser.find_by_id("invisible").first.visible)

    def test_default_wait_time_should_be_2(self):
        "should driver default wait time 2"
        assert_equals(self.browser.wait_time, 2)
