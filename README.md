# Blog
A blog with Notion as content management system. Imports content from notion and publishes it.

## Required
You need to create a `.secrets` file with the following contents:

```
#!/bin/bash

export TOKEN_V2="<YOUR TOKEN_V2>"
export SPACE_ID="<WORKSPACE ID>"
```

- Token can be obtained from cookies as `token_v2` after logging in Notion.

- To obtain workspace id, use developer tools in browser. Go to Networks tab
and press `Ctrl+R` to reload the page. Look for `getSpaces` object. Click on the
object and go to **Preview** tab. Expand and look for id in `spaces` value 
corresponding to the required workspace.

Give execute permissions to this file:

```
chmod +700 .secrets
```

## Runnning

After creating the `.secrets` file, run the program as follows:

```
bash run.sh
```
