# orangutan
Project for AnimalAI challenge

http://animalaiolympics.com/

## Code structure

     |_ source
     |_ forum: all the scritps and notebooks taken from the forum
     |_ logs: folder for storing all kind of stats and logs. For example the
     score of each model, results from experiments
     |_ notebooks: jupyter notebooks made during the challenge. They start by number for easier sorting.
     |_ reports: documents made during the challenge according to CRISP-DM methodology
     |_ tests: folder with tests for the library
     |_ data: folder with light data from teh challenge
     |_ rules: the official rules of the challenge

## Challenge workflow

### Start of the challenge
1. Add dates to the calendar
1. Download rules of the challenge
2. Create a repository for the code using cookiecutter
3. Create a Google keep label for tasks and ideas of the challenge
3. Download the challenge data
4. Create a conda environment for the challenge

    conda create -n repo_name pytest rope pylint tqdm numpy pandas sklearn
    source activate repo_name
    conda install -c conda-forge jupyter_contrib_nbextensions
    conda env export > environment.yml


4. Work on the challenge
5. Use TDD methodology whenever possible, this will save time because errors
won't be propagated along the challenge.
5. Have an aprentice aptitude, collaborate on the forum, I have a lot to learn
from Kaggle.
5. Prepare a report with a summary of the aproach to the challenge

### End of the challenge
1. Prepare a report with a summary of the aproach to the challenge
6. Download the Google keep tasks to the repository in pdf format
6. Delete the tasks on google keep and the label
7. Delete unnecessary data
8. Update the environment yml

## Methodology
I'm following [CRISP-DM 1.0](https://www.the-modeling-agency.com/crisp-dm.pdf) methodology for the reports.

I have skipped Evaluation and Deployment steps because they are not usually done on Kaggle.

1. [Business understanding](reports/01_Business_Understanding.md)
1. [Data understanding](reports/02_Data_Understanding.md)
1. [Data preparation](reports/03_Data_Preparation.md)
1. [Modeling](reports/04_Modeling.md)
1. [Solution summary](reports/05_Solution_Summary.md)