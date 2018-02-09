```none
  ,---.   ,---.    .--.  .-. .-.         ,---.  ,-.   .---.  _______ ,---.  ,---.    
 | .-.\  | .-.\  / /\ \ | | | ||\    /| | .-'  |(|  ( .-._)|__   __|| .-'  | .-.\   
 | |-' \ | `-'/ / /__\ \| | | ||(\  / | | `-.  (_) (_) \     )| |   | `-.  | `-'/   
 | |--. \|   (  |  __  || | | |(_)\/  | | .-'  | | _  \ \   (_) |   | .-'  |   (    
 | |`-' /| |\ \ | |  |)|| `-')|| \  / | |  `--.| |( `-'  )    | |   |  `--.| |\ \   
 /( `--' |_| \)\|_|  (_)`---(_)| |\/| | /( __.'`-' `----'     `-'   /( __.'|_| \)\  
(__)         (__)              '-'  '-'(__)                        (__)        (__) 
```

# Install
To install and/or update `braumeister`
```sh
pip3 install braumeister --upgrade
```

# Usage
```sh
$ braumeister --help
usage: braumeister [-h] [-r] [-u] fix_version

Create a release branch based on the "fixVersion" field in JIRA and your `master` branch. (v0.0.5)

positional arguments:
  fix_version        e.g. "Krazy Kant"

optional arguments:
  -h, --help         show this help message and exit
  -r, --resume       Continue after last merge conflict
  -u, --update_jira  Also update Jira status after merging an issue
```

# Development

Running tests
```sh
python3 -m unittest discover -p *_test.py
```