from time import time, sleep

from behave import step

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from .utils import safe_get_element_text, expand_shadow_root


@step('I click the "{button}" button in the get-started-page')
def click_button_get_started(context, button):
    try:
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = expand_shadow_root(context, landing_app)
        pages = shadow_root.find_element_by_id('pages')
        get_started = pages.find_element_by_id('get-started')
        inner_shadow_root = expand_shadow_root(context, get_started)
        container = inner_shadow_root.find_element_by_id('container')
        buttons = container.find_elements_by_tag_name('paper-button')

        for btn in buttons:
            if safe_get_element_text(btn).lower() == button.lower():
                btn.click()
                return

    except NoSuchElementException as ElementNotVisibleException:
        # get-started page does not make sense for io
        pass


@step('I open the {kind} popup')
def open_login_popup(context, kind):
    kind = kind.lower()
    modals = {'login': 'modalLogin', 'signup': 'modalRegister'}
    if kind.lower() not in list(modals.keys()):
        raise ValueError('No such popup in the landing page')
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = expand_shadow_root(context, landing_app)
    if shadow_root is None:
        sleep(1)
        shadow_root = expand_shadow_root(context, landing_app)

    if kind == 'login':
        app_toolbar = shadow_root.find_element_by_css_selector("app-toolbar")
        if app_toolbar is None:
            sleep(1)
            app_toolbar = shadow_root.find_element_by_css_selector("app-toolbar")
        sign_in_class = app_toolbar.find_element_by_class_name('signin-btn-container')
        a = sign_in_class.find_element_by_tag_name("a")
        button_to_click = a.find_element_by_tag_name("paper-button")

    elif kind == 'signup':
        landing_pages = shadow_root.find_element_by_css_selector('landing-pages')
        landing_home = landing_pages.find_element_by_tag_name("landing-home")
        inner_shadow_root = expand_shadow_root(context, landing_home)
        container = inner_shadow_root.find_element_by_id('container')
        landing_fold = container.find_element_by_tag_name('landing-fold')
        a = landing_fold.find_element_by_tag_name("a")
        button_to_click = a.find_element_by_tag_name("paper-button")

    if button_to_click.is_displayed():
        button_to_click.click()


@step("I click the {text} button in the landing page popup")
def click_button_in_landing_page(context, text):
    from .buttons import clicketi_click
    text = text.lower()
    if text not in ['email', 'google', 'github', 'sign in', 'sign up',
                    'submit', 'forgot password', 'reset_password_email_submit',
                    'reset_pass_submit', 'go', 'sign in with active directory',
                    'sign in with ldap']:
        raise ValueError('This button does not exist in the landing page popup')

    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = expand_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")

    if text in ['sign in', 'forgot password', 'google', 'github',
                'sign in with active directory', 'sign in with ldap']:
        page = landing_pages.find_element_by_tag_name('landing-sign-in')
    elif text.lower() == 'sign up':
        page = landing_pages.find_element_by_tag_name('landing-sign-up')
    elif text.lower() == 'go':
        page = landing_pages.find_element_by_tag_name('landing-set-password')
    elif text.lower() == 'reset_password_email_submit':
        page = landing_pages.find_element_by_tag_name('landing-forgot-password')
    elif text.lower() == 'reset_pass_submit':
        page = landing_pages.find_element_by_tag_name('landing-reset-password')

    shadow_root = expand_shadow_root(context, page)
    iron_form = shadow_root.find_element_by_css_selector('iron-form')
    form = iron_form.find_element_by_tag_name('form')

    if text == 'sign in':
        popup = form.find_element_by_id('signInSubmit')
    elif text == 'sign up':
        popup = form.find_element_by_id('signUpSubmit')
    elif text == 'go':
        popup = form.find_element_by_id('setPasswordSubmit')
    elif text == 'forgot password':
        popup = form.find_element_by_id('forgotPasswordLink')
    elif text == 'reset_password_email_submit':
        popup = form.find_element_by_id('forgotPasswordSubmit')
    elif text == 'reset_pass_submit':
        popup = form.find_element_by_id('resetPasswordSubmit')
    elif text == 'google':
        popup = shadow_root.find_element_by_id('signInBtnGoogle')
    elif text == 'github':
        popup = shadow_root.find_element_by_id('signInBtnGithub')
    elif text == 'sign in with active directory':
        popup = shadow_root.find_element_by_id('signInBtnAd')
    elif text == 'sign in with ldap':
        popup = shadow_root.find_elements_by_id('signInBtnLdap')

    clicketi_click(context, popup)
    return


