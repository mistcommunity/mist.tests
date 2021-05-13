from behave import step

from selenium.webdriver.common.keys import Keys

from .forms import get_edit_form

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from .utils import safe_get_element_text, get_page_element, expand_shadow_root
from .utils import clear_input_and_send_keys

from time import sleep


def add_new_rule(context, operator, rtype='all', raction='all', rid='',
                 rtags='', constraints=''):
    operator = operator.lower()
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    new_rule = form_shadow.find_element_by_css_selector(
        '#rules > rbac-rule-item:nth-last-child(2)')
    new_rule_shadow = expand_shadow_root(context, new_rule)

    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')

    if operator == 'allow':
        toggle_button = new_rule_shadow.find_element_by_css_selector('paper-toggle-button')
        clicketi_click(context, toggle_button)

    if rtype != 'all':
        rtype_drop = new_rule_shadow.\
            find_element_by_css_selector('span.resource').\
            find_element_by_css_selector('paper-dropdown-menu')
        clicketi_click(context, rtype_drop)
        sleep(1)
        click_button_from_collection(context, rtype,
                                     rtype_drop.find_elements_by_css_selector('paper-item'))

    if raction != 'all':
        raction_drop = new_rule_shadow.\
            find_element_by_css_selector('span.action').\
            find_element_by_css_selector('paper-dropdown-menu')
        clicketi_click(context, raction_drop)
        sleep(3)
        click_button_from_collection(context, raction,
                                     raction_drop.find_elements_by_css_selector('paper-item'))
    rule_identifier = new_rule_shadow.find_element_by_css_selector('rbac-rule-identifier')
    rule_identifier_shadow = expand_shadow_root(context, rule_identifier)

    rcondition = rule_identifier_shadow.find_element_by_css_selector('paper-dropdown-menu')

    if rid:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where id',
                                     rcondition.find_elements_by_css_selector('paper-item'))
        sleep(1)
        rid_drop = rule_identifier_shadow. \
            find_elements_by_css_selector('paper-dropdown-menu')[-1]
        clicketi_click(context, rid_drop)
        sleep(1)
        click_button_from_collection(context, rid,
                                     rid_drop.find_elements_by_css_selector('paper-item'))

    if rtags:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where tags',
                                     rcondition.find_elements_by_css_selector('paper-item'))
        sleep(3)
        edit_icon = rule_identifier_shadow. \
            find_element_by_css_selector('.edit')
        clicketi_click(context, edit_icon)
        clicketi_click(context, edit_icon)
        paper_input = rule_identifier_shadow.find_element_by_css_selector('paper-input#inputField')
        paper_input_shadow = expand_shadow_root(context, paper_input)
        input_element = paper_input_shadow.find_element_by_css_selector('input')
        input_element.send_keys(rtags)
    if constraints:            
        constraints_button = new_rule_shadow.find_element_by_css_selector('span.constraints').\
            find_element_by_css_selector('rbac-rule-constraints')
        clicketi_click(context, constraints_button)
        sleep(3)
        overlay = context.browser.find_element_by_css_selector('#overlay')
        overlay_shadow = expand_shadow_root(context, overlay)
        content_div = overlay_shadow.find_element_by_css_selector('#content')
        content_div_shadow = expand_shadow_root(context, content_div)
        mist_form = content_div_shadow.find_element_by_tag_name('mist-form')
        mist_form_shadow = expand_shadow_root(context, mist_form)
        if constraints == "kevin\'s":
            size_constraint_div = mist_form_shadow.find_element_by_id('size_constraint_container')
            size_constraint_toggle = size_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, size_constraint_toggle)
            sleep(1)
            primary_disk_constraint_div = size_constraint_div.find_element_by_id('primary_disk_constraint')
            primary_disk_checkbox = primary_disk_constraint_div.find_element_by_tag_name('paper-checkbox')
            clicketi_click(context, primary_disk_checkbox)
            sleep(1)
            swap_disk_constraint_div = size_constraint_div.find_element_by_id('swap_disk_constraint')
            swap_disk_checkbox = swap_disk_constraint_div.find_element_by_tag_name('paper-checkbox')
            clicketi_click(context, swap_disk_checkbox)
            sleep(1)
            field_constraint_div = mist_form_shadow.find_element_by_id('field_constraint_container')
            field_constraint_toggle = field_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, field_constraint_toggle)
            sleep(1)
            field_constraint_input = field_constraint_div.find_element_by_css_selector('.mist-form-input')
            field_constraint_shadow = expand_shadow_root(context, field_constraint_input)
            field_constraint_add_button = field_constraint_shadow.find_element_by_tag_name('paper-button')
            clicketi_click(context, field_constraint_add_button)
            sleep(1)
            field_name_paper_input = field_constraint_shadow.find_element_by_tag_name('paper-input')
            field_name_paper_input_shadow = expand_shadow_root(context, field_name_paper_input)
            field_name_input = field_name_paper_input_shadow.find_element_by_tag_name('iron-input')
            sleep(1)
            buttons_div = mist_form_shadow.find_element_by_css_selector('.buttons')
            save_button = buttons_div.find_element_by_css_selector('.submit-btn')
            clicketi_click(context, save_button)
            sleep(3)


