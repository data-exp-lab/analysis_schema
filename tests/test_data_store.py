import pytest
from yt.testing import fake_random_ds

from analysis_schema._data_store import DatasetContext, DataStore
from analysis_schema._testing import yt_file_exists


def test_data_storage():
    dstore = DataStore()

    dstore.store("test_file.hdf", dataset_name="test")
    assert len(dstore.list_available()) == 1

    # using the same dataset_name should not add another file
    fi2 = "test_file_2.hdf"
    dstore.store(fi2, dataset_name="test")
    assert len(dstore.list_available()) == 1
    assert dstore.available_datasets["test"].filename == "test_file.hdf"

    # adding without a name will use the filename
    dstore.store(fi2)
    assert len(dstore.list_available()) == 2
    assert dstore.available_datasets[fi2].filename == fi2

    # add an in-mem dataset
    ds = fake_random_ds(3)
    dstore.store("in_mem_ds", in_memory_ds=ds)
    assert len(dstore.list_available()) == 3
    assert dstore.available_datasets["in_mem_ds"]._on_disk is False
    assert dstore.available_datasets["in_mem_ds"]._ds == ds


def test_dataset_context_in_mem():
    ds = fake_random_ds(3)
    dcont = DatasetContext("in_mem_ds", in_memory_ds=ds)
    assert dcont._on_disk is False
    assert dcont._ds == ds
    with dcont.load() as ds_from_context:
        assert ds == ds_from_context


def test_dataset_context_storage():
    fi = "IsolatedGalaxy/galaxy0030/galaxy0030"
    dcont = DatasetContext(fi)
    assert dcont._on_disk


def test_dataset_context_on_disk():
    # will only run if the dataset is available.
    fi = "IsolatedGalaxy/galaxy0030/galaxy0030"
    if yt_file_exists(fi):
        dcont = DatasetContext(fi)
        assert dcont._on_disk
        with dcont.load() as ds_from_context:
            assert fi in ds_from_context.parameter_filename
    else:
        pytest.skip("Dataset file is unavailable.")


def test_loading_from_datastore():

    files = [
        "IsolatedGalaxy/galaxy0030/galaxy0030",
        "enzo_tiny_cosmology/DD0000/DD0000",
    ]

    for fi in files:
        if yt_file_exists(fi) is False:
            pytest.skip(f"{fi} not found.")

    dstore = DataStore()
    for fi in files:
        dstore.store(fi)

    ds = fake_random_ds(3)
    dstore.store("in_mem_ds", in_memory_ds=ds)

    assert len(dstore.list_available()) == 3

    for ds_name in dstore.list_available():
        ds_con = dstore.retrieve(ds_name)
        with ds_con.load() as ds_:
            _ = ds_.domain_center
