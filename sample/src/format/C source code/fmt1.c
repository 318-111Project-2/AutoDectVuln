/*
Description: Printf is called with a format from a table.  This is not a defect.
Keywords: Port C Size0 Complex0 Taint FormatString
ValidArg: "%s"*100
ValidArg: "!%s" % ("%s"*100)

Copyright 2005 Fortify Software.

Permission is hereby granted, without written agreement or royalty fee, to
use, copy, modify, and distribute this software and its documentation for
any purpose, provided that the above copyright notice and the following
three paragraphs appear in all copies of this software.

IN NO EVENT SHALL FORTIFY SOFTWARE BE LIABLE TO ANY PARTY FOR DIRECT,
INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF FORTIFY SOFTWARE HAS
BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMANGE.

FORTIFY SOFTWARE SPECIFICALLY DISCLAIMS ANY WARRANTIES INCLUDING, BUT NOT
LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

THE SOFTWARE IS PROVIDED ON AN "AS-IS" BASIS AND FORTIFY SOFTWARE HAS NO
OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
*/

/*Link  https://samate.nist.gov/SARD/test-cases/1561/versions/1.0.0*/ 

/*have 1 format string bug */

#include <stdio.h>

char *fmts[] = {
	"<%s>\n",
	"[%s]\n",
};

void test(char *str)
{
	int idx;

	idx = (str[0] == '!');
	printf(fmts[idx], str);				/* bad */
}

int main(int argc, char **argv)
{
	char *userstr;
	scanf("%s",userstr);
	test(userstr);
	return 0;
}