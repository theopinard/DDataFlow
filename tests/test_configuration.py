import os
import pytest
from ddataflow import DDataflow


def test_initialize_successfully():
    """
    Tests that a correct config will not fail to be instantiated
    """
    from ddataflow.samples.ddataflow_config import config

    DDataflow(**config)


def test_wrong_config_fails():
    with pytest.raises(BaseException, match="wrong param"):
        from ddataflow.samples.ddataflow_config import config

        DDataflow(**{**config, **{"a wrong param": "a wrong value"}})


def test_current_project_path():
    """
    Test that varying our environment we get different paths
    """
    config = {
        "project_folder_name": "my_tests",
    }
    ddataflow = DDataflow(**config)
    # by default do not override
    assert ddataflow._get_overriden_arctifacts_current_path() is None
    ddataflow.enable()
    assert (
        "dbfs:/ddataflow/my_tests"
        == ddataflow._get_overriden_arctifacts_current_path()
    )
    ddataflow.enable_offline()
    assert (
        os.getenv("HOME") + "/.ddataflow/my_tests"
        == ddataflow._get_overriden_arctifacts_current_path()
    )


def test_temp_table_name():

    config = {
        "sources_with_default_sampling": ["location"],
        "project_folder_name": "unit_tests",
    }

    ddataflow = DDataflow(**config)
    # by default do not override
    assert ddataflow._get_source_name_only("location") == "location"
    ddataflow.enable()
    assert (
        ddataflow._get_source_name_only("location") == "unit_tests_location"
    )
