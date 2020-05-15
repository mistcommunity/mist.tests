import json

from behave import step

from misttests.config import safe_get_var
from time import time
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException

from .utils import safe_get_element_text, expand_shadow_root, get_page_element, has_finished_loading, add_credit_card_if_needed

from .forms import set_value_to_field, get_add_form
from .forms import clear_input_and_send_keys

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from .dialog import get_dialog


def set_gce_creds(context):
    project_id = safe_get_var('clouds/gce/mist-dev', 'project_id', context.mist_config['CREDENTIALS']['GCE']['project_id'])
    private_key = safe_get_var('clouds/gce/mist-dev', 'private_key', context.mist_config['CREDENTIALS']['GCE']['private_key'])
    context.execute_steps(u'''
            Then I set the value "%s" to field "Title" in the "cloud" add form
            Then I set the value "%s" to field "Project ID" in the "cloud" add form
            Then I set the value "%s" to field "Private Key" in the "cloud" add form
            And I click the "Enable DNS support" toggle button in the "cloud" add form
        ''' % ('Google Cloud', project_id, json.dumps(private_key).replace('"', '\"')))


def set_rackspace_creds(context):
    region = safe_get_var('clouds/rackspace', 'region', context.mist_config['CREDENTIALS']['RACKSPACE']['region'])
    username = safe_get_var('clouds/rackspace', 'username', context.mist_config['CREDENTIALS']['RACKSPACE']['username'])
    api_key = safe_get_var('clouds/rackspace', 'api_key', context.mist_config['CREDENTIALS']['RACKSPACE']['api_key'])
    context.execute_steps(u'''
        Then I open the "Region" dropdown in the "cloud" add form
        And I wait for 1 seconds
        When I click the "%s" button in the "Region" dropdown in the "cloud" add form
        Then I set the value "Rackspace" to field "Title" in the "cloud" add form
        Then I set the value "%s" to field "Username" in the "cloud" add form
        Then I set the value "%s" to field "API Key" in the "cloud" add form
    ''' % (region, username, api_key))


def set_ibm_clouds_creds(context):
    username = safe_get_var('clouds/softlayer', 'username', context.mist_config['CREDENTIALS']['SOFTLAYER']['username'])
    api_key = safe_get_var('clouds/softlayer', 'api_key', context.mist_config['CREDENTIALS']['SOFTLAYER']['api_key'])
    context.execute_steps(u'''
        Then I set the value "%s" to field "Username" in the "cloud" add form
        Then I set the value "%s" to field "API Key" in the "cloud" add form
    ''' % (username, api_key))


def set_aws_creds(context):
    api_key = safe_get_var('clouds/aws', 'api_key', context.mist_config['CREDENTIALS']['EC2']['api_key'])
    api_secret = safe_get_var('clouds/aws', 'api_secret', context.mist_config['CREDENTIALS']['EC2']['api_secret'])
    region = safe_get_var('clouds/aws', 'region', context.mist_config['CREDENTIALS']['EC2']['region'])
    context.execute_steps(u'''
        Then I open the "Region" dropdown in the "cloud" add form
        And I wait for 1 seconds
        When I click the "%s" button in the "Region" dropdown in the "cloud" add form
        And I wait for 1 seconds
        Then I set the value "Amazon Web Services" to field "Title" in the "cloud" add form
        And I set the value "%s" to field "API Key" in the "cloud" add form
        And I set the value "%s" to field "API Secret" in the "cloud" add form
    ''' % (region, api_key, api_secret))


def set_aws_adv_creds(context):
    api_key = safe_get_var('clouds/aws_advantis', 'api_key', context.mist_config['CREDENTIALS']['EC2']['api_key'])
    api_secret = safe_get_var('clouds/aws_advantis', 'api_secret', context.mist_config['CREDENTIALS']['EC2']['api_secret'])
    region = safe_get_var('clouds/aws_advantis', 'region', context.mist_config['CREDENTIALS']['EC2']['region'])
    context.execute_steps(u'''
        Then I open the "Region" dropdown in the "cloud" add form
        And I wait for 1 seconds
        When I click the "%s" button in the "Region" dropdown in the "cloud" add form
        And I wait for 1 seconds
        Then I set the value "AWS Advantis" to field "Title" in the "cloud" add form
        And I set the value "%s" to field "API Key" in the "cloud" add form
        And I set the value "%s" to field "API Secret" in the "cloud" add form
    ''' % (region, api_key, api_secret))


