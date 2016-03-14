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


my ($dataset, $root_dir) = @ARGV;

my $_outdir = "processed_dataset";
my $root_outdir = $_outdir;
$root_outdir = "$root_dir/$_outdir" if(defined $root_dir);

-e $dataset or die "Dataset is necessary, please provide it.$!";

`mkdir -p $root_outdir`;

print STDERR "Reading all sentences\n";
my @mt_set = ();
my @h_set = ();


open(DATASET, "<:encoding(UTF-8)" ,$dataset) or die "Could not open file $dataset. $!";
while(my $line = <DATASET>) {
  chomp($line);
  if( $line =~ m/^0/) {
    $line =~ s/^0[ \r\t]*//g; 
    push(@mt_set, $line)
  } else {
    $line =~ s/^1[ \r\t]*//g; 
    push(@h_set, $line);
  }
}
close DATASET;

######Write into each separate file##########3
print STDERR "Writting mt dataset\n";
my $dataset_mt = "$root_outdir/mt_dataset.txt";
open(MT_DATASET, ">:encoding(UTF-8)" ,$dataset_mt) or die "Could not open file $dataset_mt. $!";
foreach my $mt (@mt_set) { print MT_DATASET $mt; print MT_DATASET "\n";}
close MT_DATASET;

print STDERR "Writting h dataset\n";
my $dataset_h = "$root_outdir/h_dataset.txt";
open(H_DATASET, ">:encoding(UTF-8)" ,$dataset_h) or die "Could not open file $dataset_h. $!";
foreach my $h (@h_set) { print H_DATASET $h; print H_DATASET "\n";}
close H_DATASET;
#########################################

####POS################

my $pos_tagger_location = "/afs/l2f/home/alopes/Downloads/stanford-postagger-full-2015-12-09";
my $dataset_tmp_mt = "$root_outdir/mt_dataset_tmp.txt";
print STDERR "POS tagging mt_dataset\n";
`java -mx1024m -cp \"$pos_tagger_location/stanford-postagger-3.6.0.jar:$pos_tagger_location/lib/*\" edu.stanford.nlp.tagger.maxent.MaxentTagger -model $pos_tagger_location/models/spanish-distsim.tagger -textFile $dataset_mt  > $dataset_tmp_mt`;


my $dataset_tmp_h = "$root_outdir/h_dataset_tmp.txt";
print STDERR "POS tagging h_dataset\n";
`java -mx1024m -cp \"$pos_tagger_location/stanford-postagger-3.6.0.jar:$pos_tagger_location/lib/*\" edu.stanford.nlp.tagger.maxent.MaxentTagger -model $pos_tagger_location/models/spanish-distsim.tagger -textFile $dataset_h  > $dataset_tmp_h`;
##########################################

sub retrieve_text_and_tags_from_tagged_text {
    my ($tagged_text, $text, $tags) = (shift, shift, shift);

    $tagged_text =~ s/\n/ /g;
    my @tagged_tokens = split(/ /, $tagged_text);

    foreach my $tagged_token (@tagged_tokens) {
      my ($token, $tag) = split(/_/, $tagged_token);
      push(@{$text}, $token);
      push(@{$tags}, $tag);
    }
}

