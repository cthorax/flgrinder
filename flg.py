
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as sexcept


path_to_chromedriver = 'D:\Python\chromedriver.exe'
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.plugins': 2,
                                                 'profile.managed_default_content_settings.popups': 2,
                                                 'profile.managed_default_content_settings.geolocation': 2,
                                                 'profile.managed_default_content_settings.notifications': 2,
                                                 'profile.managed_default_content_settings.media_stream': 2})


def clean_text(text):
    import unicodedata

    temp_string = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    temp_string = temp_string.lower()
    forbidden = """'".?,!:;"""
    for char in forbidden:
        temp_string = temp_string.replace(char, "")
    return temp_string


def login(browser):
    login_url = "http://www.fallenlondon.com"

    # go to the site, log in
    browser.get(url=login_url)

    input("hit enter when you've logged in, ya goober. ")


def location(browser):
    # figure out where in the loop you are

    location_selector = "#root > div > div > div:nth-child(4) > div.content.container > div > div.col-tertiary > div > div > p.heading.heading--2"
    header_selector = "#main > div.media.media--root > div.media__body > h1"
    location_text = None
    header_text = None

    try:
        location_text = clean_text(browser.find_element_by_css_selector(css_selector=location_selector).text)
    except sexcept.NoSuchElementException:
        header_text = clean_text(browser.find_element_by_css_selector(css_selector=header_selector).text)

    if header_text == "":
        current_step = 'arrive at london'

    if header_text == "":
        current_step = 'go to nadir'

    if header_text == "":
        current_step = 'at nadir'

    if header_text == "":
        current_step = 'leave nadir'

    if header_text == "":
        current_step = 'orphan trade'

    if header_text == "":
        current_step = 'go to labyrinth'

    if header_text == "offering tribute to the court of the wakeful eye" or location_text == "the labyrinth of tigers":
        current_step = 'favor trade'

    if header_text == "":
        current_step = 'depart london'

    if header_text == "":
        current_step = 'zailing to court'

    if header_text == "":
        current_step = 'enigma trade'

    if header_text == "":
        current_step = 'depart court'

    if header_text == "":
        current_step = 'zailing to london'


    return current_step


def get_payment(browser):
    # check if you can get paid sonnnnnn

    return


def check_tally(browser):
    tally_dict = {}
    # update the internal counts of shit, return a dictionary of shit

    return tally_dict


def check_actions(browser):
    # check the current number of actions, if zero wait some amount of time

    actions_selector = "#root > div > div > div:nth-child(4) > div.content.container > div > div.col-secondary > ul.items.items--list.items--currencies > li:nth-child(1) > div.item__desc > div > div > span > div.item__value"
    actions_display = browser.find_element_by_css_selector(css_selector=actions_selector)
    actions, max_actions = actions_display.text.split('/')

    return int(actions)


def travel(browser, target):
    # clicks on the map and then goes where the target is
    travel_selector = "#root > div > div > div:nth-child(4) > div.content.container > div > div.col-tertiary > div > div > button"
    travel_button = browser.find_element_by_css_selector(css_selector=travel_selector)
    travel_button.click()

    if target == "labyrinth":
        map_target = "#main > div:nth-child(1) > span > div > div > div > div:nth-child(12) > div"
    elif target == "docks":
        map_target = "#main > div:nth-child(1) > span > div > div > div > div:nth-child(2) > div"
    else:
        assert False, "you probably need to add a case for '{target}'".format(target=target)

    map_button = browser.find_element_by_css_selector(css_selector=map_target).click()
    sleep(1)


def favor_trade(browser):
    location_button(browser=browser, target_title="offering tribute to the court of the wakeful eye")
    success = True
    while success:
        success = storylet_button(browser=browser, target_title="offer a winsome dispossessed orphan")
        if success:
            next_button(browser=browser)


def storylet_button(browser, target_title):
    button_selector = "#main > div:nth-child(2) > div:nth-child({position}) > div > div.media__body.branch__body > div.buttons.storylet__buttons > a"
    title_selector = "#main > div:nth-child(2) > div:nth-child({position}) > div > div.media__body.branch__body > div:nth-child(1) > h2"
    for position in range(1, 99):
        try:
            title = clean_text(browser.find_element_by_css_selector(css_selector=title_selector.format(position=position)).text)
        except sexcept.NoSuchElementException:
            result = False
            break

        if title == target_title:
            button = browser.find_element_by_css_selector(css_selector=button_selector.format(position=position))
            disable_text = button.get_attribute('outerHTML')
            disabled = 'disabled=""' in disable_text
            if disabled:
                result = False
            else:
                button.click()
                result = True

    return result


def location_button(browser, target_title):
    title_selector = "#main > div:nth-child(3) > div:nth-child({position}) > div > div.storylet__body > h2"
    button_selector = "#main > div:nth-child(3) > div:nth-child({position}) > div > div.storylet__body > div > a"
    for position in range(1, 99):
        try:
            title = browser.find_element_by_css_selector(css_selector=title_selector.format(position=position)).text
        except sexcept.NoSuchElementException:
            break

        if title == target_title:
            button = browser.find_element_by_css_selector(css_selector=button_selector.format(position=position))
            button.click()


def next_button(browser):
    button_selector = "#main > div > div.buttons.buttons--storylet-exit-options > a"
    button = browser.find_element_by_css_selector(css_selector=button_selector)
    button.click()
    sleep(1)


def draw(browser):
    deck_selector = "#main > div.cards > div.deck-container > div.deck"
    deck = browser.find_element_by_css_selector(css_selector=deck_selector)
    deck.click()
    sleep(1)


def check_card(browser, hand_size=4):
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card_dict = {}
    for pos in range(stop=hand_size, start=1):     # +1?
        card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=pos))
        card_title = clean_text(card.get_attribute('innerHTML'))       # outerHTML?
        card_dict[card_title] = pos
    return card_dict


def pick_card(browser, position):
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=position))
    card.click()
    sleep(1)


def main():
    browser = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    login(browser)
    actions = check_actions(browser)
    current_step = location(browser)
    tally_dict = check_tally(browser)

    while actions > 0:
        if current_step == 'arrive at london':
            get_payment(browser)
            tally_dict = check_tally(browser)

        if current_step == 'go to nadir':
            pass

        if current_step == 'at nadir':
            pass

        if current_step == 'leave nadir':
            pass

        if current_step == 'orphan trade':
            pass

        if current_step == 'go to labyrinth':
            pass

        if current_step == 'favor trade':
            favor_trade(browser=browser)
            current_step = 'depart london'

        if current_step == 'depart london':
            travel(browser, 'docks')
            location_button(browser=browser, target_title="Put to Zee!")
            storylet_button(browser=browser, target_title="Lay in supplies and sail")
            next_button(browser=browser)
            next_button(browser=browser)
            current_step = 'zailing to court'

        if current_step == 'zailing to court':
            end_progress = 0
            trouble_progress = 0

            draw(browser)
            current_cards = check_card(browser)

            while end_progress < 55:
                if 'a wily zailor' in current_cards:
                    pick_card(browser, position=current_cards['a wily zailor'])
                    next_button(browser)
                    draw(browser)



        if current_step == 'enigma trade':
            pass

        if current_step == 'depart court':
            pass

        if current_step == 'zailing to london':
            pass

if __name__ == '__main__':
    main()