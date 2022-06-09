from colorama import Fore, Back, Style, init
import json
#
init(autoreset=True)

inp = input("What adventure would you like to load? (eg: cmod_example.json)\n")

VERSION = "v0.1 alpha"
VERSION_ID = "1-cmodded"
SETTINGS_FILE = inp

try:
    with open(SETTINGS_FILE, "r") as f:
        SETTINGS = json.load(f)
except json.decoder.JSONDecodeError:
    print("Error loading JSON.")
    exit(1)
except FileNotFoundError:
    print("Error finding JSON")
    exit(1)

conf = SETTINGS
version = VERSION
version_id = VERSION_ID
game_versions_id = conf['settings']['versions_supported']
inventory = conf['settings']['starting_inventory']

if not version_id in game_versions_id:
    print(Fore.RED + "Unsupported Version Installed for that Text Adventure")
    exit(1)

if conf['settings']['credit']:
    print(f"Text Adventure Generator {version}by Wooferz and modded by coldening.")
try:
    conf['settings']['title']
    conf['settings']['author']
except KeyError:
    pass
else:
    print(conf['settings']['title'], "by", conf['settings']['author'])


def colour_text(text):
    text = text.replace("[red]", Fore.RED).replace("[blue]", Fore.BLUE).replace(
        "[green]", Fore.GREEN).replace("[yellow]", Fore.YELLOW).replace("[reset]", Fore.RESET + Back.RESET + Style.RESET_ALL)
    return text


def space():
    print("\n")


def run_scenario(scenario):
    space()
    space()
    print(colour_text(scenario['text']))
    if scenario['item_giving'] != "none":
        inventory.append(scenario['item_giving'])
    if scenario['item_required'] != "none":
        if scenario['item_required'] not in inventory:
            print(colour_text("[red]You do not have that item.[reset]"))
            exit()
    if scenario['item_taking'] != "none":
        if scenario['item_taking'] not in inventory:
            print(colour_text("[red]You do not have the item that the text adventure is trying to take.[reset]"))
            exit()
        else:
            inventory.remove(scenario['item_taking'])
    space()
    print("Your current inventory:")
    for i in inventory:
        print(i)
    space()
    try:
        scenario['children']
    except KeyError:
        exit()

    a = 1
    for i in scenario['children']:
        print(colour_text(f"{a}. {i['option_text']}"))
        a += 1
    space()
    while True:
        inp = input("Selct option:\n")
        try:
            int(inp)
        except ValueError:
            print("Invalid Option")
        else:
            inp = int(inp)
            if inp > 0 and inp < a:
                break
            else:
                print("Invalid Option")
    run_scenario(scenario['children'][int(inp)-1])


try:
    run_scenario(conf["game"])
except KeyboardInterrupt:
    print(colour_text("\n\n[red]Exiting..."))
    exit()
except KeyError:
    print(colour_text(
        "[red]Something went wrong in the config, probably."))
