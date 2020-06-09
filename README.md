# zte config utility

The core of the decoding work is taken from a [pastebin](https://pastebin.com/GGxbngtK) dump by 'Felis-Sapien'.

Creates byte-perfect binaries for the limited cases that have been tested.

## Quickstart

Clone the repo and run `python3 setup.py install --user`.

## Examples

### Decode a `config.bin`
```sh
# Decode the `ZXHN H298N` config file:
$ python3 examples/decode.py resources/ZXHN_H298N.bin resources/ZXHN_H298N.xml --key 'Wj'
# check md5 of xml
$ md5sum resources/ZXHN_H298N.xml
02beac1e9450b29c08b2d45974386361  resources/ZXHN_H298N.xml
# check md5 of config file
md5sum resources/ZXHN_H298N.bin
8529c1e3d4e3018db508a3b5b5b574cc  resources/ZXHN_H298N.bin
```

### Encode a `config.xml`
```sh
# Encode the `ZXHN H298N` xml file:
$ python3 examples/encode.py resources/ZXHN_H298N.xml resources/ZXHN_H298N.NEW.bin --key 'Wj' --signature 'ZXHN H298N'
# check md5 of new config file
md5sum resources/ZXHN_H298N.NEW.bin
8529c1e3d4e3018db508a3b5b5b574cc  resources/ZXHN_H298N.NEW.bin
```

### Grab 'signature' from a `config.bin`

```sh
$ python3 examples/signature.py resources/ZXHN_H108N_V2.5.bin
ZXHN H108N V2.5
```

## Limitations

The decoder has only been tested against `config.bin` files generated by the following routers:
 - `ZXHN H298N`
 - `ZXHN H108N V2.5`
 - `F600W`

It makes a number of assumptions due to this. The encoder has not been tested in the wild. Use at your own risk.