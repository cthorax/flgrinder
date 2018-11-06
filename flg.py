
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
    space = """-_"""
    for char in space:
        temp_string = temp_string.replace(char, " ")
    return temp_string


def login(browser):
    login_url = "http://www.fallenlondon.com"

    # go to the site, log in
    browser.get(url=login_url)

    input("hit enter when you've logged in, ya goober. ")


def location(browser, tally_dict):
    """figure out where in the loop you are

    :param browser: a selenium driver instance
    :return:
    """

    location_selector = "#root > div > div > div:nth-child(4) > div.content.container > div > div.col-tertiary > div > div > p.heading.heading--2"
    perhaps_selector = "#main > div.buttons.buttons--left.buttons--storylet-exit-options > a"
    location_text = None
    
    try:
        perhaps_button = browser.find_element_by_css_selector(css_selector=perhaps_selector)
        perhaps_button.click()
        sleep(1)
        location_text = clean_text(browser.find_element_by_css_selector(css_selector=location_selector).text)
        
    except sexcept.NoSuchElementException:
        location_text = clean_text(browser.find_element_by_css_selector(css_selector=location_selector).text)

    if location_text == "wolfstack docks":
        current_step = 'arrive at london'

    elif location_text == "":
        current_step = 'go to nadir'

    elif location_text == "":
        current_step = 'at nadir'

    elif location_text == "":
        current_step = 'leave nadir'

    elif location_text == "":
        current_step = 'orphan trade'

    elif location_text == "":
        current_step = 'go to labyrinth'

    elif location_text == "the labyrinth of tigers":
        current_step = 'favor trade'

    elif location_text == "":
        current_step = 'depart london'

    elif location_text == "the broad unterzee":
        if tally_dict["searing enigma"] > 0:
            current_step = 'zailing to london'
        else:
            current_step = 'zailing to court'

    elif location_text == 'the court of the wakeful eye':
        current_step = 'enigma trade'

    elif location_text == "":
        current_step = 'depart court'

    return current_step


def check_tally(browser):
    """update the internal counts of shit, return a dictionary of shit

    :param browser: selenium driver instance
    :return:
    """

    tally_dict = {
        "tribute": 0,
        "irrigo": 0,
        "approaching journeys end": 0,
        "troubled waters": 0,
        "dramatic tension": 0,
        "payment": 0,
        "orphan": 0,
        "rostygold": 0,
        "searing enigma": 0,
        "diary of the dead": 0,
        "fecund amber": 0,
        "fluke core": 0,
        "sudden insight": 0,
        "hard earned lesson": 0,
        "confident smile": 0,
        "hastily scrawled warning note": 0,
        "journal of infamy": 0,
        "cryptic clue": 0,
        "professional perk": 0,
        "an earnest of payment": 0
    }

    myself_button = browser.find_element_by_css_selector(css_selector="#root > div > div > div:nth-child(4) > div.content.container > div > div.col-primary > nav > ul > li:nth-child(3) > a")
    myself_button.click()
    sleep(1)

    quality_elements = browser.find_elements_by_class_name(name="item__desc")
    for quality in quality_elements:
        myself_item = clean_text(quality.text)

        if "\n" in myself_item:
            if "tribute " in myself_item and tally_dict["tribute"] == 0:
                quantity = int(myself_item.split("\n")[0][8:])
                tally_dict["tribute"] = quantity
            elif "irrigo " in myself_item and tally_dict["irrigo"] == 0:
                quantity = int(myself_item.split("\n")[0][8:])
                tally_dict["irrigo"]=  quantity
            elif "dramatic tension " in myself_item and tally_dict["dramatic tension"] == 0:
                quantity = int(myself_item.split("\n")[0].split(" - ")[0][25:])
                tally_dict["dramatic tension"] = quantity
            elif "approaching journeys end " in myself_item and tally_dict["approaching journeys end"] == 0:
                quantity = int(myself_item.split("\n")[0].split(" - ")[0][25:])
                tally_dict["approaching journeys end"] = quantity
            elif "troubled waters " in myself_item and tally_dict["troubled waters"] == 0:
                quantity = int(myself_item.split("\n")[0].split(" - ")[0][16:])
                tally_dict["troubled waters"] = quantity

    possessions_button = browser.find_element_by_css_selector(css_selector="#root > div > div > div:nth-child(4) > div.content.container > div > div.col-primary > nav > ul > li:nth-child(4) > a")
    possessions_button.click()
    sleep(1)

    item_elements = browser.find_elements_by_class_name(name="icon--inventory")
    for item in item_elements:
        not_used, item_name, also_not_used, quantity = item.get_attribute('innerHTML').split("><")
        item_name = clean_text(item_name)[8:].split("aria-label")[0][:-1]
        quantity = int(quantity.split(">")[1].split("<")[0])

        tally_dict = update_tally(tally_dict, item_name, quantity)

    story_button = browser.find_element_by_css_selector(css_selector="#root > div > div > div:nth-child(4) > div.content.container > div > div.col-primary > nav > ul > li:nth-child(1) > a")
    story_button.click()

    return tally_dict


