import json
import click
import sqlite3

from twarc.expansions import ensure_flattened

@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=click.File('w'), default='-')
def hashtags(infile, outfile):
    """
    Extract and count hashtags in Twitter v2 data.
    """
    db = sqlite3.connect('hashtags.db')
    db.execute('DROP TABLE IF EXISTS hashtags')
    db.execute('CREATE TABLE hashtags (id text, created timestamp, hashtag text)')

    for line in infile:
        line = line.strip()

        # ignore empty lines
        if not line:
            continue

        data = json.loads(line)
        for tweet in ensure_flattened(data):
            if 'entities' in tweet and 'hashtags' in tweet['entities']:
                for hashtag in tweet['entities']['hashtags']:
                    db.execute(
                        '''
                        INSERT INTO hashtags (id, created, hashtag)
                        VALUES (?, ?, ?)
                        ''',
                        (tweet['id'], tweet['created_at'], hashtag['tag'])
                    )
        
        db.commit()

    click.echo('hashtag,tweets')
    for row in db.execute(
        '''
        SELECT hashtag, COUNT(*) AS total 
        FROM HASHTAGS
        GROUP BY hashtag
        ORDER BY total DESC 
        '''):
        click.echo(f'"{row[0]}",{row[1]}')





