# Flight Delay Predictor

This project was written by Tyler Conley and Preston Bell for our HackUSU 2023 submission. We couldn't figure out audio for our video, so we
made a [pdf]('Hack USU.pdf') to showcase our project a little bit more.

This project uses a statistical machine learning model to compute the chance of a future flight being delayed or not. It also uses a simple Flask
web application for a user to interface with it.

The training data needs to be downloaded from [this url](https://www.kaggle.com/datasets/threnjen/2019-airline-delays-and-cancellations?resource=download&select=full_data_flightdelay.csv)
It needs to be saved into `./content/` in order to train the model up properly
