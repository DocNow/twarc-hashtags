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

[twarc]: https://github.com/docnow/twarc
