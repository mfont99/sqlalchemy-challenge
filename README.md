# sqlalchemy-challenge
Module 10 challenge assignment

Most of the "climate_starter.ipynb" file is my own code, the only thing I struggled with a little bit was the section where I had to use the datetime import. I was getting a lot of errors, so I used the Xpert Learning Assistant to debug my code, during which I learned that I had to specify "dt.datetime.strptime" instead of just "dt.strptime". 

As far as the app goes, it mostly went smoothly, and was a lot of copying and pasting from the other file. The hardest parts were definitely these two routes: "/api/v1.0/<start_date>" and "/api/v1.0/<start_date>/<end_date>". Getting the webpage to correctly interpret the inputs for the dates took a lot of trial and error, and the debugging process was certainly aided by the Xpert Learning Assistant. Thankfully it all worked out in the end, as long as the date inputs are entered in YYYY-MM-DD form and that date actually exists in the .csv file. 