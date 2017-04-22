import configparser
import trello
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def main():
    config_files = ['secrets.cfg', 'trello2pdf.cfg']
    # our configuration and the Trello card list to be worked with
    config, target = init(config_files)
    cards = read_cards(target)
    table = gen_table(config, cards)
    gen_pdf(config, table)


def gen_table(config, cards):
    table = []
    # set up a row of column headers, capitalized as in the config file
    headers = [_.strip() for _ in config['Cards']['DescAttribs'].split(',')]
    table.append(headers)
    # set attribs, lowercased for consistency
    attribs = [_.lower() for _ in headers]
    for card in cards:
        # one row for each card
        row = []
        for attrib in attribs:
            # don't use a list comprehension because of potential missing keys
            if attrib in card:  # check if we have this one
                row.append(card[attrib])
            else:
                row.append('')  # a blank table cell
        table.append(row)
    return table


def gen_pdf(config, table):
    filename = config['PDF']['Basename']
    if config['PDF']['DateInName'] == 'yes':
        filename += " " + datetime.date.today().isoformat()
    filename += ".pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    doctable = Table(table, len(table[0])*[0.4*inch], len(table)*[0.4*inch])
    elements.append(doctable)
    doc.build(elements)


def read_cards(target):
    cards = []
    for card in target.list_cards():
        attribs = {}
        for line in card.description.split('\n'):
            if ':' in line:
                attrib, text = [_.strip() for _ in line.split(':', 1)]
                # lowercase for consistency for later scanning
                attribs[attrib.lower()] = text
        cards.append(attribs)
    return cards


def init(config_files):
    """
    Initialize things.
    Parameters:
        config_files : list of filenames to load
    Returns:
        config : a loaded configparser.ConfigParser
        target : a trello.List of trello.Cards
    """

    config = configparser.ConfigParser()
    config.read(config_files)

    api_key = config['TrelloAPI']['key']
    api_secret = config['TrelloAPI']['secret']
    oauth_token = config['OAuth']['token']
    oauth_secret = config['OAuth']['secret']
    client = trello.TrelloClient(api_key=api_key,
                                 api_secret=api_secret,
                                 token=oauth_token,
                                 token_secret=oauth_secret)

    try:
        boardid = config['Trello']['BoardID']
        board = client.get_board(boardid)
    except:
        print("ERROR: Couldn't get board with ID", boardid)
        raise

    try:
        listid = config['Trello']['ListID']
        target = board.get_list(listid)
    except:
        print("ERROR: Couldn't get list with ID", listid)
        raise

    return (config, target)


if __name__ == '__main__':
    main()
