import json
from pathlib import Path

from pydantic import BaseModel


class Chart(BaseModel):
    """A class representing chart translations.

    Attributes:
        dataChart (str): The translation for the "dataChart" text.
        xAxis (str): The translation for the "xAxis" text.
        yAxis (str): The translation for the "yAxis" text.
        chart (str): The translation for the "chart" text.
        showChart (str): The translation for the "showChart" text.
        fullscreenButton (str): The translation for the "fullscreenButton" text.
        series (str): The translation for the "series" text.
    """

    dataChart: str
    xAxis: str
    yAxis: str
    chart: str
    showChart: str
    fullscreenButton: str
    series: str

class AppStatus(BaseModel):
    """A class representing application status translations.

    Attributes:
        ready (str): The translation for the "ready" status.
        run (str): The translation for the "run" status.
        passed (str): The translation for the "passed" status.
        failed (str): The translation for the "failed" status.
        stopped (str): The translation for the "stopped" status.
        unknown (str): The translation for the "unknown" status.
    """

    ready: str
    run: str
    passed: str
    failed: str
    stopped: str
    unknown: str


class OperatorDialog(BaseModel):
    """A class representing an operator dialog.

    It contains attributes for default title, image alt text, HTML code title, HTML link title,
    enter answer text, field not empty text, notification title, notification description,
    numeric input error text, radio button error text, and checkbox error text.

    Attributes:
        defaultTitle (str): The default title of the dialog.
        imageAlt (str): The alt text for the image in the dialog.
        htmlCodeTitle (str): The title for the HTML code in the dialog.
        htmlLinkTitle (str): The title for the HTML link in the dialog.
        enterAnswer (str): The text prompting the user to enter an answer.
        fieldNotEmpty (str): The text indicating that a field is not empty.
        notificationTitle (str): The title of the notification.
        notificationDesc (str): The description of the notification.
        numericInputError (str): The error message for numeric input.
        radioButtonError (str): The error message for radio button input.
        checkboxError (str): The error message for checkbox input.
    """

    defaultTitle: str
    imageAlt: str
    htmlCodeTitle: str
    htmlLinkTitle: str
    enterAnswer: str
    fieldNotEmpty: str
    notificationTitle: str
    notificationDesc: str
    numericInputError: str
    radioButtonError: str
    checkboxError: str


class Button(BaseModel):
    """A class representing a button.

    Attributes:
        start (str): The text for the start button.
        stop (str): The text for the stop button.
        confirm (str): The text for the confirm button.
    """

    start: str
    stop: str
    confirm: str


class Error(BaseModel):
    """A class representing an error.

    Attributes:
        dbConnectionTitle (str): The title of the database connection error.
        dbConnectionMessage (str): The message of the database connection error.
    """

    dbConnectionTitle: str
    dbConnectionMessage: str


class App(BaseModel):
    """A class representing the application.

    Attributes:
        title (str): The title of the application.
        lastLaunch (str): The last launch of the application.
        duration (str): The duration of the application.
        seconds (str): The text for seconds.
        soundOn (str): The text for the sound on button.
        soundOff (str): The text for the sound off button.
        debugOn (str): The text for the debug on button.
        debugOff (str): The text for the debug off button.
        connection (str): The connection status of the application.
        dbError (str): The database error message.
        noEntries (str): The message for no entries in the database.
        status (AppStatus): The status of the application.
    """

    title: str
    lastLaunch: str
    duration: str
    seconds: str
    soundOn: str
    soundOff: str
    debugOn: str
    debugOff: str
    connection: str
    dbError: str
    noEntries: str
    status: AppStatus
    testConfigurationSelector: str


class SuiteList(BaseModel):
    """A class representing a suite list.

    Attributes:
        loadingTests (str): The text for loading tests.
        refreshHint (str): The text for the refresh hint.
        standName (str): The text for the stand name.
        status (str): The text for the status.
        startTime (str): The text for the start time.
        finishTime (str): The text for the finish time.
        alert (str): The text for the alert.
    """

    loadingTests: str
    refreshHint: str
    standName: str
    status: str
    startTime: str
    finishTime: str
    alert: str


class _TestSuite(BaseModel):
    """A class representing a test suite.

    Attributes:
        nameColumn (str): The text for the name column.
        dataColumn (str): The text for the data column.
        loading (str): The text for the loading state.
        stubName (str): The text for the stub name.
    """

    nameColumn: str
    dataColumn: str
    loading: str
    stubName: str
    stubName: str
    runSelectedTests: str
    noTestsSelected: str
    testsStarted: str
    startError: str
    connectionError: str
    selectionColumn: str
    skipped: str


class TranslationModel(BaseModel):
    """A class representing a translation model.

    Attributes:
        app (App): The app translation data.
        button (Button): The button translation data.
        error (Error): The error translation data.
        chart (Chart): The chart translation data.
        operatorDialog (OperatorDialog): The operator dialog translation data.
        suiteList (SuiteList): The suite list translation data.
        testSuite (_TestSuite): The test suite translation data.
    """

    app: App
    button: Button
    error: Error
    chart: Chart
    operatorDialog: OperatorDialog
    suiteList: SuiteList
    testSuite: _TestSuite


def validate_translation_file(file_path: Path) -> list[str]:
    """Validate a single translation file against the model."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:  # noqa: PTH123, UP015
            data = json.load(f)

        # Validate against the model
        TranslationModel(**data)

    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {file_path}: {e!s}")
    except Exception as e:  # noqa: BLE001
        errors.append(f"Validation error in {file_path}: {e!s}")

    return errors


class TranslationError(Exception):
    """Exception raised when there's an issue with translations."""

    pass  # noqa: PIE790


def test_translation_files():
    """Test that all translation files have the correct structure."""
    locales_dir = Path("hardpy/hardpy_panel/frontend/public/locales")
    errors = []

    # Find all translation.json files
    translation_files = list(locales_dir.glob("*/translation.json"))

    if not translation_files:
        msg = "No translation files found"
        raise TranslationError(msg)

    for file_path in translation_files:
        file_errors = validate_translation_file(file_path)
        errors.extend(file_errors)

    if errors:
        error_msg = "\n".join(errors)
        msg = f"Translation validation failed:\n{error_msg}"
        raise AssertionError(msg)

    assert True
