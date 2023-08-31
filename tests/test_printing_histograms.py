from typing import Dict, Optional, Sequence

import hypothesis.strategies as st
from hypothesis import given

from data_samples_printer.making_histograms import Annotations
from data_samples_printer.printing_histograms import print_hist

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
    annotations=st.sampled_from(Annotations),
    markdown_mode=st.booleans(),
    print_header=st.booleans(),
    print_footer=st.booleans(),
)
def test_print_hist(
    xs: Sequence[Sequence[float]],
    max_bins_above_num_bins: int,
    num_bins: Optional[int],
    min_value: Optional[float],
    max_value: Optional[float],
    annotations: Annotations,
    markdown_mode: bool,
    print_header: bool,
    print_footer: bool,
) -> None:
    if num_bins is not None:
        max_bins = num_bins + max_bins_above_num_bins
    else:
        max_bins = 50

    print_hist(
        *xs,
        max_bins=max_bins,
        num_bins=num_bins,
        min_value=min_value,
        max_value=max_value,
        annotations=annotations,
        markdown_mode=markdown_mode,
        print_header=print_header,
        print_footer=print_footer,
    )


@given(
    named_xs=st.dictionaries(st.text(), st.lists(safe_floats, min_size=2)),
    num_bins=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
    max_bins_above_num_bins=st.integers(min_value=0, max_value=100),
    min_value=st.one_of(st.none(), safe_floats),
    max_value=st.one_of(st.none(), safe_floats),
    annotations=st.sampled_from(Annotations),
    markdown_mode=st.booleans(),
    print_header=st.booleans(),
    print_footer=st.booleans(),
)
def test_print_hist_kwargs(
    named_xs: Dict[str, Sequence[float]],
    max_bins_above_num_bins: int,
    num_bins: Optional[int],
    min_value: Optional[float],
    max_value: Optional[float],
    annotations: Annotations,
    markdown_mode: bool,
    print_header: bool,
    print_footer: bool,
) -> None:
    if num_bins is not None:
        max_bins = num_bins + max_bins_above_num_bins
    else:
        max_bins = 50

    print_hist(
        **named_xs,
        max_bins=max_bins,
        num_bins=num_bins,
        min_value=min_value,
        max_value=max_value,
        annotations=annotations,
        markdown_mode=markdown_mode,
        print_header=print_header,
        print_footer=print_footer,
    )
