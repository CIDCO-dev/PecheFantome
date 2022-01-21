#!/usr/bin/perl

use warnings;
use strict;

# Cleanup the DFO CSV file to convert DMS locations to decimal degrees

while(<STDIN>){
	my $line=$_;

	if($line =~ /^(\d{4}-\d{2}-\d{2}),(.+),(.+),(.+),(.+),(.+),(.+)/){
		my ($date,$type,$nb,$net,$rope,$lat,$lon)=($1,$2,$3,$4,$5,$6,$7);

		if($lat =~ /(\d{2}).*(\d{2}).*(\d{2,3}).*(W|E|N|S)/){
			$lat = $1 + ($2/60.0) + ($3/3600.0);

			if($lon =~ /(\d{2}).*(\d{2}).*(\d{2,3}).*(W|E|N|S)/){
                        	$lon = -1.0 * ($1 + ($2/60.0) + ($3/3600.0));

				print "$date,$type,$nb,$net,$rope,$lat,$lon\n";
                	}
		}
	}
	else{
		#print $line;
	}
}
