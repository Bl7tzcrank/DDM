# DDM VRP with greedy confirmation and waiting

This implementation finds an optimal decision policy for the vehicle routing problem with greedy confirmation and waiting.

## Getting Started

You need to install anaconda and create an environment (https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). Next you should intall the following packages to your anaconda environment: itertools, gurobipy and networkx. You also need to bring in a gurobi license. Then move to the folder where your files are located and run  
```
source activate [environment name]
```
Then you can run the main.py by typing
```
python main.py
```
The main.py file contains various examples you can run. They differ in complexity and running time depending on number of customers and time limit.
As standard main.py will output something like this, running the first example in main.py:
```
Academic license - for non-commercial use only
State space size:231
EX:1.2527199999999998
```
You can also use the methods createGraphWithStates(policy), createSplitGraphWithStates(policy) and printStateSpace(policy) to get further insides into the implementation's output. The first two methods create .png files in the same folder where the files are located. The first method create one .png file which visualizes the state space as a graph. As this one can get very large for certain scenarios, the second method creates multiple .png files which together visualize the complete state space graph. The third method prints the state space to the console.