@step('I add the rule "{operator}" "{rtype}" "{raction}" where id = "{rid}"')
def add_new_rule_with_rid(context, operator, rtype, raction, rid):
    add_new_rule(context, operator, rtype, raction, rid)

@step(u'I add the rule always "{operator}" "{rtype}" "{raction}" with "{constr}" constraints')
def add_new_rule_with_constraints(context, operator, rtype, raction, constr):
    add_new_rule(context, operator, rtype, raction, constraints=constr)

@step('I add the rule "{operator}" "{rtype}" "{raction}" where tags = '
      '"{rtags}"')
def add_new_rule_with_rtags(context, operator, rtype, raction, rtags):
    add_new_rule(context, operator, rtype, raction, rtags=rtags)


@step('I add the rule always "{operator}" "{rtype}" "{raction}"')
def add_new_rule_always(context, operator, rtype, raction):
    add_new_rule(context, operator, rtype, raction)


@step('I remove the rule with index "{index}"')
def delete_rule(context, index):
    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    rules = [expand_shadow_root(context, rule) for rule in form_shadow.find_elements_by_css_selector('rbac-rule-item')]
    for rule in rules:
        index_class = rule.find_element_by_css_selector('.index')
        rule_index = safe_get_element_text(index_class)
        rule_index = rule_index.replace('.','')
        if rule_index == index:
            delete_btn = rule.find_element_by_css_selector('.delete')
            icon = delete_btn.find_element_by_css_selector('iron-icon')
            clicketi_click(context, icon)
            return
    assert False, "There is no rule with index %s" % index


def check_rule_exists(context, rule_number, operator, rtype, raction, rid, rtags):
    rule_number = int(rule_number)
    operator = operator.lower()
    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    rules = [expand_shadow_root(context, rule) for rule in form_shadow.find_elements_by_css_selector('rbac-rule-item')]
    rule = rules[rule_number]
    rule_operator = safe_get_element_text(
        rule.find_element_by_css_selector('span.operator')).strip().lower()
    assert operator == rule_operator, "Operator is not %s" % operator

    rule_resource = rule.find_element_by_css_selector('span.resource').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert rtype == rule_resource, "Resource type is not %s" % rtype

    rule_action = rule.find_element_by_css_selector('span.action').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert raction == rule_action, "Rule action is not %s" % raction

    rcondition = rule.find_element_by_css_selector('span.identifier').\
        find_elements_by_css_selector('input#input')[0].get_attribute('value').\
        strip().lower()

    if not rid and not rtags:
        assert rcondition == 'always', "Rule condition is not always"

    if rid:
        assert rcondition == 'where id', "Rule condition is not always"
        rule_id = rule.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[1].\
            get_attribute('value').strip().lower()
        assert rid == rule_id, "Rule id is not %s" % rid

    if rtags:
        assert rcondition == 'where tags', "Rule condition is not always"
        rule_tags = rule.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[2].\
            get_attribute('value').strip().lower()
        assert rtags == rule_tags, "Rule tag is not %s" % rtags


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where tags'
      ' = "{rtags}"')
def check_rule_with_rtags(context, rule_number, operator, rtype, raction, rtags):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', rtags)


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where id = '
      '"{rid}"')
def check_rule_with_rid(context, rule_number, operator, rtype, raction, rid):
    check_rule_exists(context, rule_number, operator, rtype, raction, rid, '')


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" always')
def check_rule_always(context, rule_number, operator, rtype, raction):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', '')
