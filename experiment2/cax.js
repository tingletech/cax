#!/usr/bin/env node

var fs = require("fs");
var libxmljs = require("libxmljs");
var crypto = require("crypto");
var xmldom = require("xmldom");
var c14n = require("xml-c14n")();

file = process.argv[2];

var xml_id = function(string) {
  var doc = libxmljs.parseXml(string, { noblanks: true })
  var string_noblanks = doc.root().toString();
  var doc = (new xmldom.DOMParser()).parseFromString(string_noblanks);
  var canonicaliser = c14n.createCanonicaliser("http://www.w3.org/2001/10/xml-exc-c14n#WithComments");
  canonicaliser.canonicalise(doc.documentElement, function(err, res) {
    digest = crypto.createHash('sha256').update(res).digest('hex');
    console.log(digest);
  });
}

fs.readFile(file, "utf-8", function(err, data) {
  if (err) {
    return console.warn(err.stack);
  }
  xml_id(data);
});

