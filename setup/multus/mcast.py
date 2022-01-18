#!/usr/bin/env python

## AoB: requires python3

import socket
import struct
import fire
from datetime import datetime

class Mcast:

    @staticmethod
    def listen(mcast_grp, mcast_port, is_all_groups=False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if is_all_groups:
            # on this port, receives ALL multicast groups
            sock.bind(('', mcast_port))
        else:
            # on this port, listen ONLY to MCAST_GRP
            sock.bind((mcast_grp, mcast_port))
        mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print("Mcast.listen is listenning on {}:{}  {}".format(mcast_grp, mcast_port, ("Single", "ALL")[is_all_groups]))
        while True:
            data, address = sock.recvfrom(10240)
            # text = '@ {}'.format(datetime.now())
            text = "[RECEIVED]: {} [FROM]: {} @ [{}] ".format(data.decode("utf-8", "ignore"), address, datetime.now())
            print(text)
            # sock.settimeout(3) ## timeout is irrelevant in sending..
            sock.sendto(text.encode("utf-8"), address)

    @staticmethod
    def send(mcast_grp, mcast_port, message='Hello, Multicast!\n', multicast_ttl=32):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, multicast_ttl)
        sock.settimeout(3)
        sock.sendto(message.encode("utf-8"), (mcast_grp, mcast_port))
        data = None
        address = None
        try:
            data, address = sock.recvfrom(10240)
        except socket.error:
            data = None
        finally:
            sock.close()
        if data is not None:
            data_text = data.decode("utf-8", "ignore")
            text = "<RECEIVED>: {} bytes <FROM>: {} <@> <{}>. <Data>: {}".format(len(data), address, datetime.now(), data_text)
            print(text)
        else:
            print("Timeout reached and no data is returned back..")


if __name__ == '__main__':
    fire.Fire(Mcast)

