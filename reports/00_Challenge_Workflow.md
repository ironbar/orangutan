# Challenge workflow

## Start of the challenge
1. Add dates to the calendar
1. Download rules of the challenge
2. Create a repository for the code using cookiecutter
3. Create a Google keep label for tasks and ideas of the challenge
3. Download the challenge data
4. Create a conda environment for the challenge and add it to jupyter

```bash
conda create -n repo_name pytest rope pylint tqdm numpy pandas scikit-learn ipython ipykernel
source activate repo_name
python -m ipykernel install --user --name repo_name --display-name "Python (repo_name)"
conda env export > environment.yml
```

4. Work on the challenge
5. Use TDD methodology whenever possible, this will save time because errors
won't be propagated along the challenge.
5. Have an aprentice attitude, collaborate on the forum, I have a lot to learn
from Kaggle.

## End of the challenge
1. Prepare a report with a summary of the aproach to the challenge
6. Download the Google keep tasks to the repository in pdf format
6. Delete the tasks on google keep and the label
7. Delete unnecessary data
8. Update the environment yml

