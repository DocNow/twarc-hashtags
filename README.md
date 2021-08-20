# twarc-hashtags

This module is extends [twarc] with a `hashtags` command that will extract and
count the hashtags in a tweet dataset.

## Install

    pip install twarc-hashtags

Now you can collect data using the core twarc utility:

    twarc2 search blacklivesmatter tweets.jsonl

And you have a new subcommand `hashtags`:

    twarc2 hashtags tweets.jsonl hashtags.csv

Then you can open `hashtags.csv` in your favourite spreadsheet program or
DataFrame library.

Behind the scenes twarc-hashtags uses Python's native support for SQLite to
create a database and then insert/query it. You can see this database after the
program finishes as `hashtags.db` in your current working directory.

[twarc]: https://github.com/docnow/twarc
