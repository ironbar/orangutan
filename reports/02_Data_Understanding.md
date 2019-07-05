# Data Understanding
## Collect initial data
<!---Acquire the data (or access to the data) listed in the project resources.
This initial collection includes data loading, if necessary for data understanding.
For example, if you use a specific tool for data understanding, it makes perfect
sense to load your data into this tool. This effort possibly leads to initial data
preparation steps.
List the dataset(s) acquired, together with their locations, the methods used to
acquire them, and any problems encountered. Record problems encountered and any
resolutions achieved. This will aid with future replication of this project or
with the execution of similar future projects.

>	Indeed it's a pain downloading huge files. Especially when there are connection issues. I used "wget" to download the dataset with an option "-c" for resuming capability in case the download fails.  You would need to save the cookies in the page using a chrome extension Chrome Extension  save the cookies as cookies.txt from the extension  Then you can download the files by using the following command  

	wget -c -x --load-cookies cookies.txt https://www.kaggle.com/c/dstl-satellite-imagery-feature-detection/data?train_wkt.csv.zip
--->

This is a special competition where there is no data. Instead there is an environment called "the arena" where an agent can play. I have downloaded the python library that allows to use the arena and I have played it already.

## External data
<!--- It is allowed in this challenge? If so write it here ideas of how to find
it and if people have already posted it on the forum describe it. --->

There is no reference to external data in the rules. Thus I believe we can use it, however it's difficult to think now
of external data that could be used in this challenge.


## Describe data
<!---Describe the data that has been acquired, including the format of the data,
the quantity of data (for example, the number of records and fields in each table),
the identities of the fields, and any other surface features which have been
discovered. Evaluate whether the data acquired satisfies the relevant requirements. --->

The arena is configured with yaml files. In the yaml files we can configure the objects, sizes, positions, orientations and colors.

The definition of the available objects can be found on [github](https://github.com/beyretb/AnimalAI-Olympics/blob/master/documentation/definitionsOfObjects.md)

<p align="center">
  <img height="400" src="https://github.com/beyretb/AnimalAI-Olympics/raw/master/documentation/PrefabsPictures/Arena.png">
</p>

A single arena is as shown above, it comes with a single agent (blue sphere, black dot showing the front), a floor and 
four walls. It is a square of size 40x40, the origin of the arena is `(0,0)`. You can provide coordinates for 
objects in the range `[0,40]x[0,40]` as floats.

It is possible to switch off the light of the arena.

## Explore data
<!---This task addresses data mining questions using querying, visualization,
and reporting techniques. These include distribution of key attributes (for example,
the target attribute of a prediction task) relationships between pairs or small
numbers of attributes, results of simple aggregations, properties of significant
sub-populations, and simple statistical analyses.

Some techniques:
* Features and their importance
* Clustering
* Train/test data distribution
* Intuitions about the data
--->

### Observations from playing

* The reward depends on the size of the ball, the bigger the ball the bigger the reward. Green balls yield positive rewards and red balls negative
* Some objects can be moved and even climb over them
* There is inertia in the movement
* I believe that designing difficult scenarios would be important in the challenge
* It is possible to place objects on top of others
* If the box is small is possible to rotate it and therefore to climb over the slope. If it is big and only moving it is allowed then is not possible to climb
* Is possible to move the goals using objects

### Ideas

* Learning to predict the world could allow to move the object even when the light is off. I could make a detector
of lightsoff that instead of feeding the black screen feeds the prediction of the model.
* There could be multiple termination goals in the same arena, so we have to first explore and choose the correct one.
* Design new arenas with increasing levels of difficulty.
* Creating a map from the observations of the agent may be very useful for planning


## Verify data quality
<!---Examine the quality of the data, addressing questions such as: Is the data
complete (does it cover all the cases required)? Is it correct, or does it contain
errors and, if there are errors, how common are they? Are there missing values in
the data? If so, how are they represented, where do they occur, and how common are they? --->

I have been playing the game and discovered a bug that when pressing forward or backwards at the same
time of rotating left or right the agent is capable of climbing higher heights. However when asking
to the host of the challenge he said that none of the tests require this bug to be solved.

**TODO:** I have to find if the resolution for playing the game is enough, and if it is possible to modify it.

## Amount of data
<!---
How big is the train dataset? How compared to the test set?
Is enough for DL?
--->

The amount of data will be proportional to the configuration files for the arena. So designing good levels
will be very valuable in the challenge.