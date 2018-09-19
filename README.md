This client is for domain owners hoping to perform ddns for their aliyun domains. Writen in python 2.7.

## Limitations
This version of DDNS client only supports updating 'A' type dns record with IPv4.

## Prerequisite
Some 3rd party python libraries are required, you can install them via pip:
- aliyun-python-sdk-core
- aliyun-python-sdk-alidns

For example:

``` bash
$(sudo) pip install aliyun-python-sdk-core
$(sudo) pip install aliyun-python-sdk-alidns
```

## Usage
This client tries to set local public ip address to target dns records specified in a configuration file via `--config` option or directly via `--domains` option. See the example below:

```bash
$ (sudo) python ddns.py --config ddns.conf
```
or
```bash
$ (sudo) python ddns.py --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```
Specify multiple sub domains by white space in the cli. You can find a sample `.conf` file [here](https://github.com/BerdyPango/ddns-client-aliyun/blob/master/config-samples/ddns.conf.sample), it looks like:
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
Once you run the client through it will exit immediately, if you want to run it regularly, append a crontab job on *NIX or task scheduler on Windows.

## Roadmap
- Create a docker image for the script and put it into another repository
- Support creation if not found target dns record and make it configurable
- Compatibility with python3