# TourGuide
TourGuide determines the best place an artist should tour.  It gathers tweets, runs sentiment analysis, and creates a bar graph of the
total sentiment vs the location.  This can be done for any artist, simply need to change the name and twitter handle.

## Code Example

> ```
> drake = Artist('Drake', '@Drake')
> drake.store_data()
> drake.create_graph()
> ```

store_data() will gather and store the raw data from twitter and create_graph() will generate a bar graph as pictured here.

![Drake: Total Sentiment vs. Location](https://github.com/Jiafi/TourGuide/blob/master/src/data/Drake_graph.png?raw=true)
