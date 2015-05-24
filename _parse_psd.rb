#!/usr/bin/env ruby
require 'rubygems'
require 'bundler/setup'
require 'psd'
require 'json'

PSD.open(ARGV[0]) do
  p tree.to_hash.to_json
end
