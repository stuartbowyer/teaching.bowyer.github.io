# Teaching Materials

## Building Locally (using nix)
Activate nix-shell
```zsh
nix-shell
```

Develop (you need to activate nix-shell first otherwise vscode cannot talk to the python environment)
```zsh
code .
```

Build all
```zsh
./resources/buildall.sh
```

## WARNING
To ensure you do not accidentally push patient level MIMIC data to git, you need to strip the cell outputs with the following added to the `.git/config`
```bash
[filter "strip-notebook"]
    clean = jq --indent 1 '(.cells[] | select(.metadata.tags | index(\"remove-output\")) | .outputs) = []'
    smudge = cat
```