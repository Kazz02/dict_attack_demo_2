#!C:/Strawberry/perl/bin/perl.exe
# Must be changed if using Mac

use strict; 	# for good coding practices
use warnings;	# help catch potential issues
use Time::HiRes qw(gettimeofday tv_interval); # Shows the time taken for the process (in milliseconds instead of seconds)

our %FORM; # Declare a global hash to store form data
my ($result, $process_time) = split(/\n/, DictAttack(*FORM));

#DictAttack(*FROM);
print <<END_OF_DATA;
Content-type: text/html;

<html lang="ja">
<head>
<title>Password Crack demo 1 - Dictionary Attack</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta name="viewport"
  content="width=320,content="text/html;",
     height=480,
     initial-scale=1.0,
     minimum-scale=1.0,
     maximum-scale=2.0,
     user-scalable=yes" />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<style>
h2 {
 padding: 0.5em;/*文字周りの余白*/
 color: #010101;/*文字色*/
 background: #eaf3ff;/*背景色*/
 border-bottom: solid 3px #516ab6;/*下線*/
}
</style>
<script type="text/javascript" src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
</head>
<body>
<h2 style="padding:10px;">
	辞書攻撃（Dictionary Attack）体験
</h2>
<form action="dict_attack_org.cgi" method="POST">
<div style="padding:10px;">
	<div>
	<span>実際にどのくらい時間がかかるのか体験してみよう</span>
	</div>
	<div>
	<span>適当な<span style="color:red">パスワード（苗字＋数字4桁）</span>を入力してください</span>
	</div>
	<div>
	<input type="password" name="TARGET" size="20">
	</div>
</div>

<div style="padding:10px;">
	<div>
	<span>辞書攻撃（Dictionary Attack）で入力したパスワード（苗字＋数字4桁）を解析しますので、実行ボタンを押下してください</span>
	</div>
	<div style="padding-top:10px;">
	<input type="submit" value="実行" />
	</div>
	<div>$result</div>
	<div>Process Time : $process_time milliseconds</div> 
</div>
</div>
</form>
</body>
</html>

END_OF_DATA


# Jesse's solution for the dictionary attack: HASH-based approach
sub DictAttack {
    local(*FORM) = @_;
    my ($buf, $tmp, $name, $value);

	# Get from data from POST method or QUERY_STRING
    if ($ENV{'REQUEST_METHOD'} eq "POST") {
        read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
    } else {
        $buf = $ENV{'QUERY_STRING'};
    }

	# Parse the form data
    foreach $tmp (split(/&/, $buf)) {
        ($name, $value) = split(/=/, $tmp, 2);
        $value =~ tr/+/ /;
        $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg; # Decode URL-encoded characters
        $FORM{$name} = $value; # Stores the parsed data in the %FORM hash
    }

	# Get the target from the form
    my $target = $FORM{"TARGET"} || ''; 
    my $result = "cannot find out your password";

	# Start timer to measure process time
	my $start_time = [gettimeofday];

	# ==== HASH-based Dictionary Attack logic ====
	# Hash-based has O(1) lookup time, making it efficient for large datasets.
		# Compared to the original nested loops that have O(n*10^4) complexity (due to 4 'for' loops).
	# Code creates a hash table from the name dictionary, and checks if the target is in the hash table.
	# Lookup time is constant O(1) instead of performing 10,000 comparisons for each surname + digits combination.
	# If the target matches a surname from the dictionary followed by 4 digits, it returns the result immediately.

    # Creates a hash table to store surnames
    my %name_dict;

	# Load the surnames into the hash table from name-dict.txt
	# Each surname is a key in the hash table, with a value of 1 (indicating existence).
    if (open(my $fh, "<", "name-dict.txt")) { # $fh = name-dict.txt file handle
        while (my $line = <$fh>) {
            chomp $line;
            $name_dict{$line} = 1; # <---
        }
        close($fh);
    } else {
        return "Error: Cannot open name-dict.txt\n";
    }

    # Check for the given pattern (surname + 4 digits)
    if ($target =~ /^([a-z]+)(\d{4})$/) {
        my ($surname, $digits) = ($1, $2); # Extract surname and digits from the target
		# Check if the surname exists in the hash table
        if (exists $name_dict{$surname}) {
            $result = $target; # Match found
        }
    }

 	# Calculate elapsed time in milliseconds with 3 decimal places
    my $elapsed = tv_interval($start_time) * 1000;  # Convert to milliseconds
    my $time_display = sprintf("%.3f", $elapsed);

	return "Result: $result\n$time_display";
}

	# THE FOLLOWING CODE IS THE ORIGINAL CODE, COMMENTED OUT

	#open(wordlist, "name-dict.txt");
	#$linecount = 0;
	#$pcount = 0; # Added to fix the undefined variable warning #J
	#if( $pcount < 10 ){
	#	while(<wordlist>){
	#		chop();
	#		for( $i=0 ; $i < 10 ; $i++ ){
	#			for( $j=0 ; $j < 10 ; $j++ ){
	#				for( $k=0 ; $k < 10 ; $k++ ){
	#					for( $l=0 ; $l < 10 ; $l++ ){
	#						if( $_.$i.$j.$k.$l  eq $target ){
	#							$result = $_.$i.$j.$k.$l;
	#							$found = 1;
	#						}
	#					}
	#				}
	#			}
	#		}
	#		if( $found == 1 ){
	#			last; # Exit the loop if password is found
	#		}
	#	}
	#	close(wordlist);
	# $end_time = time;
	# $process_time = $end_time - $start_time;