def get_mist_config_email(context,kind):
    if kind == 'invalid_email':
        return 'tester'
    elif kind == 'rbac_member1':
        return context.mist_config['MEMBER1_EMAIL']
    elif kind == 'rbac_member2':
        return context.mist_config['MEMBER2_EMAIL']
    elif kind == 'ad':
        return context.mist_config['AD_MEMBER_USERNAME']
    elif kind == 'ldap':
        return context.mist_config['LDAP_MEMBER_USERNAME']
    else:
        return context.mist_config['EMAIL']


def get_mist_config_password(context,kind):
    if kind in ['alt', 'new_creds']:
        return context.mist_config['PASSWORD2']
    elif kind == 'changed':
        return context.mist_config['CHANGED_PASSWORD']
    elif kind == 'rbac_member1':
        return context.mist_config['MEMBER1_PASSWORD']
    elif kind == 'rbac_member2':
        return context.mist_config['MEMBER2_PASSWORD']
    elif kind == 'ad':
        return context.mist_config['AD_MEMBER_PASSWORD']
    elif kind == 'ldap':
        return context.mist_config['LDAP_MEMBER_PASSWORD']
    else:
        return context.mist_config['PASSWORD1']


@step('I enter my {kind} credentials for {action}')
def enter_credentials(context, kind, action):
    kind = kind.lower()
    action = action.lower()
    if action not in ['login', 'ldap login', 'signup',
                      'signup_password_set', 'password_reset_request',
                      'password_reset', 'demo request']:
        raise ValueError("Cannot input %s credentials" % action)
    if kind not in ['standard', 'alt', 'rbac_owner', 'rbac_member1', 'ad', 'ldap',
                    'rbac_member2', 'new_creds', 'changed'] and not kind.startswith('invalid'):
        raise ValueError("No idea what %s credentials are" % kind)

    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = expand_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")

    if action == 'login':
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = expand_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        email_paper_input = form.find_element_by_id("signin-email")
        email_shadow = expand_shadow_root(context, email_paper_input)
        email_container = email_shadow.find_element_by_id('container')
        email_input = email_container.find_element_by_tag_name('input')
        email_input.send_keys(get_mist_config_email(context, kind))

        password_paper_input = form.find_element_by_id("signin-password")
        password_shadow = expand_shadow_root(context, password_paper_input)
        password_container = password_shadow.find_element_by_id('container')
        password_input = password_container.find_element_by_tag_name('input')
        password_input.send_keys(get_mist_config_password(context, kind))

    elif action == "ldap login":
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = expand_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        username_paper_input = form.find_element_by_id("signin-username")
        username_shadow = expand_shadow_root(context, username_paper_input)
        username_container = username_shadow.find_element_by_id('container')
        username_input = username_container.find_element_by_tag_name('input')
        username_input.send_keys(get_mist_config_email(context, kind))

        password_paper_input = form.find_element_by_id("signin-password")
        password_shadow = expand_shadow_root(context, password_paper_input)
        password_container = password_shadow.find_element_by_id('container')
        password_input = password_container.find_element_by_tag_name('input')
        password_input.send_keys(get_mist_config_password(context, kind))

    elif action == 'signup':
        sign_up_class = landing_pages.find_element_by_tag_name('landing-sign-up')
        shadow_root = expand_shadow_root(context, sign_up_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        name_paper_input = form.find_element_by_id("name")
        name_shadow = expand_shadow_root(context, name_paper_input)
        name_container = name_shadow.find_element_by_id('container')
        name_input = name_container.find_element_by_tag_name('input')
        name_input.send_keys(context.mist_config['NAME'])

        email_paper_input = form.find_element_by_id("signUp-email")
        email_shadow = expand_shadow_root(context, email_paper_input)
        email_container = email_shadow.find_element_by_id('container')
        email_input = email_container.find_element_by_tag_name('input')
        email_input.send_keys(get_mist_config_email(context, kind))

    elif action == 'password_reset_request':
        password_reset_class = landing_pages.find_element_by_tag_name('landing-forgot-password')
        shadow_root = expand_shadow_root(context, password_reset_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        email_paper_input = form.find_element_by_id("forgotPassword-email")
        email_shadow = expand_shadow_root(context, email_paper_input)
        email_container = email_shadow.find_element_by_id('container')
        email_input = email_container.find_element_by_tag_name('input')
        email_input.send_keys(get_mist_config_email(context, kind))

    elif action == 'password_reset':
        password_reset_class = landing_pages.find_element_by_tag_name('landing-reset-password')
        shadow_root = expand_shadow_root(context, password_reset_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')

        mist_password = form.find_element_by_tag_name('mist-password')
        shadow_root = expand_shadow_root(context, mist_password)

        password_paper_input = shadow_root.find_element_by_css_selector('paper-input')
        password_shadow = expand_shadow_root(context, password_paper_input)
        password_container = password_shadow.find_element_by_id('container')
        password_input = password_container.find_element_by_tag_name('input')
        password_input.send_keys(get_mist_config_password(context, kind))

    elif action == 'signup_password_set':
        set_password_class = landing_pages.find_element_by_tag_name('landing-set-password')

        shadow_root = expand_shadow_root(context, set_password_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        mist_password = form.find_element_by_tag_name('mist-password')
        shadow_root = expand_shadow_root(context, mist_password)

        password_paper_input = shadow_root.find_element_by_css_selector('paper-input')
        password_shadow = expand_shadow_root(context, password_paper_input)
        password_container = password_shadow.find_element_by_id('container')
        password_input = password_container.find_element_by_tag_name('input')
        password_input.send_keys(get_mist_config_password(context, kind))


@step('there should be an "{error_message}" error message inside the "{button}" button')
def check_error_message(context, error_message, button):
    button = button.lower()
    error_message = error_message.lower()
    if button not in ['sign in']:
        raise Exception('Unknown type of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = expand_shadow_root(context, landing_app)
        landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = expand_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        login_popup = form.find_element_by_id('signInSubmit')
        text = safe_get_element_text(login_popup).lower()

    if text == error_message:
        return
    assert False, "Error message was not %s but instead %s" % \
                                                  (error_message, text)


@step('the {button} button should be {state}')
def check_state_of_button(context, button, state):
    state = state.lower()
    if state not in ['clickable', 'not clickable']:
        raise Exception('Unknown state of button')
    if button == 'sign in':
        landing_app = context.browser.find_element_by_tag_name("landing-app")
        shadow_root = expand_shadow_root(context, landing_app)
        landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
        sign_in_class = landing_pages.find_element_by_tag_name('landing-sign-in')
        shadow_root = expand_shadow_root(context, sign_in_class)
        iron_form = shadow_root.find_element_by_css_selector('iron-form')
        form = iron_form.find_element_by_tag_name('form')
        login_popup = form.find_element_by_id('signInSubmit')
        is_not_clickable = login_popup.get_attribute('aria-disabled')

    if state == 'clickable' and is_not_clickable == 'false':
        return
    elif state == 'not clickable' and is_not_clickable == 'true':
        return
    else:
        assert False, "Desired state of the %s button is %s, but it is not!" % \
                                        (button, state)


@step('I should get a conflict error')
def already_registered(context):
    landing_app = context.browser.find_element_by_tag_name("landing-app")
    shadow_root = expand_shadow_root(context, landing_app)
    landing_pages = shadow_root.find_element_by_css_selector("landing-pages")
    sign_up_class = landing_pages.find_element_by_tag_name('landing-sign-up')
    shadow_root = expand_shadow_root(context, sign_up_class)
    iron_form = shadow_root.find_element_by_css_selector('iron-form')
    form = iron_form.find_element_by_tag_name('form')
    error_msg = form.find_element_by_id("signUpSubmit")
    if 'conflict' in safe_get_element_text(error_msg).lower():
        return
    assert False, 'No conflict message appeared'


@step('I should see the landing page within {seconds} seconds')
def wait_for_landing_page(context, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_tag_name('landing-app')
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "Landing page is not visible after waiting for %s seconds"\
                  % seconds


@step('that I am redirected within {seconds} seconds')
def ensure_redirection(context, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_id("top-signup-button")
            sleep(1)
        except NoSuchElementException:
            return True
    assert False, "I wasn't redirected to the app after waiting for %s seconds"\
                  % seconds
