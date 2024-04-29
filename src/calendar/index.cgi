#!/usr/bin/env perl
use v5.32;
use warnings;
use autodie;
use CGI::Tiny;
use Template;
use HTML::Make::Calendar 'calendar';

sub gethost {
	my ($sched, $date, $element) = @_;
	my $month = $date->{month};
	my $day = $date->{dom};

	if ($sched->{$month}{$day}) {
		$element->add_text("$date->{dom}<br><b>$sched->{$month}{$day}</b>");
	} else {
		$element->add_text("$date->{dom}");
	}
}

cgi {
	my $cgi = $_;
	my $template = Template->new(RELATIVE => 1);
	my $template_file = '../templates/template.tt';
	my %schedule;
	my $month;
	my %months = (
		January => 1,
		February => 2,
		March => 3,
		April => 4,
		May => 5,
		June => 6,
		July => 7,
		August => 8,
		September => 9,
		October => 10,
		November => 11,
		December => 12,
	);

	open my $fh, "<", "schedule.txt" or die "Can't open schedule.txt!";
	while (<$fh>) {
		if ($_ =~ /January|February|March|April|May|June|July|August|September|October|November|December/) {
			$_ =~ s/\s//g;
			$month = $months{$_};
		}

		if ($_ =~ /[0-9]+\s+\w+/) {
			my @line = split /\s+/;
			my $day = $line[0];
			my $host = $line[1];
			$schedule{$month}{$day} = $host;
		}
	}
	close $fh;

	my $content = '<a href="/calendar/edit.cgi">Edit Calendar</a><br><br>';
	# localtime returns month as 0..11, but the calendar function expects
	# 1..12.
	my $thismonth = ((localtime(time))[4] + 1);
	for (my $i = $thismonth; $i <= 12; $i++) {
		my $cal = calendar(
			month => $i,
			dayc => \&gethost,
			cdata => \%schedule);
		$content .= $cal->text();
		$content .= "<br>";
	}

	my %tt_vars = (
		title => "Net Calendar",
		tagline => "",
		stylesheets => '<link rel="stylesheet" type="text/css" href="/calendar/calendar.css">',
		content => $content,
	);
	my $page;
	$template->process($template_file, \%tt_vars, \$page) or
		die $template->error();
	$cgi->render(html => $page);
};

