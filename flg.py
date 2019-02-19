
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
    space = """-_–()"""
    for char in space:
        temp_string = temp_string.replace(char, " ")
    return temp_string


def login():
    login_url = "http://www.fallenlondon.com"

    # go to the site, log in
    browser.get(url=login_url)

    input("hit enter when you've logged in, ya goober. ")


def get_location():   #todo: change from selector to class
    location_selector = "#root > div > div > div:nth-child(4) > div.content.container > div > div.col-tertiary > div > div > p.heading.heading--2"
    alt_location_selector = "#root > div > div > div:nth-child(5) > div.content.container > div > div.col-tertiary > div > div > p.heading.heading--2"
    perhaps_selector = "#main > div.buttons.buttons--left.buttons--storylet-exit-options > button"
    headers_selector = "#main > div.media.media--root > div.media__body > h1"
    location_text = None
    
    try:
        perhaps_button = browser.find_element_by_css_selector(css_selector=perhaps_selector)
        perhaps_button.click()
        location_text = clean_text(browser.find_element_by_css_selector(css_selector=location_selector).text)
        
    except sexcept.NoSuchElementException:
        try:
            location_text = clean_text(browser.find_element_by_class_name("heading--2").text)
        except sexcept.NoSuchElementException:
            try:
                location_text = clean_text(browser.find_element_by_css_selector(css_selector=alt_location_selector).text)
            except sexcept.NoSuchElementException:
                location_text = clean_text(browser.find_element_by_css_selector(css_selector=headers_selector).text)

    return location_text


def location():
    locations_dict = {
        "wolfstack docks": 'london',
        "your lodgings":  'london',
        "the forgotten quarter": 'go to nadir',
        "cave of the nadir": 'at nadir',
        "the labyrinth of tigers": 'favor trade",
        "the broad unterzee": 'zailing',
        "the court of the wakeful eye": 'enigma trade',
        "court of the wakeful eye": 'enigma trade',
        "winking isle": 'winking isle',
        "the well": 'winking isle',
        "the empress court": 'at court'
    }
    location_text = get_location()
    return locations_dict.get(location_text, 'unknown')


def init_tally():
    global tally_dict
    tally_dict = {
        "tribute": 0,
        "irrigo": 0,
        "fleeting recollections": 0,
        "approaching journeys end": 0,
        "troubled waters": 0,
        "winsome dispossessed orphan": 0,
        "piece of rostygold": 0,
        "searing enigma": 0,
        "diary of the dead": 0,
        "nodule of fecund amber": 0,
        "fluke core": 0,
        "sudden insight": 0,
        "hard earned lesson": 0,
        "confident smile": 0,
        "hastily scrawled warning note": 0,
        "journal of infamy": 0,
        "cryptic clue": 0,
        "professional perk": 0,
        "an earnest of payment": 0,
        "fasting and meditating to a foolish end": 0,
        "seeking mr eatens name": 0,
        "making waves": 0,
        "notability": 0
    }

    browser.get("https://www.fallenlondon.com/myself")

    quality_elements = browser.find_elements_by_class_name(name="quality-item__name")
    for quality in quality_elements:
        myself_item = quality.text

        if "Tribute " in myself_item and tally_dict["tribute"] == 0:
            quantity = int(myself_item.split("\n")[0][8:])
            tally_dict["tribute"] = quantity
        elif "Irrigo " in myself_item and tally_dict["irrigo"] == 0:
            quantity = int(myself_item.split("\n")[0][6:])
            tally_dict["irrigo"]=  quantity
        elif "Fleeting Recollections" in myself_item and tally_dict["fleeting recollections"] == 0:
            tally_dict["fleeting recollections"] = 1
        elif "Approaching Journey's End " in myself_item and tally_dict["approaching journeys end"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][25:])
            tally_dict["approaching journeys end"] = quantity
        elif "Troubled Waters " in myself_item and tally_dict["troubled waters"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][16:])
            tally_dict["troubled waters"] = quantity
        elif "Fasting and Meditating to a Foolish End " in myself_item and tally_dict["fasting and meditating to a foolish end"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][40:])
            tally_dict["fasting and meditating to a foolish end"] = quantity
        elif "Seeking Mr Eaten's Name " in myself_item and tally_dict["seeking mr eatens name"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][24:])
            tally_dict["seeking mr eatens name"] = quantity
        elif "Making Waves " in myself_item and tally_dict["making waves"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][13:])
            tally_dict["making waves"] = quantity
        elif "Notability " in myself_item and tally_dict["notability"] == 0:
            quantity = int(myself_item.split("\n")[0].split(" - ")[0][11:])
            tally_dict["notability"] = quantity

    browser.get("https://www.fallenlondon.com/possessions")

    equipment_elements = browser.find_elements_by_class_name(name="icon--available-item")
    for item in equipment_elements:
        _, item_name, _, quantity = item.get_attribute('innerHTML').split("><")
        item_name = clean_text(item_name[8:].split("aria-label")[0][:-1])
        quantity = int(quantity.split(">")[1].split("<")[0])

        tally_dict = update_tally(tally_dict, item_name, quantity)

    item_elements = browser.find_elements_by_class_name(name="icon--inventory")
    for item in item_elements:
        _, item_name, _, quantity = item.get_attribute('innerHTML').split("><")
        item_name = clean_text(item_name[8:].split("aria-label")[0][:-1])
        quantity = int(quantity.split(">")[1].split("<")[0])

        tally_dict = update_tally(tally_dict, item_name, quantity)

    browser.get("https://www.fallenlondon.com/")


