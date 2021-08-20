from twarc_hashtags import hashtags
from click.testing import CliRunner

runner = CliRunner()

def test_v2():
    result = runner.invoke(hashtags, ['test-data/tweets.jsonl'])
    assert result.exit_code == 0
    assert result.output == \
'''hashtag,tweets
"naacpimageawards",2
"usa",1
"trafficking",1
"refugees",1
"obama",1
"isis",1
"illegals",1
"cartel",1
"biden",1
'''
