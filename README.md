# Blog
A blog with Notion as content management system. Imports content from notion and publishes it.

## Required
1. You need to create a folder named `exports` where to zips will be copied to
2. You need to create a `.secrets` file with the following contents:

```
#!/bin/bash

export TOKEN_V2="fa46801a00393e25d2b4d432305b1491776784ea0acd75fdfecf69e1031417e6dc80fb103724ccefd49fbacbcf98ea17b762ed1106dde81cc8fe3c28f4967304ffa4cda58fb7e90412f8b47dd581"
export SPACE_ID="8f1a4aff-d199-4355-872f-f6887b2701bb"
```

Give execute permissions to this file:

```
chmod +700 .secrets
```