def update_tally(item_name, quantity):
    item_name = clean_text(item_name)
    if item_name in tally_dict.keys():
        tally_dict[item_name] = quantity


def check_actions():
    # check the current number of actions
    try:
        actions_display = browser.find_element_by_class_name("item__desc")
        actions = actions_display.text.split('\n')[1].split('/')[0]
    except (sexcept.NoSuchElementException, IndexError):
        actions = 0
        print('actions machine broke. understandable have a good day. ', end='')

    return int(actions)


def travel(target, safe=True):
    # clicks on the map and then goes where the target is
    location = get_location()
    if location != target:
        travel_button = browser.find_element_by_class_name("travel-button--infobar")
        travel_button.click()

        area_buttons = browser.find_elements_by_class_name("map__area")
        for area_button in area_buttons:
            area_name = clean_text(area_button.find_element_by_class_name("map__image").get_attribute('outerHTML')[10:].split('"')[0])
            if target == area_name:
                area_button.click()
                result = True

        result = False

if safe:
    assert result
return result

def storylet_button(target_title, safe=True):
    result = None
    storylets = browser.find_elements_by_class_name('branch__body')
    for storylet in storylets:
        title = clean_text(storylet.find_element_by_class_name('branch__title').text)
        if title == target_title:
            try:
                go_button = storylet.find_element_by_class_name('button--go')
                disabled = 'disabled=""' in go_button.get_attribute('outerHTML')

                if disabled:
                    result = False
                else:
                    go_button.click()
                    result = True
                    break
            except sexcept.StaleElementReferenceException:
                print('oh no!')

    if safe:
        try:
            assert result
        except AssertionError:
            print('you did a bad job!')
            raise
    return result


def location_button(target_title, safe=True):
    result = None
    storylets = browser.find_elements_by_class_name('storylet__body')
    for storylet in storylets:
        title = clean_text(storylet.find_element_by_class_name('storylet__heading').text)
        if title == target_title:
            go_button = storylet.find_element_by_class_name('button--go')
            disabled = 'disabled=""' in go_button.get_attribute('outerHTML')

            if disabled:
                result = False
            else:
                go_button.click()
                result = True
                break

    if safe:
        assert result
    return result


def next_button():
    button = browser.find_element_by_class_name('button--primary')
    button.click()


def draw():
    deck = browser.find_element_by_class_name('deck')
    deck.click()


