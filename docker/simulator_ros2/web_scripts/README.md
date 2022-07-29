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




