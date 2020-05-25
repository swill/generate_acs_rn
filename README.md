USAGE
=====

Requires Python 2.7.11+ (not compatible with Python3)

`api_changes.py`
----------------

```bash
$ ./api_changes.py -h
Usage:
  api_changes.py <diff.json>
  api_changes.py (-h | --help)
Options:
  -h --help                 Show this screen.
  --col_name_width=<arg>    The width of the Name column [default: 45].
  --col_desc_width=<arg>    The width of the Description column [default: 80].
```

This project piggybacks off the work that Pierre-Luc Dion has done here: https://github.com/pdion891/acs-api-commands

The `diff` file produced by following the README in `acs-api-commands` is used by the `api_changes.py` script to generate the RST formatted differences between two versions of ACS.  Follow the directions in the `acs-api-commands` repository to generate a `diff-<old>-<new>/diff.json` file for the versions you would like to generate the documentation for.  Once you have the `diff-<old>-<new>/diff.json` file generated, follow these steps.

```bash
$ ./api_changes.py /path/to/acs-api-commands/diff-<old>-<new>/diff.json > ~/api-changes-partial.rst
```

Now update the `cloudstack-documentation/source/releasenotes/api-changes.rst` file with the respective sections output from the `~/api-changes-partial.rst` file.

This will product documentation like this: [ACS 4.14.0.0 Release Notes | API Changes](http://docs.cloudstack.apache.org/en/4.14.0.0/releasenotes/api-changes.html)


`fixed_issues.py`
-----------------

```bash
$ ./fixed_issues.py -h
Usage:
  fixed_issues.py [--config=<config.json>]
                  [-t <arg> | --gh_token=<arg>]
                  [-c <arg> | --prev_rel_commit=<arg>]
                  [-b <arg> | --branch=<arg>]
                  [--repo=<arg>]
                  [--gh_base_url=<arg>]
                  [--jira_base_url=<arg>]
                  [--jira_server_url=<arg>]
                  [--col_branch_width=<arg>]
                  [--col_github_width=<arg>]
                  [--col_jira_width=<arg>]
                  [--col_type_width=<arg>]
                  [--col_priority_width=<arg>]
                  [--col_desc_width=<arg>]
  fixed_issues.py (-h | --help)
Options:
  -h --help                         Show this screen.
  --config=<config.json>            Path to a JSON config file with an object of config options.
  -t <arg> --gh_token=<arg>         Required: Your Github token from https://github.com/settings/tokens
                                      with `repo/public_repo` permissions.
  -c <arg> --prev_rel_commit=<arg>  Required: The commit hash of the previous release.
  -b <arg> --branches=<arg>         Required: Comma separated list of branches to report on (eg: 4.7,4.8,4.9).
                                      The last one is assumed to be `master`, so `4.7,4.8,4.9` would
                                      actually be represented by 4.7, 4.8 and master.
  --repo=<arg>                      The name of the repo to use [default: apache/cloudstack].
  --gh_base_url=<arg>               The base Github URL for pull requests
                                      [default: https://github.com/apache/cloudstack/pull/].
  --jira_base_url=<arg>             The base Jira URL for issues
                                      [default: https://issues.apache.org/jira/browse/].
  --jira_server_url=<arg>           The Jira server URL [default: https://issues.apache.org/jira].
  --col_branch_width=<arg>          The width of the Branches column [default: 25].
  --col_github_width=<arg>          The width of the Github PR column [default: 10].
  --col_jira_width=<arg>            The width of the Jira Issue column [default: 20].
  --col_type_width=<arg>            The width of the Issue Type column [default: 15].
  --col_priority_width=<arg>        The width of the Issue Priority column [default: 10].
  --col_desc_width=<arg>            The width of the Description column [default: 60].

Sample json file contents:

{
    "--gh_token":"******************",
    "--prev_release_commit":"",
    "--repo_name":"apache/cloudstack",
    "--branch":"4.11",
    "--prev_release_ver":"4.11.1.0",
    "--new_release_ver":"4.11.2.0"
}

Example:

     # python fixed_issues.py --config=config.json
```

Don't worry too much about the shear number of usage options for `fixed_issues.py`.  There are sane defaults for the majority of the options, so there are only a few you need to care about.  While specifying a `--config` file is not required, I tend to use it to define the majority of the configuration which I have to specify values for.  I do this because it makes it easier for me to come back and pick up where I left off without having to figure out what configuration I was using in the past.

Here are the key configuration items you need to care about.

If the 'prev_release_commit' is defined, it overrides the 'prev_release_ver', otherwise the 'prev_release_commit' will be found out from the prev_release_ver (which is the git tag of the previous release). Keep in mind that if, for the previous release, the voted RC branch was not merged back to the main/master branch (by mistake), the commit ID of the git tag will be missing in the queried branch and you will have to manually find the correct last commit of the previous release.

**`config.json`**
```json
{
	"--gh_token":"your_github_token from https://github.com/settings/tokens with `repo/public_repo` permissions",
        "--prev_release_commit":"commit hash of the previous release, overrides \"prev_release_ver\" ",
        "--repo_name":"apache/cloudstack",
        "--branch":"we are querying this branch for the list of commits",
        "--prev_release_ver":"tag linked to the commit hash of the previous release, overriden by \"prev_release_commit\" if defined",
        "--new_release_ver":"Will be added as value in the version column in the output .rst file -i.e. \"4.14.0.0\""
}
```

For example, here is what was used for the 4.14 release - a custom commit hash was defined instead of the one that was voted, since the voted commit hash didn't exist in any branch as the RC branch was not merged back to the Master branch during 4.13 release (by mistake). 

```json
{
        "--gh_token":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "--prev_release_commit":"87c43501608a1df72a2f01ed17a522233e6617b0",
        "--repo_name":"apache/cloudstack",
        "--branch":"4.14",
        "--prev_release_ver":"4.13.0.0",
        "--new_release_ver":"4.14.0.0"
}```

Now run the `fixed_issues.py` script with that config.
```bash
$ python fixed_issues.py --config=config.json
```
Output will be written to the `config.rst.txt` file in the running folder.

A lot happens in the running of this script, so make sure the formatting is correct and there are no errors.

Now update the `cloudstack-documentation/source/releasenotes/changes.rst` file with the respective sections output from the `config.rst.txt` file.

This will product documentation like this: [ACS 4.14.0.0 Release Notes | Changes](http://docs.cloudstack.apache.org/en/4.13.1.0/releasenotes/changes.html)


DEPENDENCIES
============

`api_changes.py`
----------------

```bash
$ pip install docopt
```


`fixed_issues.py`
-----------------

```bash
$ pip install docopt
$ pip install PyGithub
$ pip install jira
```