def check_card(hand_size=3):    # todo: fix check_card
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card_dict = {}
    for pos in range(1, hand_size+1):     # +1?
        card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=pos))
        card_title = clean_text(card.get_attribute('innerHTML').split(" aria-label")[0][9:])
        card_dict[card_title] = pos
    return card_dict


def pick_card(position):
    card_selector = "#main > div.cards > div.hand > div:nth-child({position}) > div > div > div"
    card = browser.find_element_by_css_selector(css_selector=card_selector.format(position=position))
    card.click()


def zailing():
    draw()
    current_cards = check_card()    # todo: check_card is broken

    if 'a wily zailor' in current_cards:
        pick_card(position=current_cards['a wily zailor'])
        storylet_button(target_title='steam straight through the beechey currents ')
        read_results()
        next_button()
        draw()
    else:
        location_button(target_title='steam prudently')
        storylet_button(target_title='a cautious captain')
        read_results()
        next_button()


def read_results():
    results_list = browser.find_elements_by_class_name(name="quality-update__body")
    for result in results_list:
        if "new total" in result.text:  # item updates to any number
            item_name, quantity = result.text.split(" x ")[1].split(" (new total ")
            item_name = clean_text(item_name)
            try:
                quantity = int(quantity.split(" - ")[0])
            except ValueError:
                quantity = quantity.split(" - ")[0]
                quantity = clean_text(quantity).strip()
                quantity = int(quantity)

        elif "shows your progress" in result.text:
            item_name, not_used, quantity = result.text.split("\n")
            quantity = int(quantity)
            item_name = clean_text(item_name.split(" shows your progress in the venture")[0])

        elif "gained a new quality" in result.text:
            item_name, quantity = result.text[29:].split(" at ")
            item_name = clean_text(item_name)
            quantity = int(quantity.split(" - ")[0])

        elif "has increased to" in result.text:
            item_name, quantity = result.text.split(" has increased to ")
            item_name = clean_text(item_name)
            try:
                quantity = int(quantity.split(" - ")[0])
            except ValueError:
                quantity = int(quantity.split("!")[0])

        elif "An occurrence" in result.text:  # quality updates to any number
            item_name, quantity = result.text[21:].split("' Quality is now ")
            item_name = clean_text(item_name)
            quantity = int(quantity.split(' - ')[0])

        elif " Quality has gone!" in result.text:  # quality updates to zero
            item_name = result.text[6:-19]
            item_name = clean_text(item_name)
            quantity = 0

        update_tally(item_name, quantity)


def notability_farm():
    target = 4*tally_dict['notability'] + 7
    if tally_dict['making waves'] < target:
        location_button(target_title='the life of the mind')
        storylet_button(target_title='discuss politics at a salon')
        read_results()
        next_button()
        current_step = 'at court'
    else:
        draw()
        current_cards = []  # check_card()  todo: reimplement this

        if 'a visit from slowcakes amanuensis' in current_cards:
            pick_card(position=current_cards['a visit from slowcakes amanuensis'])
            storylet_button(target_title='i deserve a more emphatic typeface at the very least')
            read_results()
            next_button()
            draw()
        else:
            travel(target='your lodgings')
            location_button(target_title='attend to matters of society')
            storylet_button(target_title='use your influence to invite slowcakes amanuensis for a visit')
            next_button()
            storylet_button(target_title='i deserve a more emphatic type face at the very least')
            read_results()
            next_button()
            current_step = 'go to court'

    return current_step


def unknown_location():
    # todo: we dont know where we are! lets try a few things.
    # lets just try again
    current_step == location()
    if current_step == 'unknown':
        # location will hit perhaps not if present so that's already done. check if travel to the lodgings is available
        result = travel(target='your lodgings', safe=False)
        if not result:
            # well now what??
            pass
          
    return current_step


def london_hub():
    if tally_dict["seeking mr eatens name"] > 70:
        current_step = 'go to court'
    elif tally_dict['an earnest of payment'] > 0:
        current_step = 'payment'
    elif tally_dict['searing enigma'] > 0 or tally_dict['winsome dispossessed orphan'] == 0:
        current_step = 'orphan trade'
    elif tally_dict['fleeting recollections'] == 1:
        current_step = 'clear irrigo'
    elif tally_dict["winsome dispossessed orphan"] > 0:
        current_step = 'go to labyrinth'
    elif tally_dict["tribute"] > 19:
        current_step = 'depart london'

    return current_step


