#!/usr/bin/env perl
use v5.32;
use warnings;
use autodie;
use Template;
use File::Basename;
use File::Copy;
use File::Copy::Recursive;

my $template = Template->new(
	INCLUDE_PATH => "templates:pages",
	RELATIVE => 1,
	OUTPUT_PATH => "release"
);
opendir my $dh, "pages" or die "Couldn't open pages dir.";
my @files = readdir $dh;
closedir $dh;

for my $file (@files) {
	next unless $file =~ /^\w+\.tt$/;
	my $filename = basename($file, '.tt');

	$template->process($file, '', "$filename.html") or 
		die $template->error();
}

opendir $dh, "./" or die "Couldn't open src dir.";
@files = readdir $dh;
closedir $dh;

for my $file (@files) {
	next unless $file =~ /^[a-zA-Z0-9\-_ ]+\.*[a-zA-Z0-9\-_ ]*$/;
	next if $file =~ /^release|pages|mksite.pl|deploy.sh|passwd$/;

	if ($file =~ /^[a-zA-Z0-9\-_ ]+\.+[a-zA-Z0-9\-_ ]+$/) {
		copy($file, "release/$file") or die "Couldn't copy file $file";
	} elsif ($file =~ /^[a-zA-Z0-9\-_ ]+$/) {
		File::Copy::Recursive::dircopy($file, "release/$file") or die "Couldn't copy directory $file";
	}
}
