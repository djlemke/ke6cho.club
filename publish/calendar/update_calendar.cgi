#!/usr/bin/env perl
use v5.32;
use warnings;
use autodie;
use CGI::Tiny;
use Template;

cgi {
	my $cgi = $_;
	my $template = Template->new(RELATIVE => 1);
	my $template_file = '../templates/template.tt';


	my @data = $cgi->param('content');
	my $file;
	for my $v (@data) {
		$file .= "$v\n";
	}

	open my $fh, ">", "schedule.txt" or die "Can't open schedule.txt!";
	print $fh $file or die "Can't write to file!";
	truncate $fh, tell $fh;
	close $fh;

	my %tt_vars = (
		title => "Net Calendar",
		tagline => "",
		content => <<EOF,
<a href="/calendar">Back to Calendar</a><br><br>
<p>The calendar has been updated!</p>
	);
	my $page;
	$template->process($template_file, \%tt_vars, \$page) or
		die $template->error();
	$cgi->render(html => $page);
};

