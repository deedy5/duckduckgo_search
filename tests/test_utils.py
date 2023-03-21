import datetime
import os
import tempfile
from unittest import mock

from duckduckgo_search.utils import _do_output


FAKE_TIME = datetime.datetime(2023, 1, 31, 7, 30, 0)


@mock.patch("duckduckgo_search.utils.datetime")
def test__do_output_query_without_slash(mock_datetime):
    mock_datetime.now.return_value = FAKE_TIME

    with tempfile.TemporaryDirectory() as tmpdirname:
        # should write to disk successfully.
        module_name = os.path.join(tmpdirname, 'ddg_module_name')

        keywords = 'George Washington'
        output = 'json'
        results = {'a': 'b'}

        expected_filepath = f"{module_name}_George Washington_20230131_073000.json"

        output_location = _do_output(module_name, keywords, output,results)

        assert output_location == expected_filepath


@mock.patch("duckduckgo_search.utils.datetime")
def test__do_output_query_with_slash(mock_datetime):
    mock_datetime.now.return_value = FAKE_TIME

    with tempfile.TemporaryDirectory() as tmpdirname:
        # should write to disk successfully.
        module_name = os.path.join(tmpdirname, 'ddg_module_name')

        # query that should search specific sub-path of specific site.
        keywords = 'George Washington site:"en.wikipedia.org/wiki/"'
        output = 'json'
        results = {'a': 'b'}

        expected_filepath = f"{module_name}_George Washington site:'en.wikipedia.org_wiki_'_20230131_073000.json"
        output_location = _do_output(module_name, keywords, output,results)

        assert output_location == expected_filepath
