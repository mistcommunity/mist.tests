from behave import step

from misttests.helpers.selenium_utils import choose_driver


@step('I launch a second browser')
def launch_second_browser(context):
    if not context.mist_config.get('browser2'):
        context.mist_config['browser2'] = choose_driver()


@step('I quit the second browser')
def quit_second_browser(context):
    switch_active_browser(context)
    context.mist_config['browser2'].quit()
    del context.mist_config['browser2']


@step('I switch browser')
def switch_active_browser(context):
    assert context.mist_config.get('browser2'), \
        'There is no second instance of a browser'
    browser2 = context.mist_config['browser2']
    context.mist_config['browser2'] = context.mist_config['browser']
    context.mist_config['browser'] = browser2
    context.browser = context.mist_config['browser']


@step('I refresh the page')
def refresh_the_page(context):
    context.browser.refresh()


@step('I visit mist_url')
def visit_home_page(context):
    url = context.mist_config['MIST_URL']
    if not url.endswith('/'):
        url += '/'
    context.browser.get(url)
