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

#my $pos_tagger_location = "/afs/l2f/home/alopes/Downloads/stanford-postagger-full-2015-12-09";
my $dataset_tmp_mt = "$root_outdir/mt_dataset_tmp.txt";
#print STDERR "POS tagging mt_dataset\n";
#`java -mx1024m -cp \"$pos_tagger_location/stanford-postagger-3.6.0.jar:$pos_tagger_location/lib/*\" edu.stanford.nlp.tagger.maxent.MaxentTagger -model $pos_tagger_location/models/spanish-distsim.tagger -sentenceDelimiter newline -textFile $dataset_mt  > $dataset_tmp_mt`;


my $dataset_tmp_h = "$root_outdir/h_dataset_tmp.txt";
#print STDERR "POS tagging h_dataset\n";
#`java -mx1024m -cp \"$pos_tagger_location/stanford-postagger-3.6.0.jar:$pos_tagger_location/lib/*\" edu.stanford.nlp.tagger.maxent.MaxentTagger -model $pos_tagger_location/models/spanish-distsim.tagger -sentenceDelimiter newline -textFile $dataset_h  > $dataset_tmp_h`;
##########################################


############POS EXTRACT FOR LM###########
#TODO Should the extraction of the sentence length done here? I mean, the size of the tokes is the size of the sentence :)

print STDERR "Reading tagged sentences of mt dataset\n";
open(MT_DATASET_POS, "<:encoding(UTF-8)" ,$dataset_tmp_mt) or die "Could not open file $dataset_tmp_mt. $!";
my @tagged_mt_sentences = ();
while(my $line = <MT_DATASET_POS>) { chomp($line); push(@tagged_mt_sentences, $line); }
close MT_DATASET_POS;

print STDERR "Writting taggs of mt dataset\n";
my $dataset_pos_mt = "$root_outdir/mt_dataset_pos.txt";
open(MT_DATASET_POS_ONLY, ">:encoding(UTF-8)" ,$dataset_pos_mt) or die "Could not open file $dataset_pos_mt. $!";
foreach my $mt (@tagged_mt_sentences) { my @tags = (); retrieve_tags_from_tagged_text($mt,\@tags); print MT_DATASET_POS_ONLY join(" ",@tags); print MT_DATASET_POS_ONLY "\n";}
close MT_DATASET_POS_ONLY;

print STDERR "Reading tagged sentences of h dataset\n";
open(H_DATASET_POS, "<:encoding(UTF-8)" ,$dataset_tmp_h) or die "Could not open file $dataset_tmp_mt. $!";
my @tagged_h_sentences = ();
while(my $line = <H_DATASET_POS>) { chomp($line); push(@tagged_h_sentences, $line); }
close H_DATASET_POS;

print STDERR "Writting taggs of h dataset\n";
my $dataset_pos_h = "$root_outdir/h_dataset_pos.txt";
open(H_DATASET_POS_ONLY, ">:encoding(UTF-8)" ,$dataset_pos_h) or die "Could not open file $dataset_pos_h. $!";
foreach my $h (@tagged_h_sentences) { my @tags = (); retrieve_tags_from_tagged_text($h,\@tags); print H_DATASET_POS_ONLY join(" ",@tags); print H_DATASET_POS_ONLY "\n";}
close H_DATASET_POS_ONLY;
##########################################

##########TRAIN LM'S######################
#TODO Do this parallel!!! DIVIDE IN TRAIN AND TEST! MAYBE DO IN PYTHON?
`time ./rnnlm -train $dataset_pos_mt -valid $dataset_pos_mt -rnnlm model_pos -hidden 50 -rand-seed 1 -debug 2 -bptt 4 -bptt-block 10 -direct-order 3 -direct 2 -binary`
`time ./rnnlm -train $dataset_pos_h -valid $dataset_pos_h -rnnlm model_pos -hidden 50 -rand-seed 1 -debug 2 -bptt 4 -bptt-block 10 -direct-order 3 -direct 2 -binary`

`ngram-count -text $dataset_pos_mt -order 5 -lm templm_pos_mt -kndiscount -interpolate -gt3min 1 -gt4min 1`
`ngram -lm templm_pos_mt -order 5 -ppl test -debug 2 > temp_pos_mt.ppl`
`ngram-count -text $dataset_pos_h -order 5 -lm templm_pos_h -kndiscount -interpolate -gt3min 1 -gt4min 1`
`ngram -lm templm_pos_h -order 5 -ppl test -debug 2 > temp_pos_h.ppl`


`time ./rnnlm -train $dataset_mt -valid $dataset_mt -rnnlm model_pos -hidden 50 -rand-seed 1 -debug 2 -bptt 4 -bptt-block 10 -direct-order 3 -direct 2 -binary`
`time ./rnnlm -train $dataset_h -valid $dataset_h -rnnlm model_pos -hidden 50 -rand-seed 1 -debug 2 -bptt 4 -bptt-block 10 -direct-order 3 -direct 2 -binary`
`ngram-count -text $dataset_mt -order 5 -lm templm_mt -kndiscount -interpolate -gt3min 1 -gt4min 1`
`ngram -lm templm_mt -order 5 -ppl test -debug 2 > temp_mt.ppl`
`ngram-count -text $dataset_h -order 5 -lm templm_h -kndiscount -interpolate -gt3min 1 -gt4min 1`
`ngram -lm templm_h -order 5 -ppl test -debug 2 > temp_h.ppl`
##########################################



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

