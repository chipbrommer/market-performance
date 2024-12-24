# market-performance
A simple python application to generate a bar chart for market performance on a list of tickers on or after a set date. 


### Change / Add tickers
To add or change the list of tickers, please adjust the `TICKERS` variable on line 7. 
This is a list and will create a bar in the chart for each year, for each ticker. 

### Change Date
To change the date to conform to your needs, please adjust the `TARGET_MONTH_DAY` variable on line 10. 
This will change the targeted date, and the program will search for next valid data on or after the specified date. 

To adjust the year range, change the `START_YEAR` and `END_YEAR` to fit your desired range. 

