from typing import Dict, Mapping, Optional, Sequence

import hypothesis.strategies as st
from hypothesis import given

from data_samples_printer.making_histograms import (
    Annotations,
    generate_annotated_hists,
    generate_hists,
    make_header,
    make_min_max_footer,
)

safe_floats = st.one_of(
    st.floats(min_value=0.0000000001, max_value=100000000, allow_subnormal=False),
    st.floats(min_value=-100000000, max_value=-0.0000000001, allow_subnormal=False),
    st.just(0.0),
)


@given(
    xs=st.lists(st.lists(safe_floats, min_size=2)),
    num_bins=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
    max_bins_above_num_bins=st.integers(min_value=0, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
)
def test_generate_hists(
    xs: Sequence[Sequence[float]],
    max_bins_above_num_bins: int,
    num_bins: Optional[int],
    min_value: Optional[float],
    max_value: Optional[float],
) -> None:
    if num_bins is not None:
        max_bins = num_bins + max_bins_above_num_bins
    else:
        max_bins = 50

    hists = list(
        generate_hists(
            *xs,
            max_bins=max_bins,
            num_bins=num_bins,
            min_value=min_value,
            max_value=max_value,
        )
    )

    assert len(hists) == len(xs)


@given(
    xs=st.lists(st.lists(safe_floats, min_size=2)),
    num_bins=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
    max_bins_above_num_bins=st.integers(min_value=0, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
    annotations=st.sampled_from(Annotations),
)
def test_generate_annotated_hists(
    xs: Sequence[Sequence[float]],
    max_bins_above_num_bins: int,
    num_bins: Optional[int],
    min_value: Optional[float],
    max_value: Optional[float],
    annotations: Annotations,
) -> None:
    if num_bins is not None:
        max_bins = num_bins + max_bins_above_num_bins
    else:
        max_bins = 50

    hists = list(
        generate_annotated_hists(
            *xs,
            max_bins=max_bins,
            num_bins=num_bins,
            min_value=min_value,
            max_value=max_value,
            annotations=annotations,
        )
    )

    assert len(hists) == len(xs)


@given(
    named_xs=st.dictionaries(st.text(), st.lists(safe_floats, min_size=2)),
    num_bins=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
    max_bins_above_num_bins=st.integers(min_value=0, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
    annotations=st.sampled_from(Annotations),
)
def test_generate_annotated_hists_kwargs(
    named_xs: Dict[str, Sequence[float]],
    max_bins_above_num_bins: int,
    num_bins: Optional[int],
    min_value: Optional[float],
    max_value: Optional[float],
    annotations: Annotations,
) -> None:
    if num_bins is not None:
        max_bins = num_bins + max_bins_above_num_bins
    else:
        max_bins = 50

    hists = list(
        generate_annotated_hists(
            **named_xs,
            max_bins=max_bins,
            num_bins=num_bins,
            min_value=min_value,
            max_value=max_value,
            annotations=annotations,
        )
    )

    assert len(hists) == len(named_xs)


@given(annotations=st.sampled_from(Annotations), add_names_column=st.booleans())
def test_make_header(annotations: Annotations, add_names_column: bool) -> None:
    make_header(annotations, add_names_column)


@given(
    xs=st.lists(st.lists(safe_floats, min_size=2)),
    width=st.integers(min_value=1, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
)
def test_make_min_max_footer_with_args(
    xs: Sequence[Sequence[float]],
    width: int,
    min_value: Optional[float],
    max_value: Optional[float],
) -> None:
    if min_value is not None and max_value is not None and min_value < max_value:
        min_value, max_value = max_value, min_value
    make_min_max_footer(*xs, width=width, min_value=min_value, max_value=max_value)


@given(
    named_xs=st.dictionaries(st.text(), st.lists(safe_floats, min_size=2)),
    width=st.integers(min_value=1, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
)
def test_make_min_max_footer_with_kwargs(
    named_xs: Mapping[str, Sequence[float]],
    width: int,
    min_value: Optional[float],
    max_value: Optional[float],
) -> None:
    if min_value is not None and max_value is not None and min_value < max_value:
        min_value, max_value = max_value, min_value
    make_min_max_footer(
        width=width, min_value=min_value, max_value=max_value, **named_xs
    )
