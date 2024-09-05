import os
from pathlib import Path
import pandas as pd
import constants
from typing import Union
import datetime

WHOOP_SLEEP_DATA_FILENAME = "sonno.csv"
WHOOP_DAILY_DATA_FILENAME = "cicli_fisiologici.csv"

WHOOP_CYCLE_START_COL = "Ora di inizio ciclo"
WHOOP_SLEEP_START_COL = "Inizio del sonno"
WHOOP_SLEEP_END_COL = "Inizio del risveglio"
WHOOP_AWAKE_TIME_IN_MIN_COL = "Durata del risveglio (min)"
WHOOP_SLEEP_DURATION_IN_MIN_COL = "Durata del sonno (min)"
WHOOP_REM_SLEEP_DURATION_IN_MIN_COL = "Durata REM (min)"
WHOOP_LIGHT_SLEEP_DURATION_IN_MIN_COL = "Durata del sonno leggero (min)"
WHOOP_DEEP_SLEEP_DURATION_IN_MIN_COL = "Durata profondo (SWS) (min)"

WHOOP_HRV_COL = "Variabilità della frequenza cardiaca (ms)"


def load_sleep_summary(
    data_folder: os.PathLike,
    start_date: Union[datetime.datetime, datetime.date, str, pd.Timestamp, None] = None,
    end_date: Union[datetime.datetime, datetime.date, str, pd.Timestamp, None] = None,
) -> pd.DataFrame:
    """Load and format Whoop sleep data.

    Parameters
    ----------
    data_folder : os.PathLike
        Folder containing Whoop sleep CSV file.
    start_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        Start date with which sleep data have to be filtered (inclusive), by default None
    end_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        End date with which sleep data have to be filtered (exclusive), by default None

    Returns
    -------
    pd.DataFrame
        Formatted Whoop sleep data.

    Raises
    ------
    FileNotFoundError
        If folder does not exist or if sleep data are not found inside folder.
    """
    if not Path(data_folder).exists():
        raise FileNotFoundError(f"Folder {data_folder} does not exist.")
    # Path to sleep summary
    path_to_sleep_summary = Path(data_folder) / WHOOP_SLEEP_DATA_FILENAME
    if not path_to_sleep_summary.exists():
        raise FileNotFoundError(f"File {path_to_sleep_summary} does not exist.")
    # Read CSV file
    sleep_summary = pd.read_csv(
        path_to_sleep_summary,
        parse_dates=[WHOOP_CYCLE_START_COL, WHOOP_SLEEP_START_COL, WHOOP_SLEEP_END_COL],
    )
    sleep_summary = sleep_summary.rename(
        columns={
            WHOOP_SLEEP_START_COL: constants.ISODATE_COL,
            WHOOP_AWAKE_TIME_IN_MIN_COL: constants.AWAKE_DURATION_IN_MS_COL,
            WHOOP_SLEEP_DURATION_IN_MIN_COL: constants.DURATION_IN_MS_COL,
            WHOOP_REM_SLEEP_DURATION_IN_MIN_COL: constants.REM_SLEEP_DURATION_IN_MS_COL,
            WHOOP_DEEP_SLEEP_DURATION_IN_MIN_COL: constants.DEEP_SLEEP_DURATION_IN_MS_COL,
            WHOOP_LIGHT_SLEEP_DURATION_IN_MIN_COL: constants.LIGHT_SLEEP_DURATION_IN_MS_COL,
        }
    )
    for col in [
        constants.DURATION_IN_MS_COL,
        constants.AWAKE_DURATION_IN_MS_COL,
        constants.REM_SLEEP_DURATION_IN_MS_COL,
        constants.DEEP_SLEEP_DURATION_IN_MS_COL,
        constants.LIGHT_SLEEP_DURATION_IN_MS_COL,
    ]:
        sleep_summary[col] = sleep_summary[col] * 60 * 1000
    # Get calendarDate
    sleep_summary[constants.CALENDAR_DATE_COL] = sleep_summary[
        WHOOP_SLEEP_END_COL
    ].dt.floor(freq="D")
    # Sort values
    sleep_summary = sleep_summary.sort_values(by=constants.CALENDAR_DATE_COL)
    if start_date is None:
        start_date = sleep_summary[constants.CALENDAR_DATE_COL].min()
    if end_date is None:
        end_date = sleep_summary[constants.CALENDAR_DATE_COL].max()
    # Filter by date
    sleep_summary = (
        sleep_summary.set_index(constants.CALENDAR_DATE_COL)
        .truncate(before=start_date, after=end_date)
        .reset_index(names=[constants.CALENDAR_DATE_COL])
    )
    return sleep_summary


def load_daily_summary(data_folder, start_date, end_date) -> pd.DataFrame:
    """Load and format Whoop daily data.

    Parameters
    ----------
    data_folder : os.PathLike
        Folder containing Whoop daily CSV file.
    start_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        Start date with which daily data have to be filtered (inclusive), by default None
    end_date : Union[datetime.datetime, datetime.date, str, pd.Timestamp, None], optional
        End date with which daily data have to be filtered (exclusive), by default None

    Returns
    -------
    pd.DataFrame
        Formatted Whoop daily data.

    Raises
    ------
    FileNotFoundError
        If folder does not exist or if daily data are not found inside folder.
    """
    if not Path(data_folder).exists():
        raise FileNotFoundError(f"Folder {data_folder} does not exist.")
    # Path to daily summary
    path_to_daily_summary = Path(data_folder) / WHOOP_DAILY_DATA_FILENAME
    if not path_to_daily_summary.exists():
        raise FileNotFoundError(f"File {path_to_daily_summary} does not exist.")
    # Read CSV file
    daily_summary = pd.read_csv(
        path_to_daily_summary,
        parse_dates=[WHOOP_CYCLE_START_COL, WHOOP_SLEEP_START_COL, WHOOP_SLEEP_END_COL],
    )
    daily_summary[constants.CALENDAR_DATE_COL] = daily_summary[
        WHOOP_SLEEP_END_COL
    ].dt.floor(freq="D")

    daily_summary = daily_summary.sort_values(by=constants.CALENDAR_DATE_COL)
    if start_date is None:
        start_date = daily_summary[constants.CALENDAR_DATE_COL].min()
    if end_date is None:
        end_date = daily_summary[constants.CALENDAR_DATE_COL].max()
    # Filter by date
    daily_summary = (
        daily_summary.set_index(constants.CALENDAR_DATE_COL)
        .sort_index()
        .truncate(before=start_date, after=end_date)
        .reset_index(names=[constants.CALENDAR_DATE_COL])
    )
    return daily_summary