def main():
    global browser
    browser = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    browser.implicitly_wait(10)
    login()
    init_tally()
    current_step = location()

    # todo: implement this        
    '''   
    function_dict = {
        'unknown': unknown_location,
        'london': london_hub,
    }
    '''
    
    while True:
        actions = check_actions()
        if actions >= 5:
          
            # todo: implement this
            """
            location_function = function_dict['current_step']
            current_step = location_function.__call__()
            """
            
            if current_step == 'unknown':
                # todo: we dont know where we are! lets try a few things.
                # lets just try again
                current_step == location()
                if current_step == 'unknown':
                    # location will hit perhaps not if present so that's already done. check if travel to the lodgings is available
                    result = travel(target='your lodgings', safe=False)
                    if not result:
                        # well now what??

            elif current_step == 'london':
                if tally_dict["seeking mr eatens name"] > 70:
                    current_step = 'go to court'
                elif tally_dict['an earnest of payment'] > 0:
                    current_step = 'payment'
                elif tally_dict['searing enigma'] > 0 or tally_dict['winsome dispossessed orphan'] == 0:
                    current_step = 'orphan trade'
                elif tally_dict['fleeting recollections'] == 1:
                    current_step = 'clear irrigo'
                elif tally_dict["winsome dispossessed orphan"] > 0:
                    current_step = 'go to labyrinth'
                elif tally_dict["tribute"] > 19:
                    current_step = 'depart london'

            elif current_step == 'payment':
                travel(target='your lodgings')
                location_button(target_title="a professional reward")
                if tally_dict['professional perk'] == 4:
                    storylet_button(target_title="use your professional perks")
                    next_button()
                    storylet_button(target_title="gain a trade secret")
                    tally_dict['professional perk'] = 0
                else:
                    storylet_button(target_title="the wage of a crooked cross")
                    next_button()
                    tally_dict['an earnest of payment'] = 0
                    current_step = 'london'

            elif current_step == 'clear irrigo':
                location_button(target_title="fleeting recollections")
                storylet_button(target_title='call it to mind')
                next_button()

                tally_dict['fleeting recollections'] = 0
                tally_dict['irrigo'] = 0

                current_step = 'go to nadir'

            elif current_step == 'go to nadir':
                if tally_dict['irrigo'] >= 1:
                    travel(target='your lodgings')
                    current_step = 'london'
                else:
                    travel(target='the forgotten quarter')
                    location_button(target_title="return to the cave of the nadir")
                    storylet_button(target_title='make the journey')
                    next_button()
                    current_step = 'at nadir'


            elif current_step == 'at nadir':
                if tally_dict['irrigo'] >= 6:
                    current_step = 'leave nadir'

                else:
                    draw()
                    hand_dict = check_card(hand_size=4)
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


                    if fluke_trade_flag is None:
                        current_step = 'leave nadir'

                    elif "do you recall how they came to that place" in hand_dict.keys() and fluke_trade_flag:
                        pick_card(position=hand_dict["do you recall how they came to that place"])
                        storylet_button(target_title=fluke_trade_flag)
                        tally_dict = read_results(tally_dict)
                        next_button()

                    elif "the end of battles" in hand_dict.keys() and battles_flag:
                        pick_card(position=hand_dict["the end of battles"])
                        storylet_button(target_title=battles_flag)
                        tally_dict = read_results(tally_dict)
                        next_button()

                    elif "losing" in hand_dict.keys() and losing_flag:
                        pick_card(position=hand_dict["losing"])
                        storylet_button(target_title=losing_flag)
                        tally_dict = read_results(tally_dict)
                        next_button()

                    elif "a card game" in hand_dict.keys():
                        pick_card(position=hand_dict["a card game"])
                        storylet_button(target_title="deal yourself in")
                        tally_dict = read_results(tally_dict)
                        next_button()

                    else:
                        current_step = 'leave nadir'

            elif current_step == 'leave nadir':
                location_button(target_title="leave the cave of the nadir")
                storylet_button(target_title='leave')
                next_button()
                current_step = 'london'


            elif current_step == 'orphan trade':
                bazaar_button = browser.find_element_by_css_selector(css_selector="#root > div > div > div:nth-child(5) > div.content.container > div > div.col-primary > nav > ul > li:nth-child(5) > a")
                bazaar_button.click()

                search_bar = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > input")

                quantity = tally_dict["searing enigma"]
                if quantity > 0:
                    search_bar.clear()
                    search_bar.send_keys("searing enigma")

                    sell_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > li > div.js-item-controls.item__controls > a")
                    sell_button.click()

                    quantity_entry = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__controls > input")
                    quantity_entry.clear()
                    quantity_entry.send_keys(str(quantity))

                    final_sale_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(12) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__submit-button-container > button")
                    final_sale_button.click()

                    close_button = browser.find_element_by_css_selector(css_selector="body > div:nth-child(12) > div > div > div.exchange-ui__close-button--md-up > span > span.fa.fa-inverse.fa-stack-1x.fa-close")
                    close_button.click()

                quantity = 5 - tally_dict["diary of the dead"]
                if quantity > 0:
                    cryptics_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.nav.nav--stacked.nav--stacked--1-of-4.nav--stacked--roman > div > nav > ol > li:nth-child(13) > a")
                    cryptics_button.click()

                    search_bar.clear()
                    search_bar.send_keys("diary of the dead")
                    buy_button = browser.find_element_by_css_selector(css_selector="#main > div > span > div > div > div.stack-content.stack-content--3-of-4.shop > li > div.js-item-controls.item__controls > a")
                    buy_button.click()

                    quantity_entry = browser.find_element_by_css_selector(css_selector="body > div:nth-child(13) > div > div > div:nth-child(2) > div:nth-child(5) > form > div.exchange-ui__controls > input")
                    quantity_entry.clear()
                    quantity_entry.send_keys(str(quantity))

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
                while result == True:
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

                current_step = 'go to labyrinth'

            elif current_step == 'go to labyrinth':
                travel(target='labyrinth of tigers')
                current_step = 'favor trade'

            elif current_step == 'favor trade':
                if tally_dict["winsome dispossessed orphan"] > 0:
                    location_button(target_title="offering tribute to the court of the wakeful eye")
                    storylet_button(target_title="offer a winsome dispossessed orphan")
                    tally_dict = read_results(tally_dict)
                    next_button()
                else:
                    current_step = 'depart london'

            elif current_step == 'depart london':
                try:
                    travel('wolfstack docks')
                except sexcept.ElementNotInteractableException:     # already there
                    pass

                location_button(target_title="put to zee")
                storylet_button(target_title="lay in supplies and sail")
                next_button()
                next_button()
                current_step = 'zailing to court'

            elif current_step == 'zailing':
                if tally_dict["searing enigma"] > 0:
                    current_step = 'zailing to london'
                else:
                    current_step = 'zailing to court'
                
            elif current_step == 'zailing to court':
                if tally_dict['approaching journeys end'] < 10:
                    zailing(tally_dict)
                else:
                    location_button(target_title='across the southern archipelago')
                    storylet_button(target_title="the court of the wakeful eye")

            elif current_step == 'enigma trade':
                if tally_dict['tribute'] >= 20:
                    storylet_button('join the minister of enigmas for teatime')
                    tally_dict = read_results(tally_dict)
                    next_button()
                else:
                    current_step = 'depart court'

            elif current_step == 'depart court':
                storylet_button(target_title="set to zee")
                next_button()
                next_button()

                current_step = "zailing to london"

            elif current_step == 'zailing to london':
                if tally_dict['approaching journeys end'] < 10:
                    zailing(tally_dict)
                else:
                    location_button(target_title='across the southern archipelago')
                    storylet_button(target_title="london")
                    next_button()

            elif current_step == 'winking isle':
                if tally_dict["seeking mr eatens name"] < 77:

                    if tally_dict["fasting and meditating to a foolish end"] < 11:
                        location_button(target_title='preparations')
                        storylet_button(target_title='you have set aside jewels and riches')
                    elif tally_dict["fasting and meditating to a foolish end"] < 22:
                        location_button(target_title='preparations')
                        storylet_button(target_title='you have given up your intrigues')
                    elif tally_dict["fasting and meditating to a foolish end"] < 33:
                        location_button(target_title='preparations')
                        storylet_button(target_title='you have rejected wine and song')
                    elif tally_dict["fasting and meditating to a foolish end"] < 44:
                        location_button(target_title='preparations')
                        storylet_button(target_title='no map knows the place you go')
                    elif tally_dict["fasting and meditating to a foolish end"] < 55:
                        location_button(target_title='preparations')
                        storylet_button(target_title='no more sweet memories no more bitter')
                    elif tally_dict["fasting and meditating to a foolish end"] < 66:
                        location_button(target_title='preparations')
                        storylet_button(target_title='you know nothing of stones light')
                    elif tally_dict["fasting and meditating to a foolish end"] < 77:
                        location_button(target_title='preparations')
                        storylet_button(target_title='your chiefest treasures are gone')
                        tally_dict = read_results(tally_dict)
                        next_button()
                        storylet_button(target_title='the lower mysteries')
                    elif tally_dict["fasting and meditating to a foolish end"] < 100:
                        location_button(target_title='the well')
                        storylet_button(target_title='wait by the well')
                    elif tally_dict["fasting and meditating to a foolish end"] < 10000:
                        location_button(target_title='the well')
                        storylet_button(target_title='circle the well')
                    elif tally_dict["fasting and meditating to a foolish end"] >= 10000 and tally_dict["seeking mr eatens name"] >= 70:
                        location_button(target_title='the well')
                        storylet_button(target_title='understand')
                    elif tally_dict["fasting and meditating to a foolish end"] < 60000 and tally_dict["seeking mr eatens name"] < 70:
                        location_button(target_title='the well')
                        storylet_button(target_title='circle the well')
                    elif tally_dict["fasting and meditating to a foolish end"] >= 60000 and tally_dict["seeking mr eatens name"] < 70:
                        location_button(target_title='the well')
                        storylet_button(target_title='insight')

                    tally_dict = read_results(tally_dict)
                    next_button()
                else:
                    current_step = 'leave the isle'

            elif current_step == 'leave the isle':
                quit()

            elif current_step == 'go to court':
                travel(target='your lodgings')
                location_button(target_title='find new stories chat with the local gossip')
                storylet_button(target_title='speak to the bohemian sculptress')
                storylet_button(target_title='into the empress court')

                while get_location() != 'the empress court':
                    next_button()
                current_step = 'at court'

            elif current_step == 'at court':
                target = 4*tally_dict['notability'] + 7
                if tally_dict['making waves'] < target:
                    location_button(target_title='the life of the mind')
                    storylet_button(target_title='discuss politics at a salon')
                    read_results(tally_dict)
                    next_button()
                else:
                    draw()
                    current_cards = []  # check_card()  todo: reimplement this

                    if 'a visit from slowcakes amanuensis' in current_cards:
                        pick_card(position=current_cards['a visit from slowcakes amanuensis'])
                        storylet_button(target_title='i deserve a more emphatic typeface at the very least')
                        tally_dict = read_results(tally_dict=tally_dict)
                        next_button()
                        draw()
                    else:
                        travel(target='your lodgings')
                        location_button(target_title='attend to matters of society')
                        storylet_button(target_title='use your influence to invite slowcakes amanuensis for a visit')
                        next_button()
                        storylet_button(target_title='i deserve a more emphatic type face at the very least')
                        tally_dict = read_results(tally_dict=tally_dict)
                        next_button()
                        current_step = 'go to court'

        else:
            print("not enough actions, sleeping for 10 minutes.")
            sleep(600)
            browser.refresh()

if __name__ == '__main__':
    main()
