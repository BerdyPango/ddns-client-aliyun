For those who host their websites at home server, exposing their sites to external internet via a domain name registered from Aliyun. It's been annoying that they need to manually update the dns record whenever the ISP changed their home public IP address. This utility is built for those who:
- Expect a lightweight tool running regularly to automate the process
- Do not want to register their real name at 3rd party ddns provider like [Oray](https://hsk.oray.com/) merely to get a ddns service with a given subdomain.
- Have suffered the terrible network connection with the free of charge ddns providers outside mainland China.

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
First, you need to get the following things ready:
- Your domain name registered at Aliyun.
- Your Aliyun domain resolution API access id and key.

Then, clone this repo into your home server or local machine:
```bash
$ git clone https://github.com/BerdyPango/ddns-client-aliyun.git
$ cd ddns-client-aliyun
```
The client can be configured either with an `--config` option specifying the path to the configuration file or directly populating the values of each option through cli.

### Populate option values through cli
```bash
$ (sudo) python ddns.py --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```
Available options listed below, they are:
- `domains`: Full domain name to be deteced and updated. Multiple sub domains are supported by giving white space in between. **Required**
- `access-key-id`: Assigned from Aliyun. **Required**
- `access-key-secret`: Assigned from Aliyun. **Required**
- `type`: Type of dns resolution records, default value is 'A' and only support 'A' for now. **Optional**

### Split options into a dedicated configuration file
You can find a sample `.conf` file [here](https://github.com/BerdyPango/ddns-client-aliyun/blob/master/config-samples/ddns.conf.sample). It might look like:
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
You can copy from the default config file or name a config file, remember to specify the `--config` option:
```bash
$ (sudo) cp ./config-samples/ddns.conf.sample ./ddns.conf
$ (sudo) python ddns.py --config ddns.conf
```

## Docker Support
If you prefer the Docker way. You could find the docker image at [Docker Hub](https://hub.docker.com/r/frosthe/ddns-client-aliyun). Just simply pull it to your home server or local machine:
```
$ (sudo) docker pull frosthe/ddns-client-aliyun
```
Run the docker image with same options like the client:
```bash
$ (sudo) docker run frosthe/ddns-client-aliyun --config ./ddns.conf
```
or
```bash
$ (sudo) docker run frosthe/ddns-client-aliyun --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```

The client will exit immediately after running through. If you want to run it regularly, append a crontab job on *NIX or a task scheduler job on Windows. For example, we could restart the docker container every 10 seconds:
```bash
$ crontab -e

* * * * * (docker container restart ddns-client-aliyun)
* * * * * (sleep 10; docker container restart ddns-client-aliyun)
* * * * * (sleep 20; docker container restart ddns-client-aliyun)
* * * * * (sleep 30; docker container restart ddns-client-aliyun)
* * * * * (sleep 40; docker container restart ddns-client-aliyun)
* * * * * (sleep 50; docker container restart ddns-client-aliyun)
```