def update_tally(tally_dict, item_name, quantity):
    item_name = clean_text(item_name)
    if item_name in tally_dict.keys():
        tally_dict[item_name] = quantity

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
    sleep(1)
    button_selector = "#main > div:nth-child(2) > div:nth-child({position}) > div > div.media__body.branch__body > div.buttons.storylet__buttons > a"
    title_selector = "#main > div:nth-child(2) > div:nth-child({position}) > div > div.media__body.branch__body > div:nth-child(1) > h2"
    for position in range(1, 99):
        try:
            title = clean_text(browser.find_element_by_css_selector(css_selector=title_selector.format(position=position)).text)
        except (sexcept.NoSuchElementException, sexcept.StaleElementReferenceException):
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
    sleep(1)
    title_selector = "#main > div:nth-child(3) > div:nth-child({position}) > div > div.storylet__body > h2"
    button_selector = "#main > div:nth-child(3) > div:nth-child({position}) > div > div.storylet__body > div > a"
    for position in range(1, 99):
        try:
            title = clean_text(browser.find_element_by_css_selector(css_selector=title_selector.format(position=position)).text)
        except sexcept.NoSuchElementException:
            break

        if title == target_title:
            button = browser.find_element_by_css_selector(css_selector=button_selector.format(position=position))
            button.click()


def next_button(browser):
    sleep(1)
    button_selector = "#main > div > div.buttons.buttons--storylet-exit-options > a"
    alt_button_selector = "#main > div > div.buttons.buttons--storylet-exit-options > a:nth-child(1)"
    try:
        button = browser.find_element_by_css_selector(css_selector=button_selector)
    except sexcept.NoSuchElementException:
        try:
            button = browser.find_element_by_css_selector(css_selector=alt_button_selector)
        except sexcept.NoSuchElementException:
            raise

    button.click()
    sleep(1)


def draw(browser):
    deck_selector = "#main > div.cards > div.deck-container > div.deck"
    deck = browser.find_element_by_css_selector(css_selector=deck_selector)
    deck.click()
    sleep(1)


def check_card(browser, hand_size=3):
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card_dict = {}
    for pos in range(1, hand_size+1):     # +1?
        card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=pos))
        card_title = clean_text(card.get_attribute('innerHTML')).split(" aria-label")[0][9:]
        card_dict[card_title] = pos
    return card_dict


def pick_card(browser, position):
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=position))
    card.click()
    sleep(1)


def zailing(browser, tally_dict):
    draw(browser)
    current_cards = check_card(browser)

    if 'a wily zailor' in current_cards:
        pick_card(browser, position=current_cards['a wily zailor'])
        next_button(browser)
        tally_dict = read_results(browser=browser, tally_dict=tally_dict)
        draw(browser)
    else:
        location_button(browser=browser, target_title='steam prudently')
        storylet_button(browser=browser, target_title='a cautious captain')
        tally_dict = read_results(browser=browser, tally_dict=tally_dict)
        next_button(browser)

    return tally_dict


