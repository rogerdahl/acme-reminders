#!/usr/bin/env python

"""Add a new notification using the HTTP POST interface.
"""

import argparse
import logging
import requests

DEBUG = False

# noinspection PyArgumentList
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(levelname)-8s %(message)s",
    force=True,
)
log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("msg")
    args = parser.parse_args()

    form_dict ={'msg': args.msg}
    response = requests.post('http://192.168.1.154:5050/add', data=form_dict)
    log.info(response.text)


if __name__ == "__main__":
    main()
