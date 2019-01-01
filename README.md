## Scenarios
For those who host their websites at home server, expecting access to the sites from external internet, it's been annoying that they need to manually update the dns record once the ISP re-assign their home public IP address. 

## Why should I use a ddns client rather than a ddns provider?
If you:
- Expect a lightweight tool running regularly to perform ddns.
- Expect a custom domain name instead of a given sub domain from ddns providers.
- Do not want to provide ddns providers with your real information merely to get a ddns service.
- Have suffered the terrible network connection with the free of charge ddns providers outside mainland China.

## Limitations
This version of DDNS client only supports updating 'A' type dns record with IPv4.

## Usage
First, you need to get ready some key information:
- The domain name registered at Aliyun.
- The API key assigned by Aliyun to manage your dns records programmatically.

Clone this repo into your home server or local machine:
```bash
$ git clone https://github.com/BerdyPango/ddns-client-aliyun.git
$ cd ddns-client-aliyun
$ pip install -r requirements.txt
```
The client can be configured either with an `--config` option specifying the path to the configuration file or directly populating the values of each option through cli.

### Populate option values through cli
```bash
$ (sudo) python ddns.py --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```
Available options are listed below:
- `domains`: [Required]Full domain name to be detected and updated. Multiple sub domains are supported by giving white space in between. 
- `access-key-id`: [Required]Assigned from Aliyun. 
- `access-key-secret`: [Required]Assigned from Aliyun. 
- `type`: [Optional]Type of dns resolution records, default value is 'A' and it only supports 'A' for now.

### Split options into a dedicated configuration file
You could find a sample `.conf` file [here](https://github.com/BerdyPango/ddns-client-aliyun/blob/master/config-samples/ddns.conf.sample). It might look like:
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
Copy from the default config file from `config-samples/ddns.conf.sample` or create a new one, remember to specify the `--config` option:
```bash
$ (sudo) cp ./config-samples/ddns.conf.sample ./ddns.conf

$ (sudo) python ddns.py --config ddns.conf
```

## Automation
Create a crontab job to run the client every 5 min:
```bash
*/5 * * * * cd /home/pi/apps/ddns-client-aliyun && /usr/bin/python ./ddns.py --config ./ddns.conf >> ./logs/log.txt 2>&1
```

## Docker Support
If you prefer the Docker way. You could find the docker image at [Docker Hub](https://hub.docker.com/r/frosthe/ddns-client-aliyun). Currently it only supports amd64 CPUs. 

Simply pull the image into your home server or local machine:
```
$ (sudo) docker pull frosthe/ddns-client-aliyun
```
Run the docker image with same options like described above:
```bash
$ (sudo) docker run frosthe/ddns-client-aliyun --config ./ddns.conf
```
or
```bash
$ (sudo) docker run --rm frosthe/ddns-client-aliyun --domains www.example.com --access-key-id XXXXXXXXX --access-key-secret XXXXXXXXXXXXX
```

The program will exit immediately after running through. If you want to run it regularly, append a crontab job on *NIX or a task scheduler job on Windows. For example, we could restart the docker container every 10 seconds:
```bash
$ crontab -e

* * * * * (docker container restart ddns-client-aliyun)
* * * * * (sleep 10; docker container restart ddns-client-aliyun)
* * * * * (sleep 20; docker container restart ddns-client-aliyun)
* * * * * (sleep 30; docker container restart ddns-client-aliyun)
* * * * * (sleep 40; docker container restart ddns-client-aliyun)
* * * * * (sleep 50; docker container restart ddns-client-aliyun)
```