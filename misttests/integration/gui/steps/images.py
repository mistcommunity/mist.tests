from behave import step

from time import time

from .utils import safe_get_element_text, get_page_element
from .utils import expand_shadow_root, get_grid_items


def find_image(image, images_list):
    for check_image in images_list:
        if image in safe_get_element_text(check_image):
            return check_image.find_element_by_css_selector('strong.name')


@step(u'the "{image}" image should be "{state}" within {seconds} seconds')
def assert_starred_unstarred_image(context, image, state, seconds):
    state = state.lower()
    if state not in ['starred', 'unstarred']:
        raise Exception('Unknown type of state')
    images_page = get_page_element(context, 'images')
    images_page_shadow = expand_shadow_root(context, images_page)
    mist_list = images_page_shadow.find_element_by_css_selector('mist-list')
    list_shadow = expand_shadow_root(context, mist_list)
    grid = list_shadow.find_element_by_css_selector('vaadin-grid')
    end_time = time() + int(seconds)
    while time() < end_time:
        starred = get_grid_items(context, grid)[0]['starred']
        if state == 'starred':
            assert starred, "Image is not starred"
        else:
            assert not starred, "Image is starred"
        return
    assert False, 'Image %s is not %s in the list after %s seconds' \
                  % (image, state, seconds)
