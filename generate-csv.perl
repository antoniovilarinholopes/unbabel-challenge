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


my ($featset_1, $class_1, $featset_2, $class_2, $out_dir) = @ARGV;

-e $featset_1 or die "Featureset_1 is necessary, please provide it.$!";
-e $featset_2 or die "Featureset_2 is necessary, please provide it.$!";
die "Please provide the classes and they must be different" unless (defined $class_1 and defined $class_2 and $class_1 != $class_2);



print STDERR "Reading all features\n";
my @feat_set_1 = ();
my @feat_set_2 = ();


open(DATASET, "<:encoding(UTF-8)" ,$featset_1) or die "Could not open file $featset_1. $!";
while(my $line = <DATASET>) {
  chomp($line);
  push(@feat_set_1, $line);
}
close DATASET;

open(DATASET, "<:encoding(UTF-8)" ,$featset_2) or die "Could not open file $featset_2. $!";
while(my $line = <DATASET>) {
  chomp($line);
  push(@feat_set_2, $line);
}
close DATASET;

######Write into a file##########
print STDERR "Writting total featset\n";
my $feat_file = "$out_dir/features.csv";

open(FEATSET, ">:encoding(UTF-8)" ,$feat_file) or die "Could not open file $feat_file. $!";
my $header = shift(@feat_set_1);
my $header_2 = shift(@feat_set_2);
print "Headers not equal $header : $header_2\n" if($header ne $header_2);
print FEATSET "$header, class";
print FEATSET "\n";
foreach my $line (@feat_set_1) { print FEATSET "$line,$class_1"; print FEATSET "\n";}
foreach my $line (@feat_set_1) { print FEATSET "$line,$class_2"; print FEATSET "\n";}
close FEATSET;
########################################
