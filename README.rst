=====
dj2j2
=====

Known limitations
=================

``dj2j2`` isn't perfect and should be paired with an extensive test suite.

 * Django has implicit method calls, but Jinja2 doesn't. This means that there will be some functions that we can't detect, and therefore won't translate into explicit calls.
