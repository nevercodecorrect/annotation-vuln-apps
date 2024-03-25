# pylint: disable=redefined-outer-name

from typing import Callable, Dict

import pytest

from tempor.methods.preprocessing.scaling import BaseScaler
from tempor.methods.preprocessing.scaling.static.plugin_static_standard_scaler import StaticStandardScaler
from tempor.utils.serialization import load, save

INIT_KWARGS = {"random_state": 123}
PLUGIN_FROM_OPTIONS = ["from_api", pytest.param("from_module", marks=pytest.mark.extra)]
TEST_ON_DATASETS = [
    "sine_data_scaled_small",
    pytest.param("sine_data_scaled_full", marks=pytest.mark.extra),
]


@pytest.fixture
def get_test_plugin(get_plugin: Callable):
    def func(plugin_from: str, base_kwargs: Dict):
        return get_plugin(
            plugin_from,
            fqn="preprocessing.scaling.static.static_standard_scaler",
            cls=StaticStandardScaler,
            kwargs=base_kwargs,
        )

    return func


@pytest.mark.parametrize("plugin_from", PLUGIN_FROM_OPTIONS)
def test_sanity(get_test_plugin: Callable, plugin_from: str) -> None:
    test_plugin = get_test_plugin(plugin_from, INIT_KWARGS)
    assert test_plugin is not None
    assert test_plugin.name == "static_standard_scaler"
    assert len(test_plugin.hyperparameter_space()) == 0


def test_no_static(get_test_plugin: Callable, get_dataset: Callable) -> None:
    test_plugin: BaseScaler = get_test_plugin("from_api", INIT_KWARGS)
    dataset = get_dataset("sine_data_scaled_small")
    dataset.static = None

    test_plugin.fit(dataset)
    out = test_plugin.transform(dataset)
    assert out.static is None


@pytest.mark.parametrize("plugin_from", PLUGIN_FROM_OPTIONS)
@pytest.mark.parametrize("data", TEST_ON_DATASETS)
def test_fit(plugin_from: str, data: str, get_test_plugin: Callable, get_dataset: Callable) -> None:
    test_plugin: BaseScaler = get_test_plugin(plugin_from, INIT_KWARGS)
    dataset = get_dataset(data)
    test_plugin.fit(dataset)


@pytest.mark.filterwarnings("ignore:RNN.*contiguous.*:UserWarning")  # Expected: problem with current serialization.
@pytest.mark.parametrize("plugin_from", PLUGIN_FROM_OPTIONS)
@pytest.mark.parametrize("data", TEST_ON_DATASETS)
@pytest.mark.parametrize(
    "covariates_dataset",
    [
        False,
        pytest.param(True, marks=pytest.mark.extra),
    ],
)
def test_transform(
    plugin_from: str,
    data: str,
    covariates_dataset: bool,
    get_test_plugin: Callable,
    get_dataset: Callable,
    as_covariates_dataset: Callable,
) -> None:
    test_plugin: BaseScaler = get_test_plugin(plugin_from, INIT_KWARGS)
    dataset = get_dataset(data)

    if covariates_dataset:
        dataset = as_covariates_dataset(dataset)

    assert dataset.static is not None  # nosec B101
    assert (dataset.static.numpy() > 50).any()

    dump = save(test_plugin)
    reloaded = load(dump)

    reloaded.fit(dataset)

    dump = save(reloaded)
    reloaded = load(dump)

    output = reloaded.transform(dataset)

    assert (output.static.numpy() < 50).all()
