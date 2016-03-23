#!/usr/bin/perl -w

use strict;
use encoding 'utf8';
use constant;
use Data::Dumper;
use Unicode::Normalize;
use POSIX;
use File::Basename;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

my @classifications_arr = ();
open(DATASET, "<:encoding(UTF-8)" ,"real_tags") or die "Could not open file. $!";
while(my $line = <DATASET>) {
  chomp($line);
  push(@classifications_arr, $line);
}
close DATASET;

foreach (@classifications_arr) {print $_; print "\n";}

