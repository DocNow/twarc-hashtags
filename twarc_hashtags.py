import json
import click
import sqlite3

from pathlib import Path
from twarc.expansions import ensure_flattened
from twarc.decorators2 import FileSizeProgressBar

@click.command()
@click.option(
    "--group", 
    "-g",
    type=click.Choice(["day", "week", "month", "year"]),
    help="Group hashtag results by time"
)
@click.option(
    "--db",
    "-d",
    "db_path",
    default="hashtags.db",
    help="Path to use for the SQLite database"
)
@click.option(
    "--skip-import",
    "-s",
    is_flag=True,
    help="Skip loading the tweets and use existing SQLite database"
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=0,
    help="Limit output to this many hashtags"
)
@click.argument("infile", type=click.File("r"), default="-")
@click.argument("outfile", type=click.File("w"), default="-")
def hashtags(group, db_path, limit, skip_import, infile, outfile):
    """
    Extract and count hashtags in Twitter v2 data.
    """

    db = sqlite3.connect(db_path)
    if not skip_import:
        db.execute("DROP TABLE IF EXISTS hashtags")
        db.execute("CREATE TABLE hashtags (id text, created timestamp, hashtag text)")
        load(infile, outfile, db)

    export(outfile, db, group, limit)


def load(infile, outfile, db):

    with FileSizeProgressBar(infile, outfile) as progress: 
        for line in infile:
            progress.update(len(line))

            # ignore empty lines
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)
            for tweet in ensure_flattened(data):
                # Process Retweets:
                if "referenced_tweets" in tweet:
                    rts = [t for t in tweet["referenced_tweets"] if t["type"] == "retweeted"]
                    retweeted_tweet = rts[-1] if rts else None
                    # If it's a native retweet, replace the "RT @user Text" with the original text, metrics, and entities, but keep the Author.
                    if retweeted_tweet:
                        # A retweet inherits everything from retweeted tweet.
                        tweet["text"] = retweeted_tweet.pop("text", None)
                        tweet["entities"] = retweeted_tweet.pop("entities", None)
                        tweet["attachments"] = retweeted_tweet.pop("attachments", None)
                        tweet["context_annotations"] = retweeted_tweet.pop(
                            "context_annotations", None
                        )
                        tweet["public_metrics"] = retweeted_tweet.pop("public_metrics", None)
                if "entities" in tweet and "hashtags" in tweet["entities"]:
                    for hashtag in tweet["entities"]["hashtags"]:
                        db.execute(
                            """
                            INSERT INTO hashtags (id, created, hashtag)
                            VALUES (?, ?, ?)
                            """,
                            (
                                tweet["id"],
                                tweet["created_at"],
                                hashtag["tag"].lower()
                            )
                        )
            
            db.commit()


def export(outfile, db, group, limit):

    if group:
        click.echo("hashtag,time,tweets", outfile)
    else:
        click.echo("hashtag,tweets", outfile)

    # if the grouping results by time period
    if group:
        if group == "day":
            fmt = "%Y-%m-%d"
        elif group == "week":
            fmt = "%Y-%W"
        elif group == "month":
            fmt = "%Y-%m"
        elif group == "year":
            fmt = "%Y"

        sql = \
            """
            SELECT
                hashtag,
                STRFTIME(?, created) AS time,
                COUNT(*) AS tweets
            FROM hashtags
            GROUP BY time, hashtag
            ORDER BY time DESC, tweets DESC 
            """

        results = db.execute(sql, [fmt])

    # otherwise we're doing a global count
    else:
        sql = \
            """
            SELECT hashtag, COUNT(*) AS tweets
            FROM HASHTAGS
            GROUP BY hashtag
            ORDER BY tweets DESC 
            """
        results = db.execute(sql)

    count = 0
    skip_group = None
    for row in results:
        count += 1

        if skip_group:
            if skip_group == row[1]:
                continue
            else:
                count = 0
                skip_group = None

        if limit != 0 and count > limit:
            if group:
                skip_group = row[1]
            else:
                break

        click.echo(",".join(map(str, row)), outfile)