def read_results(browser, tally_dict):
    sleep(1)
    results_list = browser.find_elements_by_class_name(name="quality-update__body")
    for result in results_list:
        if "new total" in result.text:  # item updates
            item_name, quantity = clean_text(result.text).split(" x ")[1].split(" (new total ")
            quantity = int(quantity[:-1])
            tally_dict = update_tally(tally_dict, item_name, quantity)

        elif "shows your progress" in result.text:
            item_name, quantity = result.text.split(" has increased to ")
            quantity = int(quantity.split(" - ")[0])
            tally_dict = update_tally(tally_dict, item_name, quantity)

        elif "gained a new quality" in result.text:
            item_name, quantity = result.text.split(" has increased to ")
            quantity = int(quantity.split(" - ")[0])
            tally_dict = update_tally(tally_dict, item_name, quantity)

        elif "has increased to" in result.text:
            item_name, quantity = result.text.split(" has increased to ")
            quantity = int(quantity.split(" - ")[0])
            tally_dict = update_tally(tally_dict, item_name, quantity)

    return tally_dict


def main():
    browser = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    login(browser)
    tally_dict = check_tally(browser)
    current_step = location(browser, tally_dict)

    while True:
        actions = check_actions(browser)
        if actions >= 5:
            if current_step == 'london':
                tally_dict = check_tally(browser)
                if tally_dict['an earnest of payment'] > 0:
                    current_step = 'payment'
                elif tally_dict['irrigo'] == 0:
                    current_step = 'go to nadir'
                elif tally_dict['searing enigma'] > 0:
                    current_step = 'orphan trade'
                elif tally_dict["winsome dispossessed orphan"] > 0:
                    current_step = 'go to labyrinth'

            elif current_step == 'payment'
                travel(browser, target='your lodgings')
                location_button(browser, target_title="a professional reward")
                storylet_button(browser, target_title="the wage of a crooked cross")
                next_button(browser)
                current_step = 'london'

            elif current_step == 'go to nadir':
                travel(browser, target='the forgotten quarter')
                location_button(browser, target_title="return to the cave of the nadir")
                storylet_button(browser, target_title='make the journey')
                current_step = 'at nadir'


            elif current_step == 'at nadir':
                if tally_dict['irrigo'] >= 6:
                    current_step = 'leave nadir'
                else:
                    draw(browser)
                    hand_dict = check_card(browser, hand_size=4)
                    if tally_dict['nodule of fecund amber'] >= 5:
                        fluke_trade_flag = 'why'
                    elif tally_dict["diary of the dead"] >= 5:
                        fluke_trade_flag = 'what'
                    else:
                        fluke_trade_flag = None

                    if tally_dict['sudden insight'] >= 3:
                        battles_flag = "wisdom"
                    elif tally_dict['hard earned lesson'] >= 3:
                        battles_flag = "pleasure"
                    elif tally_dict['confident smile'] >= 3:
                        battles_flag = "truth"
                    elif tally_dict['hastily scrawled note'] >= 3:
                        battles_flag = "experience"
                    else:
                        battles_flag = None

                    if tally_dict["journal of infamy"] > 0:
                        losing_flag = 'dubious_attribution'
                    elif tally_dict['cryptic clue'] > 0:
                        losing_flag = 'just one'
                    else:
                        losing_flag = None


                    if "do you recall how they came to that place" in hand_dict.keys() and fluke_trade_flag:
                        pick_card(browser, position=hand_dict["do you recall how they came to that place"])
                        storylet_button(browser, target_title=fluke_trade_flag)
                        next_button(browser)

                    elif "the end of battles" in hand_dict.keys() and battles_flag:
                        pick_card(browser, position=hand_dict["the end of battles"])
                        storylet_button(browser, target_title=battles_flag)
                        next_button(browser)
                    elif "losing" in hand_dict.keys() and losing_flag:
                        pick_card(browser, position=hand_dict["losing"])
                        storylet_button(browser, target_title=losing_flag)
                        next_button(browser)
                    elif "a card game" in hand_dict.keys():
                        pick_card(browser, position=hand_dict["a card game"])
                        storylet_button(browser, target_title="deal yourself in")
                        next_button(browser)
                    else:
                        current_step = 'leave nadir'

            elif current_step == 'leave nadir':
                pass

            elif current_step == 'orphan trade':
                bazaar_button = browser.find_element_by_css_selector(css_selector="#root > div > div > div:nth-child(4) > div.content.container > div > div.col-primary > nav > ul > li:nth-child(5) > a")
                bazaar_button.click()

                search_bar = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > input")
                search_bar.clear()
                search_bar.send_keys("searing enigma")

                sell_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > li > div.js-item-controls.item__controls > a")
                sell_button.click()

                result = True
                while result == True
                    plus_ten_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__controls > button:nth-child(5)")
                    disable_text = plus_ten_button.get_attribute('outerHTML')
                    disabled = 'disabled=""' in disable_text

                    if disabled:
                        result = False
                    else:
                        plus_ten_button.click()
                        result = True

                final_sale_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__submit-button-container > button")
                final_sale_button.click()

                close_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div.exchange-ui__close-button--md-up > span > span.fa.fa-inverse.fa-stack-1x.fa-close")
                close_button.click()

                redemptions_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.nav.nav--stacked.nav--stacked--1-of-4.nav--stacked--roman > div > nav > ol > li:nth-child(10) > a")
                redemptions_button.click()

                search_bar.clear()
                search_bar.send_keys("winsome")

                buy_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > li > div.js-item-controls.item__controls > a")
                buy_button.click()

                result = True
                while result == True
                    plus_ten_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__controls > button:nth-child(5)")
                    disable_text = plus_ten_button.get_attribute('outerHTML')
                    disabled = 'disabled=""' in disable_text

                    if disabled:
                        result = False
                    else:
                        plus_ten_button.click()
                        result = True

                sleep(1)
                final_sale_button.click()
                sleep(1)
                close_button.click()

                current_step = 'go to labyrinth'

            elif current_step == 'go to labyrinth':
                travel(browser, target='labyrinth of tigers')
                current_step = 'favor trade'

            elif current_step == 'favor trade':
                favor_trade(browser=browser)
                current_step = 'depart london'

            elif current_step == 'depart london':
                travel(browser, 'docks')
                location_button(browser=browser, target_title="put to zee")
                storylet_button(browser=browser, target_title="lay in supplies and sail")
                next_button(browser=browser)
                next_button(browser=browser)
                current_step = 'zailing to court'

            elif current_step == 'zailing to court':
                if tally_dict['journeys end'] < 10:
                    zailing(browser, tally_dict)
                else:
                    location_button(browser=browser, target_title='across the southern archipelago')
                    storylet_button(browser=browser, target_title="the court of the wakeful eye")

            elif current_step == 'enigma trade':
                if tally_dict['tribute'] >= 20:
                    storylet_button(browser, 'join the minister of enigmas for teatime')
                    tally_dict = read_results(browser, tally_dict)
                    next_button(browser)
                else:
                    current_step = 'depart court'

            elif current_step == 'depart court':
                location_button(browser=browser, target_title="set to zee")
                next_button(browser)

                current_step = "zailing to london"

            elif current_step == 'zailing to london':
                if tally_dict['approaching journeys end'] < 10:
                    zailing(browser, tally_dict)
                else:
                    location_button(browser=browser, target_title='across the southern archipelago')
                    storylet_button(browser=browser, target_title="london")


        else:
            print("not enough actions, sleeping for 10 minutes.")
            sleep(600)
            browser.refresh()
            sleep(10)

if __name__ == '__main__':
    main()