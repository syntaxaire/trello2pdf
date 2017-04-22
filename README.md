# trello2pdf
## Overview
This Python 3 utility scans a Trello card list and creates a PDF with a table.

Example: Given 3 cards with the descriptions below:

(Card 1 description)  
Date: August 1  
Time: 3:00PM  
Foo: Egg

(Card 2 description)  
Date: August 5  
Time: 4:00PM  

(Card 3 description)  
Date: August 7  
Time: 1:00AM  
Notes: Bring a chair  

trello2pdf would read the list and create a pdf containing a table like this:

    Date      Time      Foo     Notes
    August 1  3:00PM    Egg
    August 5  4:00PM
    August 7  1:00AM            Bring a chair

This was written to automate creation of a schedule on Dropbox from a Trello notebook.

## Configuration
Copy secrets.cfg.example to secrets.cfg and enter your Trello API and OAuth parameters.

Enter the desired board and list ID in trello2pdf.cfg. You can find these by adding .json to the URL of your board and list on the official Trello web client.
