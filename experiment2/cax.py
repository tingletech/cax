#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
import sys
import argparse
import os
import logging
import time
from lxml import etree
import hashlib


def main(argv=None):
    _loglevel_ = 'WARNING'
    parser = argparse.ArgumentParser(description='migrate nuxeo data to s3')
    parser.add_argument('--file', required=True)
    parser.add_argument(
        '--loglevel',
        default=_loglevel_,
        help=''.join([
            'CRITICAL ERROR WARNING INFO DEBUG NOTSET, default is ',
            _loglevel_
        ])
    )

    if argv is None:
        argv = parser.parse_args()

    # set debugging level
    numeric_level = getattr(logging, argv.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % argv.loglevel)
    logging.basicConfig(level=numeric_level, )
    logger = logging.getLogger(__name__)

    root = etree.parse(
        argv.file,
        # etree.XMLParser(remove_blank_text=True)
    ).getroot()

    string = etree.tostring(root)

    print(xml_id(string))


def xml_id(string):
    reparse = etree.fromstring(string, etree.XMLParser(remove_blank_text=True))
    string_to_hash = etree.tostring(reparse, method='c14n',exclusive=True)
    #string_to_hash = etree.tostring(reparse, method='xml',)
    digest = hashlib.sha256(string_to_hash).hexdigest()
    return digest


# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())


"""
Copyright © 2015, Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
