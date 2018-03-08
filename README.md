[![PyPI](https://img.shields.io/pypi/v/Braumeister.svg)](https://pypi.python.org/pypi/Braumeister/)
[![Build Status](https://travis-ci.org/talentsconnect/braumeister.svg?branch=master)](https://travis-ci.org/talentsconnect/braumeister)

```none
  ,---.   ,---.    .--.  .-. .-.         ,---.  ,-.   .---.  _______ ,---.  ,---.    
 | .-.\  | .-.\  / /\ \ | | | ||\    /| | .-'  |(|  ( .-._)|__   __|| .-'  | .-.\   
 | |-' \ | `-'/ / /__\ \| | | ||(\  / | | `-.  (_) (_) \     )| |   | `-.  | `-'/   
 | |--. \|   (  |  __  || | | |(_)\/  | | .-'  | | _  \ \   (_) |   | .-'  |   (    
 | |`-' /| |\ \ | |  |)|| `-')|| \  / | |  `--.| |( `-'  )    | |   |  `--.| |\ \   
 /( `--' |_| \)\|_|  (_)`---(_)| |\/| | /( __.'`-' `----'     `-'   /( __.'|_| \)\  
(__)         (__)              '-'  '-'(__)                        (__)        (__) 
```

`braumeister` is a release-candidate preparation tool for git and JIRA users. 
Given a fix-version, it gathers git branches mentioned in JIRA issues targetting this fix-version and merges them in a release-candidate branch.

# Installation
**The `braumeister` requires at least Python `3.5`**

Install with:
```sh
pip3 install braumeister
```

# Configuration
You can initialize the `braumeister` inside the root directory of a git repository like this:
```sh
braumeister init
```

The `braumeister` will create a `.braumeister` configuration file in the current directory. The configuration may look like this:

```ini
[general]
verbose = false

[jira]
url = https://jira.dev
username = my-user
password = secret
destination_transition = Merged
branch_custom_field_id = customfield_5711
```

|Section|key|default value|description|
|-------|---|-----|---|
|general|verbose|false|Verbose output|
|jira|url|None|JIRA Base URL|
|jira|username|None|A JIRA User|
|jira|password|None|The password for the user|
|jira|destination_transition|None|Workflow Transition name for the ticket after merging, if executed with `-u`|
|jira|branch_custom_field_id|None|The JIRA Custom Field where we should read the branch from|

We'll be looking for a configuration file at the following places
```
[CURRENT-DIRECTORY]/.braumeister
~/.braumeister
```

**It's recommended to add the following files to your `.gitignore`**
```gitignore
.braumeister
release_state.json
```

## JIRA Configuration
### Custom Field für Branch anlegen
In JIRA, press `gg` (or `.`) to open the "Quick Actions" > Type `Custom Fields` > `Add custom field` > `Text field (single line)` > `Next`
```
Name: Branch
Description: git Branch
```
In the next screen, you need to assign the created field to one or more screens.
The `branch_custom_field_id` is `customfield_[ID]` whereas the `ID` is the number in the URL behind the `customFieldId=`.
e.g.:
```none
https://jira.dev/secure/admin/ConfigureCustomField!default.jspa?customFieldId=57111
```
Here, the JIRA Custom Field Id is `5711`, so the `braumeister` configuration for `branch_custom_field_id` would be `customfield_5711`.

# Description
The `braumeister` requests all issues from JIRA with the given release name as `Fix Version`.
In theses tickets, we'll search for the configured custom field (eg Branch) containing the git branch.
The release branch will be created like this:
```
release/[cleaned_release_name]_RC_[LATEST_RC + 1]
```
If the `braumeister` discovered a branch with the same name, we'll increase the `RC` part with 1 (with leading zeros). The first release branch will have the RC `001`.

For each of theses branches, the following commands will be executed:
```sh
$ git checkout $branch
$ git pull
$ git merge origin/master
$ git push origin $branch
$ git checkout $release_branch
$ git merge origin/$branch
$ git branch -D $branch
```

After merging all branches to the release branch, the branch will be pushed to `origin`.

## Conflicts
If there are any conflicts during the merge of a branch, the `braumeister` will stop and write the current state to a `release_state.json` file. The output may looks like this:
```sh
$ braumeister -v "Barking Dog" candidate
[*] Requesting all issues with fixVersion: Barking Dog
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5711
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5712
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5713
[+] The last branch for RC Barking Dog is:   release/Barking_Dog_RC_002
[+] Creating new branch 'release/Barking_Dog_RC_003' from master

Branch 'release/Barking_Dog_RC_003' set up to track remote branch 'master' from 'origin'.
Switched to a new branch 'release/Barking_Dog_RC_003'

[🍻 ] Merging feature-2...
[🍻 ] Branch 'feature-2' merged

[🍻 ] Merging feature-1...

Writing state json!

A merge error occured while merging feature into release/Barking_Dog_RC_003

Please do the following steps:
	* Resolve the conflicts
	* Commit the changes
	* Call the script again with the option -r
```

The `braumeister` will stay in the current release branch to let you resolve the conflict. After the conflict has been resolved, you can rerun the `braumeister` with `-r` to resume where we stopped.

```sh
$ braumeister -v "Barking Dog" -r candidate
Reading state json!
Resuming with feature-1
[🍻 ] Merging feature-1...
[🍻 ] Branch 'feature-1' merged

[🍻 ] Merging affe...
[🍻 ] Branch 'affe' merged

Deleting state json!

[🍻 ] All done. Grab a 🍺
```

## Examples

### Release Candidate

#### New release candidate
```sh
$ braumeister -v "Barking Dog" candidate
[*] Requesting all issues with fixVersion: Barking Dog
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5711
[+] Creating new branch 'release/Barking_Dog_RC_001' from master

Branch 'release/Barking_Dog_RC_001' set up to track remote branch 'master' from 'origin'.
Switched to a new branch 'release/Barking_Dog_RC_001'

[🍻 ] Merging affe...
[🍻 ] Branch 'affe' merged


[🍻 ] All done. Grab a 🍺
```

#### Existing release candidate
When you execute the `braumeister` with the same release name again, a new release candidate will be created (increasing the `RC` part with 1).

```sh
$ braumeister -v "Barking Dog" candidate
[*] Requesting all issues with fixVersion: Barking Dog
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5711
[+] The last branch for RC Barking Dog is: release/Barking_Dog_RC_001
[+] Creating new branch 'release/Barking_Dog_RC_002' from master

Branch 'release/Barking_Dog_RC_002' set up to track remote branch 'master' from 'origin'.
Switched to a new branch 'release/Barking_Dog_RC_002'

[🍻 ] Merging affe...
[🍻 ] Branch 'affe' merged


[🍻 ] All done. Grab a 🍺
```

#### Update JIRA issue
Executing the `braumeister` with `-u` will also execute the configured transition on all related issues.

```sh
$ braumeister -v "Barking Dog" -u candidate
[*] Requesting all issues with fixVersion: Barking Dog
[+] Requesting issue: https://jira.dev/rest/api/2/issue/31300
[+] Requesting issue: https://jira.dev/rest/api/2/issue/30209
[+] The last branch for RC Barking Dog is:   release/Barking_Dog_RC_004
[+] Creating new branch 'release/Barking_Dog_RC_005' from master

Branch 'release/Barking_Dog_RC_005' set up to track remote branch 'master' from 'origin'.
Switched to a new branch 'release/Barking_Dog_RC_005'

[🍻 ] Merging feature-1...
[🍻 ] Branch 'feature-1' merged

[🍻 ] Merging affe...
[🍻 ] Branch 'affe' merged

Deleting state json!
------------------------------------
[+] Update status to Merged on all related jira issues!
------------------------------------
Requesting all transitions for: DEV-1
Updating jira status on DEV-1 to Staging Needed
------------------------------------
Requesting all transitions for: DEV-2
Updating jira status on DEV-2 to Staging Needed

[🍻 ] All done. Grab a 🍺
```

### Release

#### New release
```sh
$ braumeister -v "Barking Dog" release
[*] Requesting all issues with fixVersion: Barking Dog
[+] Requesting issue: https://jira.dev/rest/api/2/issue/5711
[+] Creating new branch 'release/Barking_Dog_GA' from master

Branch 'release/Barking_Dog_GA' set up to track remote branch 'master' from 'origin'.
Switched to a new branch 'release/Barking_Dog_GA'

[🍻 ] Merging affe...
[🍻 ] Branch 'affe' merged

[🍻 ] All done. Grab a 🍺
```

#### Finalize a release
When you execute the `braumeister` with the `finalize` action it will merge the given branch back to `origin/master`. 

THIS CHANGES YOUR REMOTE REPOSITORY, HANDLE WITH CARE!

```sh
$ braumeister -v "Barking Dog" finalize
[+] Merging branch 'release/Barking_Dog_GA' to origin/master

[🍻 ] Merging release/Barking_Dog_GA...
[🍻 ] Branch 'release/Barking_Dog_GA' merged

[🍻 ] All done. Grab a 🍺
```

#### Cleanup after a release
When you execute the `braumeister` with the `cleanup` action it will delete all branches associated with tickets in your `fixVersion`.

THIS CHANGES YOUR REMOTE REPOSITORY, HANDLE WITH CARE!

```sh
$ braumeister -v "Barking Dog" cleanup
[+] Cleaning up after release of Barking Dog

[🍻 ] Deleting origin/feature-fifty...
[🍻 ] Deleting origin/feature-seven...
[🍻 ] Deleting origin/feature-eleven...

[🍻 ] Brewhouse all clean again. Grab a 🍺
```

# Development
Running tests
```sh
make test
```
