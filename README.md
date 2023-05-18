## pbptricks &ndash; do stuff with pbp (proboards plugin) file
things that plugin editor can't do but pbptricks can:<ul>
<li>save and open plugin as <a href="https://en.wikipedia.org/wiki/JSON">json</a></li>
<li>make not editable plugin editable</li>
<li>add image with any format (including not image formats) like <a href="https://en.wikipedia.org/wiki/SVG">svg</a></li>
</ul><code>help</code> command output:<pre>usage: python3 pbptricks.py [FILE]
do stuff with pbp (proboards plugin) file&#10;
commands:
help, ?  print this help
exit, q  exit
o        open file
ro       reopen current file
c        current file info
sp       save pbp
sj       save json
s        save to current file
+e       make plugin editable
-e       make plugin not editable
aif      add image from file
ail      add image from link (url)&#10;
if input starts with &#96;"&#96; it's python3 string literal (&#96;"\x2Be"&#96; is same as &#96;+e&#96;)</pre>pbptricks name insired by <a href="https://github.com/Winetricks/winetricks">winetricks</a>