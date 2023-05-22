# Eurovision 2023 Odds - Web Scraping

This mini-project consists of collecting data on the probability of winning the Eurovision Song Contest 2023, which will be held in the United Kingdom on Saturday, May 13.

## Links
- [Twitter - eurovision_data](https://twitter.com/eurovision_data): illustrations that appear in this twitter profile were designed and created by **Alejandra Rodríguez Ramírez** with Adobe Illustrator and Adobe Photoshop. Here you can find [her LinkedIn profile](https://es.linkedin.com/in/alejandrarodriguezramirez).
- [Kaggle - Dataset](https://www.kaggle.com/datasets/anxods/eurovision-2023-betting-odds)

## Data access

To make it easier to read the data, we created this spreadsheet in Google Sheets. It can be accessed [here](https://docs.google.com/spreadsheets/d/1SkcXpMeDGgqKFdMBL_9LICRxvMGqID86YT8WS91Lvmg/edit?usp=sharing)

## How does the script work?

With the execution of the file written in python 'scraping.py', we will obtain daily, by means of _web scraping_, the data of probability of victory of all the songs and participating artists, according to different bookmakers.

The data, as we said before, will be obtained by means of the _web scraping_ technique, accessing the following URL and collecting the data from the table that appears in it: https://eurovisionworld.com/odds/eurovision

And, since April 13th we started collecting Spotify streaming data from participating songs, via the Spotify API, collecting the metrics they provide: _popularity_.

Here, we can find a description of this value, and how it is calculated by the API:

> The popularity of the track. The value will be between 0 and 100, with 100 being the most popular. The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are. Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity.