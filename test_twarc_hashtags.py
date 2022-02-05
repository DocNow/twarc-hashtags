from twarc_hashtags import hashtags
from click.testing import CliRunner

runner = CliRunner()


def test_basic():
    result = runner.invoke(hashtags, ["test-data/tweets1.jsonl"])
    assert result.exit_code == 0
    assert (
        result.output
        == """hashtag,tweets
naacpimageawards,2
usa,1
trafficking,1
refugees,1
obama,1
isis,1
illegals,1
cartel,1
biden,1
"""
    )


def test_group():
    result = runner.invoke(hashtags, ["--group", "day", "test-data/tweets2.jsonl"])
    assert result.exit_code == 0
    assert result.output.startswith(
        """hashtag,time,tweets
bitcoin,2021-08-20,10
reinstate45,2021-08-20,5
hypocrisy,2021-08-20,5
fbi,2021-08-20,5
"""
    )


def test_limit():
    result = runner.invoke(hashtags, ["--limit", "5", "test-data/tweets2.jsonl"])
    assert result.exit_code == 0
    assert (
        result.output
        == """hashtag,tweets
wtfhappenedin1971,389
bitcoin,372
banliznowjack,230
btc,113
farmersprotest,111
"""
    )


def test_retweets():
    result = runner.invoke(hashtags, ["test-data/tweets3.jsonl"])
    assert result.exit_code == 0
    assert result.output.startswith(
        """hashtag,tweets
endsars,2
freeimoleayo,2
"""
    )
