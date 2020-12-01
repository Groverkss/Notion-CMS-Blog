# Blog
A blog with Notion as content management system. Imports content from notion and publishes it.

## Required
You need to create a `.secrets` file with the following contents:

```
#!/bin/bash

export TOKEN_V2="***REMOVED***"
export SPACE_ID="***REMOVED***"
```

Give execute permissions to this file:

```
chmod +700 .secrets
```