def set_linode_creds(context):
    api_key = safe_get_var('clouds/linode', 'api_key', context.mist_config['CREDENTIALS']['LINODE']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'the "cloud" add form' % api_key)


def set_do_creds(context):
    token = safe_get_var('clouds/digitalocean', 'token', context.mist_config['CREDENTIALS']['DIGITALOCEAN']['token'])
    context.execute_steps(u'Then I set the value "%s" to field "Token" in the '
                          u'"cloud" add form' % token)


def set_docker_orchestrator_creds(context):
    host = safe_get_var('clouds/docker_orchestrator', 'host', context.mist_config['CREDENTIALS']['DOCKER_ORCHESTRATOR']['host'])
    port = safe_get_var('clouds/docker_orchestrator', 'port', context.mist_config['CREDENTIALS']['DOCKER_ORCHESTRATOR']['port'])
    context.execute_steps(u'''
                Then I set the value "Docker_Orchestrator" to field "Title" in the "cloud" add form
                Then I set the value "%s" to field "Host" in the "cloud" add form
                Then I set the value "%s" to field "Port" in the "cloud" add form
            ''' % (host, port))

def set_docker_creds(context):
    if context.mist_config['LOCAL']:
        host = context.mist_config['LOCAL_DOCKER']
        port = '2375'
        context.execute_steps(u'''
                Then I set the value "Docker" to field "Title" in the "cloud" add form
                Then I set the value "%s" to field "Host" in the "cloud" add form
                Then I set the value "%s" to field "Port" in the "cloud" add form
        ''' % (host, port))
    else:
        host = safe_get_var('dockerhosts/godzilla', 'host', context.mist_config['CREDENTIALS']['DOCKER']['host'])
        port = safe_get_var('dockerhosts/godzilla', 'port', context.mist_config['CREDENTIALS']['DOCKER']['port'])
        context.execute_steps(u'''
                Then I set the value "Docker" to field "Title" in the "cloud" add form
                Then I set the value "%s" to field "Host" in the "cloud" add form
                Then I set the value "%s" to field "Port" in the "cloud" add form
            ''' % (host, port))

        certificate = safe_get_var('dockerhosts/godzilla', 'cert', context.mist_config['CREDENTIALS']['DOCKER']['cert'])
        key = safe_get_var('dockerhosts/godzilla', 'key', context.mist_config['CREDENTIALS']['DOCKER']['key'])
        ca = safe_get_var('dockerhosts/godzilla', 'ca', context.mist_config['CREDENTIALS']['DOCKER']['ca'])

        set_value_to_field(context, key, 'key', 'cloud', 'add')
        set_value_to_field(context, certificate, 'certificate', 'cloud', 'add')
        set_value_to_field(context, ca, 'ca certificate', 'cloud', 'add')


def set_packet_creds(context):
    api_key = safe_get_var('clouds/packet', 'api_key', context.mist_config['CREDENTIALS']['PACKET']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in the '
                          u'"cloud" add form' % api_key)


def set_openstack_creds(context):
    context.execute_steps(u'''
            Then I set the value "OpenStack" to field "Title" in the "cloud" add form
            Then I set the value "%s" to field "Username" in the "cloud" add form
            Then I set the value "%s" to field "Password" in the "cloud" add form
            Then I set the value "%s" to field "Auth Url" in the "cloud" add form
            Then I set the value "%s" to field "Tenant Name" in the "cloud" add form
        ''' % (safe_get_var('clouds/openstack_newton', 'username', context.mist_config['CREDENTIALS']['OPENSTACK']['username']),
               safe_get_var('clouds/openstack_newton', 'password', context.mist_config['CREDENTIALS']['OPENSTACK']['password']),
               safe_get_var('clouds/openstack_newton', 'auth_url', context.mist_config['CREDENTIALS']['OPENSTACK']['auth_url']),
               safe_get_var('clouds/openstack_newton', 'tenant', context.mist_config['CREDENTIALS']['OPENSTACK']['tenant']),))


