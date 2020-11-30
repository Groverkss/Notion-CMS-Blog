# Blog
A blog with Notion as content management system. Imports content from notion and publishes it.

## Required
1. You need to create a folder named `exports` where to zips will be copied to
2. You need to create a `.secrets` file with the following contents:

```
#!/bin/bash

export TOKEN_V2="***REMOVED***"
export SPACE_ID="***REMOVED***"
```

Give execute permissions to this file:

```
chmod +700 .secrets
```
