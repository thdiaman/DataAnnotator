# DataAnnotator
A data annotator that can be used to annotate different types of datasets.

## How to use
All datasets to be annotated must have a specific file/folder structure.  
In specific, a dataset must be inside a folder with the name of the dataset, which should include:  
- a subfolder named `files`, which contains the data instances to be annotated. All data instances inside the files subfolder must be in JSON format.
- a file named `schema.json` that allows defining the schema of the data instances. The schema can have all JSON elements (arrays and nested objects), while the accepted data types include `ID`, `STRING`, `NUMBER`, `URL`, `CODE` (source code), `IMAGE` (image in base64 format). The schema must have **exactly one ID**.
- a file named `classes.json` that allows defining the classes to annotate  the data instances. 

Upon setting this structure, make sure to set the dataset folder in file `properties.py`. After that, the app can be executed using `python -m flask --debug --app run run`

Opening a browser at `localhost:5000` provides the interface of the annotator. The interface allows moving backwards and forwards to iterate over data instances and annotating the current data instance. Apart from the buttons, the interface support keyboard shortcuts (left/right arrow keys for moving backwards/forwards, numbers 0-9 to annotate the corresponding categories). Upon selecting a new category, the interface can move to the next data instance (next page), as long as the variable `nextpage` in file `properties.py` is set to True.

Finally, the annotations are stored in the dataset folder, with the name `annotations.json`

## Examples
There are three examples in folder data:
- Commits: An annotation scenario where source code commits are annotated according to their purpose (adding a new feature, improving existing code, adding documentation, fixing a bug). The example demonstrates how there are multiple fields in the commits/json objects, however only a few of them are shown, as defined in the schema.
- Images: An annotation scenario where images are annotated according to whether they depict a dog or a cat. The example further includes a script (in subfolder `originalimages`) that converts png images to json objects for annotation.
- Recipes: An annotation scenario where recipes are annotated according to whether they are salty or sweet. The example further includes a script (in subfolder `originalrecipes`) that converts xml documents to json objects for annotation.


