# Incidr

Groups of IP addresses can be defined by ["cidr blocks"](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing), but looking at a block, it can be difficult to determine whether blocks contain each other or not.

This tool is supposed to assist with that.

## Usage

The tool takes a list of cidr blocks as input, parses them and outputs which blocks are inside which.

```sh
echo 172.128.0.0/15 172.128.0.0/16 172.129.0.0/17 | python ./incidr

# 172.128.0.0/15        
#         172.128.0.0/16
#         172.129.0.0/17
```
