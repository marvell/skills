#!/usr/bin/env bash
# Mechanical typography check for a Russian Markdown translation.
# Usage: check_typography.sh file.ru.md
# Prints "line: [rule] text" for each finding; exits 1 if anything is found.
set -euo pipefail

if [ $# -ne 1 ] || [ ! -f "$1" ]; then
  echo "Usage: check_typography.sh file.ru.md" >&2
  exit 2
fi

perl -CSD -Mutf8 -ne '
  BEGIN { $found = 0 }
  if (/^\s*```/) { $code = !$code; next }
  next if $code;
  chomp; my $l = $_;
  (my $t = $l) =~ s/`[^`]*`//g;              # inline code
  $t =~ s/\]\([^)]*\)/]/g;                   # link targets
  $t =~ s/<?https?:\/\/\S+>?//g;             # bare URLs
  my @hits;
  push @hits, "double space"          if $t =~ /\S  +\S/;
  push @hits, "mixed Cyrillic/Latin"  if $t =~ /[а-яёА-ЯЁ][a-zA-Z]|[a-zA-Z][а-яёА-ЯЁ]/;
  push @hits, "hyphen instead of dash" if $t =~ / - /;
  push @hits, "en dash with spaces"   if $t =~ / \x{2013} /;
  push @hits, "straight quotes"       if $t =~ /"/;
  push @hits, "English quotes"        if $t =~ /[\x{201C}\x{201D}]/;
  push @hits, "three dots"            if $t =~ /\.\.\./;
  push @hits, "space before punctuation" if $t =~ /\S\s+[,.;:!?](\s|$)/ && $t !~ /^\s*[*-] /;
  my $em = () = $t =~ /(?<!\*)\*(?!\*)/g;
  $em-- if $t =~ /^\s*\* /;
  push @hits, "unpaired *" if $em % 2;
  for my $h (@hits) { print "$.: [$h] $l\n"; $found = 1 }
  END { exit $found }
' "$1"
