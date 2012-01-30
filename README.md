# Synopsis

Cleans up Mifos translation files. Example usage:

    python add_prefixes.py GOOD.po BAD.po

Where `GOOD.po` is a file with prefixes, and `BAD.po` is a file with
everything *but* proper prefixes.

    python add_prefixes.py out-mifos-0-all_lo.po part1_lo_clean.po

The (hopefully) cleaned up [PO](http://www.gnu.org/software/gettext/manual/gettext.html#PO-Files) data is written to `fixed.po`.

Some messages are logged to the console, others to a file called `log`.

# Bugs

## msgctxt assumed single line

If msgctxt can span multiple lines, this script can't parse it.

## Terminology probably wrong

I used the word "prefix" to mean "the thing before the key used in Mifos Java
.properties-based translated messages files", but the wikimedia-i18n folks
might use the word "group" or "group ID" or something instead.

For the msgctxt `menu-label.loan`, `menu` is the "prefix".

## Multiple matches for prefix

The following is not [easily] automatically resolvable, and must be manually
corrected:

1. `errors.required` could be `client-errors.required`, `center-errors.required`, or something else.

# Source code

<https://github.com/meonkeys/mifos-fix-i18n-prefixes>

# See also

<http://thread.gmane.org/gmane.comp.finance.mifos.devel/12605/focus=12607>

# Fine print

Copyright ©2012 Adam Monsen <haircut@gmail.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
