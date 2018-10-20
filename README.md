This client is for domain owners hoping to perform ddns to their domains registered in aliyun. Writen in python 2.7.

## Limitations
This version of DDNS client only supports updating 'A' type dns record with IPv4.

## Prerequisites
3rd party python libraries are required, you can install them via pip:
``` bash
$(sudo) pip install requests
$(sudo) pip install aliyun-python-sdk-core
$(sudo) pip install aliyun-python-sdk-alidns
```

## Usage
Specify domain configuration and aliyun access credentials via `--config` option or `--domains` option. See the example below:

```bash
$ (sudo) python ddns.py --config ddns.conf
```
or
```bash
$ (sudo) python ddns.py --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```
Multiple sub domains are supported by white space. You can find a sample `.conf` file [here](https://github.com/BerdyPango/ddns-client-aliyun/blob/master/config-samples/ddns.conf.sample). It might look like:
```
[DEFAULT]

[ApiProvider]
# access_key_id and access_key_secret acquired from dns provider
access_key_id = 1234567890
access_key_secret = 0987654321

# Dns records to update, specify multiple sub domians with ','
[DomainNameToUpdate1]
domain = example.com
sub_domain = www, api
type = A

[DomainNameToUpdate2]
domain = example2.com
sub_domain = cloud, home
type = A
```
The client will exit immediately after running through. If you want to run it regularly, append a crontab job on *NIX or a task scheduler job on Windows.

## Roadmap
- [Done]Create a docker image for the script and put it into another repository. You could find the docker image repo [here](https://github.com/BerdyPango/ddns-client-aliyun-docker)
- Support creation if not found target dns record.
- Compatibility with python3.