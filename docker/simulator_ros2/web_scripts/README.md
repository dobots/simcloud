# Asimovo Jupyter
Instructions to convert Markdown to jupyter readable files.
Request for new wiki makers, add tags. (Further to be explained)

Jupyter Asimovo Notebooks:

The Asimovo Wiki now exist as Jupyter Notebooks, but are mostly none interactive.

Software, Libraries, Plugins:
- Jupyter Notebooks/Labs
- Jupytext 
- Jupyros  (https://github.com/RoboStack/jupyter-ros), using a Ros2 port from (https://github.com/zmk5/jupyter-ros2 ) 
- Development of singular package for Ros1 and Ros2 (git clone --single-branch -branch Ros2 https://github.com/dobots/jupyter-ros/)


To Do:
- Port Jupyros to Ros2   (Current Ros2 Fork is deprecated)
  -Communications between Jupyter and Nodes succesful   
- Create basic interactive nodes
-


## How to read this document
This document will explain how the Jupyter interactive Notebooks for the Asimovo platform works. 
With this document as user will:
- How to Navigate and use the Jupyte (labs) environment
- Be able to create their own their own notebooks
- Be able to interact with  Ros/Asimovo via the Jupyterlabs environment
- Create Notebooks to interact with Ros
- Create Notebooks as entire projects for the Asimovo platform
- Understand how the Jupyter (Labs) systems work on asimovo and thus further customize it to their desire

## Start Jupyter in Asimovo
To start the Jupyter Server on Asimovo, run the following script:
```
~/web_scripts/start_lab.sh 
```
Open a browser and navigate to [container ip]:8080 . If you use the start_lab.sh script, the container IP adress will be shown at startup.

## How to create Jupyter files
To create a Jupyter Notebooks on the Asimovo Platform a user has two options.
- Jupyter Notebooks environment (https://jupyter.org/)
- Myst Markdown (https://jupyterbook.org/en/stable/content/myst.html)

For beginner or novice users the Jupyter Notebooks environment is recommended. 

### Jupyter Notebooks
Using Jupyter Notebooks


### Markdown users
The biggest advantage to using Myst Mardkwon is that a Jupyter Notebook could be presented as a markdown file, and thus would not require an external entity to run their own Jupyter Server. Most modern browsers would automatically open the markdown filea.


## How to interact with Ros/Asimovo with Jupyter



## Using Nodes with Jupyter

### Using A Jupyter cell
```{code-cell}
!ros2 <package name> <node name> 
```
