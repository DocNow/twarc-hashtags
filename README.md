# twarc-hashtags

This module is extends [twarc] with a `hashtags` command that will extract and
count the hashtags in a tweet dataset.

## Install

    pip install twarc-hashtags

Collect some Twitter data, for example:

    twarc2 search blacklivesmatter tweets.jsonl 

Because you installed the plugin you have a new subcommand `hashtags`:

    twarc2 hashtags tweets.jsonl hashtags.csv

Then open `hashtags.csv` in your favourite spreadsheet program or
DataFrame library.

Behind the scenes twarc-hashtags uses Python's native support for SQLite to
create a database and then insert/query it. You can see this database after the
program finishes as `hashtags.db` in your current working directory.

## Options

**--group**: group results by day, week, month, year

**--limit**: limit to this number of hashtags (per group if --group is used)

**--db**: if you would like to name the database something other than
`hashtags.db`

**--no-insert**: use an existing database instead of inserting (useful for
large numbers of tweets)

[twarc]: https://github.com/docnow/twarc