def set_hostvirtual_creds(context):
    api_key = safe_get_var('clouds/hostvirtual', 'api_key', context.mist_config['CREDENTIALS']['HOSTVIRTUAL']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" add form' % api_key)


def set_vultr_creds(context):
    api_key = safe_get_var('clouds/vultr', 'apikey', context.mist_config['CREDENTIALS']['VULTR']['apikey'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in the "cloud" add form' % api_key)


def set_aliyun_creds(context):
    context.execute_steps(u'''
                        Then I open the "Region" dropdown in the "cloud" add form
                        Then I wait for 2 seconds
                        Then I click the "US West 1 (Silicon Valley)" button in the "Region" dropdown in the "cloud" add form
                        Then I wait for 1 seconds
                        Then I set the value "Alibaba Cloud" to field "Title" in the "cloud" add form
                        Then I set the value "%s" to field "API Key" in the "cloud" add form
                        Then I set the value "%s" to field "API Secret" in the "cloud" add form
                    ''' % (safe_get_var('clouds/aliyun', 'api_key', context.mist_config['CREDENTIALS']['ALIYUN']['api_key']),
                           safe_get_var('clouds/aliyun', 'api_secret', context.mist_config['CREDENTIALS']['ALIYUN']['api_secret'])))

def set_azure_arm_creds(context):
    context.execute_steps(u'''
                    Then I set the value "Microsoft Azure" to field "Title" in the "cloud" add form
                    Then I set the value "%s" to field "Tenant ID" in the "cloud" add form
                    Then I set the value "%s" to field "Subscription ID" in the "cloud" add form
                    Then I set the value "%s" to field "Client Key" in the "cloud" add form
                    Then I set the value "%s" to field "Client Secret" in the "cloud" add form
                ''' % (safe_get_var('clouds/azure_arm', 'tenant_id', context.mist_config['CREDENTIALS']['AZURE_ARM']['tenant_id']),
                       safe_get_var('clouds/azure_arm', 'subscription_id', context.mist_config['CREDENTIALS']['AZURE_ARM']['subscription_id']),
                       safe_get_var('clouds/azure_arm', 'client_key', context.mist_config['CREDENTIALS']['AZURE_ARM']['client_key']),
                       safe_get_var('clouds/azure_arm', 'client_secret', context.mist_config['CREDENTIALS']['AZURE_ARM']['client_secret']),))


def set_kvm_creds(context):
    context.execute_steps(u'''
                    Then I set the value "KVM" to field "Title" in the "cloud" add form
                    Then I set the value "%s" to field "KVM hostname or IP" in the "cloud" add form
                    And I wait for 1 seconds
                    And I open the "SSH Key" dropdown in the "cloud" add form
                    And I wait for 2 seconds
                    And I click the "KVMKEY" button in the "SSH Key" dropdown in the "cloud" add form
                    And I wait for 1 seconds
                    And I set the value "ubuntu" to field "SSH USER" in the "cloud" add form
                ''' % (safe_get_var('clouds/other_server', 'hostname', context.mist_config['CREDENTIALS']['KVM']['hostname']),))


def set_other_server_creds(context):
    hostname = safe_get_var('clouds/other_server', 'hostname', context.mist_config['CREDENTIALS']['KVM']['hostname'])
    context.mist_config['bare_metal_host'] = hostname
    context.execute_steps(u'''
                    Then I set the value "Bare Metal" to field "Cloud Title" in the "cloud" add form
                    Then I set the value "%s" to field "Hostname" in the "cloud" add form
                    And I wait for 1 seconds
                    And I open the "SSH Key" dropdown in the "cloud" add form
                    And I wait for 2 seconds
                    And I click the "KVMKEY" button in the "SSH Key" dropdown in the "cloud" add form
                    And I wait for 1 seconds
                ''' % hostname)


def set_vsphere_creds(context):
    context.execute_steps(u'''
                # Then I set the value "%s" to field "Username" in the "cloud" add form
                # Then I set the value "%s" to field "Password" in the "cloud" add form
                Then I set the value "%s" to field "CA Certificate" in the "cloud" add form
                Then I set the value "%s" to field "Hostname" in the "cloud" add form
            ''' % (safe_get_var('clouds/VCenter-packet', 'username', context.mist_config['CREDENTIALS']['VSPHERE']['username']),
                   safe_get_var('clouds/VCenter-packet', 'password', context.mist_config['CREDENTIALS']['VSPHERE']['password']),
                   safe_get_var('clouds/VCenter-packet', 'ca_cert', context.mist_config['CREDENTIALS']['VSPHERE']['ca']),
                   safe_get_var('clouds/VCenter-packet', 'host', context.mist_config['CREDENTIALS']['VSPHERE']['host']),))


def set_onapp_creds(context):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Username" in the "cloud" add form
                Then I set the value "%s" to field "Password" in the "cloud" add form
                Then I set the value "%s" to field "Host" in the "cloud" add form
                And I click the "Verify SSL certificate" toggle button in the "cloud" add form
            ''' % (safe_get_var('clouds/onapp', 'username', context.mist_config['CREDENTIALS']['ONAPP']['username']),
                   safe_get_var('clouds/onapp', 'password', context.mist_config['CREDENTIALS']['ONAPP']['password']),
                   safe_get_var('clouds/onapp', 'host', context.mist_config['CREDENTIALS']['ONAPP']['host']),))


def set_second_packet_creds(context):
    api_key = safe_get_var('clouds/packet_2', 'api_key', context.mist_config['CREDENTIALS']['PACKET_2']['api_key'])
    context.execute_steps(u'Then I set the value "%s" to field "API Key" in '
                          u'"cloud" edit form' % api_key)


def set_maxihost_creds(context):
    api_key = safe_get_var('clouds/maxihost', 'api_token', context.mist_config['CREDENTIALS']['MAXIHOST']['api_token'])
    context.execute_steps(u'''
                Then I set the value "%s" to field "API token" in the "cloud" add form
            ''' % api_key)


def set_second_openstack_creds(context):
    context.execute_steps(u'''
                Then I set the value "%s" to field "Username" in the "cloud" edit form
                Then I set the value "%s" to field "Password" in the "cloud" edit form
                Then I set the value "%s" to field "Auth Url" in the "cloud" edit form
                Then I set the value "%s" to field "Tenant Name" in the "cloud" edit form
            ''' % (safe_get_var('clouds/openstack_2', 'username', context.mist_config['CREDENTIALS']['OPENSTACK_2']['username']),
                   safe_get_var('clouds/openstack', 'password', context.mist_config['CREDENTIALS']['OPENSTACK_2']['password']),
                   safe_get_var('clouds/openstack', 'auth_url', context.mist_config['CREDENTIALS']['OPENSTACK_2']['auth_url']),
                   safe_get_var('clouds/openstack_2', 'tenant', context.mist_config['CREDENTIALS']['OPENSTACK_2']['tenant']),))


@step(u'I use my second AWS credentials')
def set_second_aws_creds(context):
    context.execute_steps(u'''
                Then I set the value "%s" to field "API KEY" in the "Edit Credentials" dialog
                Then I set the value "%s" to field "API SECRET" in the "Edit Credentials" dialog
            ''' % (safe_get_var('clouds/aws_2', 'api_key', context.mist_config['CREDENTIALS']['AWS_2']['api_key']),
                   safe_get_var('clouds/aws_2', 'api_secret', context.mist_config['CREDENTIALS']['AWS_2']['api_secret']),))


cloud_creds_dict = {
    "google cloud": set_gce_creds,
    "rackspace": set_rackspace_creds,
    "ibm cloud": set_ibm_clouds_creds,
    "amazon web services": set_aws_creds,
    "linode": set_linode_creds,
    "digital ocean": set_do_creds,
    "docker": set_docker_creds,
    "packet": set_packet_creds,
    "openstack": set_openstack_creds,
    "hostvirtual": set_hostvirtual_creds,
    "vultr": set_vultr_creds,
    "microsoft azure": set_azure_arm_creds,
    "kvm": set_kvm_creds,
    "other server": set_other_server_creds,
    "vmware vsphere": set_vsphere_creds,
    "docker_orchestrator": set_docker_orchestrator_creds,
    "onapp": set_onapp_creds,
    "alibaba cloud": set_aliyun_creds,
    "aws advantis": set_aws_adv_creds,
    "maxihost": set_maxihost_creds,
}


cloud_second_creds_dict = {
    "aws": set_second_aws_creds,
    "openstack": set_second_openstack_creds
}


@step(u'I select the "{provider}" provider')
def select_provider_in_cloud_add_form(context, provider):
    form_element = get_add_form(context, 'cloud')
    form_shadow = expand_shadow_root(context, form_element)
    # if in mist-hs repo and user has not provided mist
    # with a billing card, then a cc-required dialog appears
    add_credit_card_if_needed(context, form_shadow)
    provider_title = provider.lower()
    providers_lists = form_shadow.find_elements_by_tag_name('paper-listbox')
    providers = []
    for provider_type in providers_lists:
        providers += provider_type.find_elements_by_tag_name('paper-item')

    for p in providers:
        if safe_get_element_text(p).lower().strip() == provider_title:
            clicketi_click(context, p)
            return


@step(u'I use my "{provider}" credentials')
def cloud_creds(context, provider):
    provider = provider.strip().lower()
    if provider not in cloud_creds_dict.keys():
        raise Exception("Unknown cloud provider")
    cloud_creds_dict.get(provider)(context)


@step(u'I use my second "{provider}" credentials in cloud edit form')
def cloud_second_creds(context, provider):
    provider = provider.strip().lower()
    if provider not in cloud_second_creds_dict.keys():
        raise Exception("Unknown cloud provider")
    cloud_second_creds_dict.get(provider)(context)


@step(u'I should have {clouds} clouds added')
def check_error_message(context, clouds):
    page_dashboard = get_page_element(context, 'dashboard')
    page_dashboard_shadow = expand_shadow_root(context, page_dashboard)
    cloud_chips = page_dashboard_shadow.find_elements_by_css_selector('cloud-chip')
    if len(cloud_chips) == int(clouds):
        return
    else:
        assert False, "There are %s clouds added, not %s"%(len(cloud_chips), clouds)


def find_cloud(context, cloud_title):
    page_dashboard = get_page_element(context, 'dashboard')
    page_dashboard_shadow = expand_shadow_root(context, page_dashboard)

    end_time = time() + 10
    while time() < end_time:
        cloud_chips = page_dashboard_shadow.find_elements_by_css_selector('cloud-chip')
        if cloud_chips or has_finished_loading(context, 'clouds'):
            break
        sleep(2)

    for cloud in cloud_chips:
        if cloud.is_displayed:
            title = cloud.find_element_by_css_selector('.cloud-title')
            if safe_get_element_text(title).lower().strip() == cloud_title:
                return cloud
    return None


def find_cloud_info(context, cloud_title):
    clouds = context.browser.find_elements_by_tag_name('cloud-info')
    clouds = filter(lambda el: el.is_displayed(), clouds)
    for c in clouds:
        try:
            input_containers = c.find_elements_by_id('labelAndInputContainer')
            for container in input_containers:
                text = safe_get_element_text(container.find_element_by_tag_name('label')).lower().strip()
                if text == 'title':
                    text = container.find_element_by_tag_name('input').\
                            get_attribute('value').lower().strip()
                    if text == cloud_title:
                        return c
        except NoSuchElementException:
            pass
    return None


@step(u'"{cloud}" cloud has been added')
def given_cloud(context, cloud):
    if find_cloud(context, cloud.lower()):
        return True

    context.execute_steps(u'''
        When I click the fab button in the "dashboard" page
        Then I expect the "Cloud" add form to be visible within max 5 seconds
    ''')

    if 'docker_orchestrator' in cloud.lower():
        cloud_type = 'docker'
    elif 'aws advantis' in cloud.lower():
        cloud_type = 'amazon web services'
    else:
        cloud_type = cloud

    context.execute_steps(u'''When I select the "%s" provider''' % cloud_type)

    context.execute_steps('''
        Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
        When I use my "%s" credentials
        And I focus on the button "Add Cloud" in the "cloud" add form
        And I click the button "Add Cloud" in the "cloud" add form
        And I wait for the dashboard to load
        And I scroll the clouds list into view
        Then the "%s" provider should be added within 120 seconds
    ''' % (cloud, cloud))


@step(u'I {action} the cloud page for "{provider}"')
def open_cloud_menu(context, action, provider):
    action = action.lower()
    if action not in ['open', 'close']:
        raise Exception('Unrecognized action')
    if action == 'open':
        cloud = find_cloud(context, provider.lower())
        assert cloud, "Provider %s is not available" % provider
        clicketi_click(context, cloud)
    cloud_info = find_cloud_info(context, provider.lower())
    if action == 'close':
        close_button = cloud_info.find_element_by_id('close-btn')
        clicketi_click(context, close_button)


@step(u'I delete the "{provider}" cloud')
def delete_cloud(context, provider):
    cloud_info = find_cloud_info(context, provider.lower())
    assert cloud_info, "Cloud page has not been found"
    cloud_menu_buttons = cloud_info.find_elements_by_tag_name('paper-button')
    click_button_from_collection(context, 'Delete Cloud', cloud_menu_buttons)


@step(u'the "{cloud}" provider should be added within {seconds} seconds')
def cloud_added(context, cloud, seconds):
    end_time = time() + int(seconds)
    while time() < end_time:
        if find_cloud(context, cloud.lower()):
            return True
        sleep(2)
    assert False, u'%s is not added within %s seconds' % (cloud, seconds)


@step(u'the "{cloud}" cloud should be deleted')
def cloud_deleted(context, cloud):
    if find_cloud(context, cloud.lower()):
        return False


@step(u'the "{cloud}" cloud should be deleted within "{seconds}" seconds')
def cloud_deleted(context, cloud, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        if not find_cloud(context, cloud.lower()):
            return True
        sleep(1)
    assert False, "Cloud has not been deleted after %s seconds" % seconds


@step(u'I ensure "{title}" cloud is enabled')
def ensure_cloud_enabled(context, title):
    cloud = find_cloud(context, title.lower())
    assert cloud, "Cloud %s has not been added" % title
    return 'offline' in cloud.get_attibute('class')


@step(u'I add the key needed for Other Server')
def add_key_for_provider(context):

    context.execute_steps(u'''
        When I visit the Keys page
        When I click the button "+"
        Then I expect the "Key" add form to be visible within max 10 seconds
        When I set the value "KVMKey" to field "Name" in the "key" add form
    ''')

    key = safe_get_var('clouds/other_server', 'key', context.mist_config['CREDENTIALS']['KVM']['key'])
    set_value_to_field(context, key, 'Private Key', 'key', 'add')

    context.execute_steps(u'''
        When I expect for the button "Add" in the "key" add form to be clickable within 9 seconds
        And I focus on the button "Add" in the "key" add form
        And I click the button "Add" in the "key" add form
        Then I expect the "key" page to be visible within max 7 seconds
        And I visit the Home page
        When I visit the Keys page
        Then "KVMKey" key should be present within 15 seconds
        Then I visit the Home page
        When I wait for the dashboard to load
    ''')
