# Mission-to-Mars
## An exercise in web scraping, web building

This project involved scraping data from government websites and consolidating the desired data into our own site.

To gather the date we wanted from other sites, we used
- Beautiful Soup
- Splinter
- request
- chromedrivermanager 

To store the data collected, or at least references for the images, we used MongoDB - a non-relational database with a format very similar to JSON files and Python dictionaries

To assist Python in getting data from MongoDB to HTML, we used Flask. This also enabled the implementation of an interactive button on the website that triggered a data update.

And finally, we used HTML to lay out the website, and referenced Bootstrap for formatting controls.

## Python code
We developed and tested the scraping commands in a jupyter notebook, to allow for easy testing as we went.

To mqke the process productional, we exported the code to VScode, wrapped it into functions as appropriate, saved as scaping.py.

To control the execution of the scraping, and passing data back and forth between Python, MongoDB, and the HTML file, we developed app.py.  This is the function that needs to be triggered from the terminal to enable the process.

We placed the html code in a subfolder called 'templates' - this is what Flask expects and requires to function properly.
