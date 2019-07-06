# Data Preparation
<!--- --->

In this challenge Data Preparation is equivalent to designing levels for the arena.

## Syllabus

The syllabus is described on the challenge [blog](https://mdcrosby.com/blog/animalailaunch.html)


### 1. Food
> Most animals are motivated by food and this is exploited in animal cognition tests. The same is true here. Food items provide the only positive reward in the environment and the goal of each test is to get as much food as possible before the time runs out (usually this means just getting 1 piece of food). This introductory category tests the agent's ability to reliably retrieve food and does not contain any obstacles.

<p align="center">
  <img src="https://mdcrosby.com/blog/figs/GoodGoal.png">
</p>


I think this category is very simple. A model without memory could solve it. It will just have to learn to move towards the food.
If it does not see the food at first sight just rotate and the model will find it.

### 2. Preferences
> This category tests an agent's ability to choose the most rewarding course of action. Almost all animals will display preferences for more food or easier to obtain food, although the exact details differ between species. Some animals possess the ability to make complex decisions about the most rewarding long-term course of action.

<p align="center">
  <img src="https://mdcrosby.com/blog/figs/BadGoal.png">
</p>

This category is much more complex than the first one. To be able to choose the agent has to first explore all the arena and remember all the options. The agent needs: **memory, ranking**.

### 3. Obstacles
>This category contains immovable barriers that might impede the agent's navigation. To succeed in this category, the agent may have to explore its environment. Exploration is a key component of animal behaviour.

<p align="center">
  <img src="https://mdcrosby.com/blog/figs/Wall.png">
</p>

If there are walls then the agent needs to know that it does not know what is it behind the wall and go to explore it. The agent needs: **memory, uncertainty, navigation**.

### 4. Avoidance
>This category introduces the hot zones and death zones, areas which give a negative reward if they are touched by the agent. A critical capacity possessed by biological organisms is the ability to avoid negative stimuli. The red zones are our versions of these, creating no-go areas that reset the tests if the agent moves over them. This category of tests identifies an agent’s ability to detect and avoid such negative stimuli.

<p align="center">
  <img src="https://mdcrosby.com/blog/figs/DeathZone.png">
</p>

I don't think adding death zones increases the difficulty too much.

Pain zones on the other hand increase the complexity of **planning**. For example if there are many
paths to a goal with different pain zones the agent should choose the less painful one.
We can think of different arenas where planning is needed:
* A dead zone dividing the arena and only a path of harm zone to cross
* A maze of dead zone with harm zones to navigate over it.

Sometimes we have to avoid harm zones and other times we have to cross them to get to the food.

### 5. Spatial Reasoning
>This category tests an agent's ability to understand the spatial affordances of its environment. It tests for more complex navigational abilities and also knowledge of some of the simple physics by which the environment operates.

### 6. Generalization
>This category includes variations of the environment that may look superficially different to the agent even though the properties and solutions to problems remain the same. These are still all specified by the standard configuration files.

### 7. Internal Models
>This category tests the agent's ability to store internal models of the environment. In these tests, the lights may turn off after a while and the agent must remember the layout of the environment to navigate it in the dark. Many animals are capable of this behaviour, but have access to more sensory input than our agents. Hence, the tests here are fairly simple in nature, designed for agents that must rely on visual input alone.

<p align="center">
  <img src="https://mdcrosby.com/blog/figs/black.png">
</p>

To solve this tests **memory** is needed, but it also was needed previously. I thought of a mechanism that detected when the lights were off and instead of feeding black frames to the model feed the predictions.

### 8. Object Permanence
> Many animals seem to understand that when an object goes out of sight it still exists. This is a property of our world, and of our environment, but is not necessarily respected by many AI systems. There are many simple interactions that aren't possible without understanding object permanence and it will be interesting to see how this can be encoded into AI systems.

### 9. Advanced Preferences
>This category tests the agent's ability to make more complex decisions to ensure it gets the highest possible reward. Expect tests with choices that lead to different achievable rewards.

### 10. Causal Reasoning
>Finally we test causal reasoning, which includes the ability to plan ahead so that the consequences of actions are considered before they are undertaken. All the tests in this category have been passed by some non-human animals, and these include some of the more striking examples of intelligence from across the animal kingdom.

<!--
## Select Data
<!---Decide on the data to be used for analysis. Criteria include relevance to
the data mining goals, quality, and technical constraints such as limits on data
volume or data types. Note that data selection covers selection of attributes
(columns) as well as selection of records (rows) in a table.
List the data to be included/excluded and the reasons for these decisions.
## Clean Data
<!---Raise the data quality to the level required by the selected analysis techniques.
This may involve selection of clean subsets of the data, the insertion of suitable
defaults, or more ambitious techniques such as the estimation of missing data by
modeling. Describe what decisions and actions were taken to address the data
quality problems reported during the Verify Data Quality task of the Data
Understanding phase. Transformations of the data for cleaning purposes and the
possible impact on the analysis results should be considered. 
## Construct Data
<!---This task includes constructive data preparation operations such as the
production of derived attributes or entire new records, or transformed values
for existing attributes. 
## Integrate Data
<!---These are methods whereby information is combined from multiple tables or
records to create new recordsor values. 
## Format Data
<!---Formatting transformations refer to primarily syntactic modifications made
to the data that do not change its meaning, but might be required by the
modeling tool. --->
