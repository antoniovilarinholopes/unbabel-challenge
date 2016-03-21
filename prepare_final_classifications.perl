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


my ($classifications, $sentences, $file) = @ARGV;

-e $classifications or die "Featureset_1 is necessary, please provide it.$!";
-e $sentences or die "Featureset_2 is necessary, please provide it.$!";



print STDERR "Reading all features\n";
my @classifications_arr = ();
my @sentences_arr = ();


open(DATASET, "<:encoding(UTF-8)" ,$classifications) or die "Could not open file $classifications. $!";
while(my $line = <DATASET>) {
  chomp($line);
  push(@classifications_arr, $line);
}
close DATASET;

open(DATASET, "<:encoding(UTF-8)" ,$sentences) or die "Could not open file $sentences. $!";
while(my $line = <DATASET>) {
  chomp($line);
  push(@sentences_arr, $line);
}
close DATASET;

######Write into a file##########
print STDERR "Writting classifications\n";

open(FEATSET, ">:encoding(UTF-8)" ,$file) or die "Could not open file $file. $!";
foreach my $i (0 .. $#classifications_arr) { print FEATSET "$classifications_arr[$i]       $sentences_arr[$i]"; print FEATSET "\n";}
close FEATSET;
########################################
