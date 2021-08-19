from twarc_hashtags import hashtags
from click.testing import CliRunner

runner = CliRunner()

def test_v2():
    result = runner.invoke(hashtags, ['test-data/tweets.jsonl'])
    assert result.exit_code == 0
    assert result.output == '1366871005755547653\n'
