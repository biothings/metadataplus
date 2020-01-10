# Metadata Plus Site

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## VSCode Debug Configuration

```        
{
    "name": "Debug Mplus",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}\\index.py",
    "console": "integratedTerminal",
    "env": {
        "ES_HOST": "REPLACE_HERE",
        "ES_INDEX_GEO": "REPLACE_HERE"
    },
    "args": [
        "--geo-host=localtest:8000",
        "--server-host=localhost:8000"
    ],
    "justMyCode": false
}
```

