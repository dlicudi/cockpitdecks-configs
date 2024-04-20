# Development Guide


## Visual Studio Code setup


``` json title="settings.json"
{
    "yaml.schemas": {
      "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    },
    "yaml.customTags": [ 
      "!ENV scalar",
      "!ENV sequence",
      "!relative scalar",
      "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
      "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
      "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
    ]
  }
```


``` json title="launch.json"
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Cessna 172 SP",
      "type": "python",
      "request": "launch",
      "program": "~/Documents/GitHub/cockpitdecks/bin/cockpitdecks_upd_start.py",
      "args": [
        "~/Documents/Github/cockpitdecks-configs/decks/cessna-172-sp/"
      ],
      "console": "integratedTerminal",
      "pythonPath": "python3.10"
    },
    {
      "name": "Beechcraft Baron 58",
      "type": "python",
      "request": "launch",
      "program": "~/Documents/GitHub/cockpitdecks/bin/cockpitdecks_upd_start.py",
      "args": [
        "~/Documents/Github/cockpitdecks-configs/decks/beechcraft-baron-58/"
      ],
      "console": "integratedTerminal",
      "pythonPath": "python3.10"
    },
    {
      "name": "Cirrus SR22",
      "type": "python",
      "request": "launch",
      "program": "~/Documents/GitHub/cockpitdecks/bin/cockpitdecks_upd_start.py",
      "args": [
        "~/Documents/Github/cockpitdecks-configs/decks/cirrus-sr22/"
      ],
      "console": "integratedTerminal",
      "pythonPath": "python3.10"
    },
    {
      "name": "Robin DR401",
      "type": "python",
      "request": "launch",
      "program": "~/Documents/GitHub/cockpitdecks/bin/cockpitdecks_upd_start.py",
      "args": [
        "${workspaceFolder}/decks/robin-dr401/"
      ],
      "console": "integratedTerminal",
      "pythonPath": "python3.10"
    }
  ]
}


```