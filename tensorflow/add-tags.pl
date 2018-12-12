#!/usr/bin/perl
# 


use strict;

open(IN, "< $ARGV[0]") || die "Could not open $ARGV[0]\n$!\n";
my @lines = <IN>;
close(IN);

my $DEST = "$ARGV[0]";
open(OUT, "> $DEST") || die "Can not write to $DEST\n$!\n";

	print OUT "<S>\n</S>\n<UNK>\n"";

foreach my $i  (0 .. $#lines)
{	

print OUT $lines[$i] ;
}


close(OUT);


exit;

