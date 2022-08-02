# Editting a custom Jupyterlabs CSS page


Open a Jupyterlabs page, find the component you want to edit.
Displayed below:
![css_editor](https://user-images.githubusercontent.com/27964546/182395721-f345469d-6e7d-40d6-a45d-24c3aad040fc.png)

Find the variable which determines the size of the component. In this example we used:

```
--jp-private-horizontal-tab-height
```

Open the local index file of the Jupyterlabs page:
```
vim /usr/local/share/jupyter/lab/themes/@jupyterlab/theme-light-extension/index.css
```
At any line after the root open bracker (line 28), insert:

```
--jp-private-horizontal-tab-height: 0px;

```
Example:

![Screenshot from 2022-08-02 16-15-54](https://user-images.githubusercontent.com/27964546/182396894-16f5254a-8bac-47ab-9775-32e49f2125a3.png)


Close the file then launch labs.



# HOW TO ADD WORKSPACE
Navigate to File-> Save Workspace As
![Workspace_1](https://user-images.githubusercontent.com/27964546/181778983-181431e8-2c59-4cb7-a804-fbb35032d66b.png)

Give the Workspace a name:
![Workspace_2](https://user-images.githubusercontent.com/27964546/181780205-f0367432-1819-44fd-b03f-2eee6bf852c1.png)

For example the we named it MyWorkspace. The file has a default extension of .jupyterlab-workspace. Which is a custom Json file.

# Launch Workspace/Labs
To launch labs run command:
```
~ ./web_scripts/start_labs.sh
```

To add the workspace to the Jupyterlabs environment you must first run  the command.
```
jupyter lab workspaces import /[PATH_TO_FILE]/[filename].jupyterlab-workspace
```

For our example:
```
jupyter lab workspaces import /[PATH_TO_FILE]/MyWorkspace.jupyterlab-workspace
```


To activate the saved workspace in the browser:
```
http://[IP ADRESS]:[PORT]/lab/workspaces/[WORKSPACE NAME]
```

By default you can launch a workspace in this simcloud image. 

To launch a specific workspace:
```
~ ./web_scripts/start_workspace.sh
```




