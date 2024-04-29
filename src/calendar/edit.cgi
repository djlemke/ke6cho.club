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

	open my $fh, "<", "../calendar/schedule.txt" or die "Can't open schedule.txt!";
	local $/;
	my $file = <$fh>;
	close $fh;

	my $content = <<EOF;
<a href="/calendar">Back to Calendar</a><br><br>
<p>Note: You can use tabs to seperate values!</p>
<p>This file is simple. The number is the day, and the name is who will host.</p>
<form method="POST" action="update_calendar.cgi">
	<textarea id="content" name="content" rows=10>$file</textarea>
	<input type="submit">
</form>
<script type="text/javascript">
document.querySelector('#content').addEventListener('keydown', function(e) {
	if (e.key == 'Tab') {
		e.preventDefault();
		var start = this.selectionStart;
		var end = this.selectionEnd;
		this.value = this.value.substring(0, start) +
			"\\t" + this.value.substring(end);
		this.selectionStart = this.selectionEnd = start + 1;
	}
});
</script>
EOF

	my %tt_vars = (
		title => "Net Calendar",
		tagline => "",
		content => $content,
		stylesheets => '<link rel="stylesheet" type="text/css" href="/calendar/edit.css">',
	);
	my $page;
	$template->process($template_file, \%tt_vars, \$page) or
		die $template->error();
	$cgi->render(html => $page);
};

