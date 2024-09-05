# Garmin vs Whoop - A Comparison

In this repository you will find code and data that I used to compare wearable data collected from a Garmin Venu (worn on my non-dominant arm) and a Whoop 4.0 
(worn on my dominant arm).

## Data Format
### Garmin
I extracted Garmin data using Garmin Health API. You can do that using several tools:
- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
- [GarminDB](https://github.com/tcgoetz/GarminDB)

From Garmin Health API data, I exported them in CSV format. You can find my Garmin data [here](Data/Garmin).

### Whoop
For Whoop data, I did not use the Whoop API but instead I exported the data directly from the Whoop app. Unfortunately, my data are in italian (I still couldn't find a way to export them in a different language). You can find my Whoop data [here](Data/Whoop).

## Setup
1. Clone this repository by running ``git clone https://github.com/dado93/garmin-vs-whoop.git``
2. Change directory ``cd garmin-vs-whoop``
3. Install the requirements in your environment ``pip install -r requirements.txt``
4. Run the notebooks that you find under the [``Notebooks``](Notebooks) folder

