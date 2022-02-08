from twarc_hashtags import hashtags
from click.testing import CliRunner

runner = CliRunner()


def test_basic():
    result = runner.invoke(hashtags, ["test-data/tweets1.jsonl"])
    assert result.exit_code == 0
    assert (
        result.output
        == """hashtag,tweets
gettyimagesnews,2
naacpimageawards,2
savetheseabirds,2
biden,1
boulder,1
cartel,1
forthepeopleact,1
guncontrolnow,1
illegals,1
isis,1
islarebelde,1
nft,1
niunamenos,1
nra,1
obama,1
patriaomuerte,1
refugees,1
sethrich,1
trafficking,1
usa,1
"""
    )


def test_group():
    result = runner.invoke(hashtags, ["--group", "day", "test-data/tweets2.jsonl"])
    assert result.exit_code == 0
    assert result.output.startswith(
        """hashtag,time,tweets
ethereum,2021-08-20,13
bitcoin,2021-08-20,10
fbi,2021-08-20,5
hypocrisy,2021-08-20,5
"""
    )


def test_limit():
    result = runner.invoke(hashtags, ["--limit", "5", "test-data/tweets2.jsonl"])
    assert result.exit_code == 0
    assert (
        result.output
        == """hashtag,tweets
banliznowjack,650
wtfhappenedin1971,599
bitcoin,469
farmersprotest,128
btc,121
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
