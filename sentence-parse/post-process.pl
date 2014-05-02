#! /usr/bin/perl
use strict;
use warnings;

if (@ARGV != 2) {
     print "usage: perl extract-treebank.pl INFILE OUTFILE\n";
     exit;
}

my $line;
my @words;
my @stack;
my @brackets;

open(INFILE, $ARGV[0]) || die;
open(OUTFILE, ">", $ARGV[1]) || die;

while ($line = <INFILE>) {
    if ($line =~ /No parse/) {
	$line = "(TOP nil)\n";
    }
    else {
	$line =~ s/\\([^\/])/$1/g;
	$line =~ s/\(([A-Z`\',:\.\-\$\#]+)-[A-Z]+/\($1/g;
	$line =~ s/\)/\) /g;
	$line =~ s/<[^>]*>//g;
	$line =~ s/\(([^\/\s]+)\S*/\($1/g;
    }
    @words = split(' ', $line);
    @stack = ();
    foreach (@words) {
	if ($_ =~ /\(/) {
	    if ($_ =~ /[^\(]@[^\)]/) {
		push(@stack, 0);
#		print(OUTFILE $stack[-1]);
	    }
	    else {
		push(@stack, 1);
#		print(OUTFILE $stack[-1]);
		print(OUTFILE $_ . " ");
	    }
	}
	elsif ($_ =~ /(.*)(\)+)/) {
	    print(OUTFILE $1);
	    @brackets = split(//, $2);
	    foreach(@brackets) {
		my $d = pop(@stack);
#		print(OUTFILE $d);
		if ($d == 1) {
		    print(OUTFILE ") ");
		}
	    }
	}
    }
    print(OUTFILE "\n");
}

    


