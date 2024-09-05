from pathlib import Path
import json
import pandas as pd
import constants
import os
from typing import Union
import datetime


def load_sleep_summary(
    data_folder: os.PathLike,
    start_date: Union[datetime.datetime, datetime.date, str, pd.Timestamp, None] = None,
    end_date: Union[datetime.datetime, datetime.date, str, pd.Timestamp, None] = None,
    single_day_filter: bool = True,
) -> pd.DataFrame:
    """Load and format Garmin sleep data.

    Parameters
    ----------
    data_folder : os.PathLike
        Folder containing Garmin sleep CSV file.
    start_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        Start date with which sleep data have to be filtered (inclusive), by default None
    end_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        End date with which sleep data have to be filtered (exclusive), by default None

    Returns
    -------
    pd.DataFrame
        Formatted Garmin sleep data.
    """
    sleep_summaries = pd.read_csv(
        os.path.join(data_folder, "sleep_summaries.csv"),
        parse_dates=[constants.CALENDAR_DATE_COL, constants.ISODATE_COL],
        index_col=0,
    )

    if single_day_filter:
        sleep_summaries = filter_sleep_summary(sleep_summaries)
    if start_date is None:
        start_date = sleep_summaries[constants.CALENDAR_DATE_COL].min()
    if end_date is None:
        end_date = sleep_summaries[constants.CALENDAR_DATE_COL].max()
    sleep_summaries = (
        sleep_summaries.set_index(constants.CALENDAR_DATE_COL)
        .truncate(before=start_date, after=end_date)
        .reset_index(names=[constants.CALENDAR_DATE_COL])
    )
    return sleep_summaries


def filter_sleep_summary(sleep_summary: pd.DataFrame) -> pd.DataFrame:
    """Filter sleep summary so that a single summary is returned for each day.

    This function filters sleep summaries so that a single sleep summary
    is returned for each ``calendarDate``. The filtering is based on the
    ``"validation"`` and ``"durationInMs`` columns.

    Parameters
    ----------
    sleep_summary : :class:`pd.DataFrame`
        :class:`pd.DataFrame` with sleep summaries.

    Returns
    -------
    :class:`pd.DataFrame`
        Filtered :class:`pd.DataFrame` with a single sleep summary for each day.
    """
    # Filter based on duration and validation
    # -> Create a dummy column for filtering that we will later remove
    sleep_summary["validationMap"] = sleep_summary[constants.VALIDATION_COL].map(
        {
            "AUTO_TENTATIVE": 1,
            "AUTO_FINAL": 2,
            "ENHANCED_TENTATIVE": 3,
            "ENHANCED_FINAL": 4,
        }
    )
    sleep_summary = (
        sleep_summary.sort_values(
            by=(
                [
                    constants.CALENDAR_DATE_COL,
                    "validationMap",
                    constants.DURATION_IN_MS_COL,
                ]
            ),
            ascending=True,
        )
        .groupby(constants.CALENDAR_DATE_COL)
        .tail(1)
    )
    # Remove created column
    sleep_summary = sleep_summary.drop(["validationMap"], axis=1).reset_index(drop=True)
    return sleep_summary
