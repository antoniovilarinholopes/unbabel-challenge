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


my ($dataset) = @ARGV;

my $outdir = "blind_test_dataset";

`mkdir -p $outdir`;

-e $dataset or die "Dataset is necessary, please provide it.$!";

####POS################

my $pos_tagger_location = "/afs/l2f/home/alopes/Downloads/stanford-postagger-full-2015-12-09";

my $dataset_tmp = "$outdir/test_dataset_tmp.txt";
print STDERR "POS tagging dataset $dataset\n";
`java -mx1024m -cp \"$pos_tagger_location/stanford-postagger-3.6.0.jar:$pos_tagger_location/lib/*\" edu.stanford.nlp.tagger.maxent.MaxentTagger -model $pos_tagger_location/models/spanish-distsim.tagger -sentenceDelimiter newline -textFile $dataset  > $dataset_tmp`;

#########################################


############POS EXTRACT FOR LM###########
#TODO Should the extraction of the sentence length done here? I mean, the size of the tokes is the size of the sentence :)

print STDERR "Reading tagged sentences of test dataset\n";
open(DATASET_POS, "<:encoding(UTF-8)" ,$dataset_tmp) or die "Could not open file $dataset_tmp. $!";
my @tagged_sentences = ();
while(my $line = <DATASET_POS>) { chomp($line); push(@tagged_sentences, $line); }
close DATASET_POS;

print STDERR "Writting taggs of test dataset\n";
my $dataset_pos = "$outdir/test_dataset_pos.txt";
open(DATASET_POS_ONLY, ">:encoding(UTF-8)" ,$dataset_pos) or die "Could not open file $dataset_pos. $!";
foreach my $line (@tagged_sentences) { my @tags = (); retrieve_tags_from_tagged_text($line,\@tags); print DATASET_POS_ONLY join(" ",@tags); print DATASET_POS_ONLY "\n";}
close DATASET_POS_ONLY;
#########################################


sub retrieve_tags_from_tagged_text {
    my ($tagged_text, $tags) = (shift,  shift);

    $tagged_text =~ s/\n/ /g;
    my @tagged_tokens = split(/ /, $tagged_text);

    foreach my $tagged_token (@tagged_tokens) {
      my ($token, $tag) = split(/_/, $tagged_token);
#      push(@{$text}, $token);
      push(@{$tags}, $tag);
    }
}

