"""Named indicator templates: saving, loading, and the UI that drives them."""

import json
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication

from backtester.indicators import loader
from backtester.ui import indicator_templates as templates
from backtester.ui.chart_tab import ChartTab
from backtester.ui.indicators_dialog import NO_TEMPLATE, IndicatorsDialog


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def template_dir(tmp_path, monkeypatch):
    """Keep every test's templates in its own folder."""
    monkeypatch.setattr(templates, "template_dir", lambda: tmp_path)
    return tmp_path


def some_indicators(count: int = 2) -> list:
    registry, _errors = loader.discover()
    names = sorted(registry)[:count]
    return [registry[name][0]() for name in names]


# ------------------------------------------------------------ serialisation


def test_spec_round_trips_through_build():
    original = some_indicators(3)
    rebuilt, skipped = templates.build(templates.to_spec(original))
    assert skipped == []
    assert [i.display_name for i in rebuilt] == [i.display_name for i in original]
    assert [i.values() for i in rebuilt] == [i.values() for i in original]


def test_spec_keeps_edited_parameters():
    registry, _errors = loader.discover()
    ssl = registry["SSL Channel"][0](period=27, nrtr=False)
    rebuilt, skipped = templates.build(templates.to_spec([ssl]))
    assert skipped == []
    assert rebuilt[0].p.period == 27 and rebuilt[0].p.nrtr is False


def test_build_skips_an_indicator_that_no_longer_exists():
    built, skipped = templates.build(
        [{"name": "SSL Channel", "params": {}}, {"name": "Long Gone", "params": {}}]
    )
    assert len(built) == 1
    assert len(skipped) == 1 and "Long Gone" in skipped[0]


def test_build_skips_a_parameter_that_no_longer_exists():
    built, skipped = templates.build(
        [{"name": "SSL Channel", "params": {"removed_option": 3}}]
    )
    assert built == []
    assert len(skipped) == 1 and "removed_option" in skipped[0]


# -------------------------------------------------------------------- files


def test_save_and_load_a_template(template_dir):
    saved = some_indicators(2)
    path = templates.save_template("Trend setup", saved)
    assert path.exists() and path.parent == template_dir

    loaded, skipped = templates.load_template("Trend setup")
    assert skipped == []
    assert [i.display_name for i in loaded] == [i.display_name for i in saved]


def test_template_file_is_readable_json(template_dir):
    templates.save_template("Trend setup", some_indicators(1))
    data = json.loads((template_dir / "Trend setup.json").read_text(encoding="utf-8"))
    assert data["format"] == templates.FORMAT
    assert data["name"] == "Trend setup" and data["saved"]
    assert isinstance(data["indicators"], list) and data["indicators"]


def test_listing_uses_the_name_inside_the_file(template_dir):
    templates.save_template("My/Setup: 2", some_indicators(1))
    # The filename is sanitised, but the listed name is the one you typed.
    assert templates.list_templates() == ["My/Setup: 2"]
    assert not (template_dir / "My/Setup: 2.json").exists()


def test_saving_the_same_name_replaces_it(template_dir):
    templates.save_template("Setup", some_indicators(3))
    templates.save_template("Setup", some_indicators(1))
    assert templates.list_templates() == ["Setup"]
    loaded, _skipped = templates.load_template("Setup")
    assert len(loaded) == 1


def test_an_empty_template_is_allowed(template_dir):
    """Saving nothing is a legitimate "clear the chart" template."""
    templates.save_template("Clean", [])
    loaded, skipped = templates.load_template("Clean")
    assert loaded == [] and skipped == []


def test_delete_and_exists(template_dir):
    templates.save_template("Temporary", some_indicators(1))
    assert templates.exists("Temporary")
    assert templates.delete_template("Temporary")
    assert not templates.exists("Temporary")
    assert templates.list_templates() == []
    assert not templates.delete_template("Temporary")   # already gone


def test_loading_a_missing_template_reports_instead_of_raising(template_dir):
    loaded, skipped = templates.load_template("Nothing here")
    assert loaded == [] and len(skipped) == 1


def test_a_corrupt_template_reports_instead_of_raising(template_dir):
    (template_dir / "Broken.json").write_text("{not json", encoding="utf-8")
    loaded, skipped = templates.load_template("Broken")
    assert loaded == [] and "readable" in skipped[0]
    # It still lists, so the user can see and delete it.
    assert templates.list_templates() == ["Broken"]


def test_a_template_without_an_indicator_list_is_rejected(template_dir):
    (template_dir / "Odd.json").write_text('{"name": "Odd"}', encoding="utf-8")
    loaded, skipped = templates.load_template("Odd")
    assert loaded == [] and "indicator list" in skipped[0]


def test_listing_an_absent_folder_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(templates, "template_dir", lambda: tmp_path / "missing")
    assert templates.list_templates() == []


# ------------------------------------------------------------------- dialog


def test_dialog_saves_loads_and_deletes(qapp, template_dir, monkeypatch):
    dialog = IndicatorsDialog(some_indicators(2))
    assert dialog.template_combo.currentText() == NO_TEMPLATE

    monkeypatch.setattr(
        "backtester.ui.indicators_dialog.QInputDialog.getText",
        lambda *args, **kwargs: ("Saved set", True),
    )
    dialog._save_template()
    assert dialog.template_combo.currentText() == "Saved set"
    assert templates.exists("Saved set")

    # Loading it back replaces whatever is attached.
    dialog._clear()
    assert dialog.attached.count() == 0
    dialog._load_template()
    assert dialog.attached.count() == 2

    from PySide6.QtWidgets import QMessageBox

    monkeypatch.setattr(
        "backtester.ui.indicators_dialog.QMessageBox.question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    dialog._delete_template()
    assert not templates.exists("Saved set")
    assert dialog.template_combo.currentText() == NO_TEMPLATE


def test_dialog_save_is_cancellable(qapp, template_dir, monkeypatch):
    dialog = IndicatorsDialog(some_indicators(1))
    monkeypatch.setattr(
        "backtester.ui.indicators_dialog.QInputDialog.getText",
        lambda *args, **kwargs: ("", False),
    )
    dialog._save_template()
    assert templates.list_templates() == []


def test_dialog_reports_what_a_template_skipped(qapp, template_dir):
    (template_dir / "Stale.json").write_text(
        json.dumps({"indicators": [{"name": "Long Gone", "params": {}}]}),
        encoding="utf-8",
    )
    dialog = IndicatorsDialog([])
    dialog.refresh_templates(select="Stale")
    dialog._load_template()
    assert "Long Gone" in dialog.error_label.text()


# ----------------------------------------------------------------- chart tab


def test_chart_tab_applies_a_template(qapp, template_dir, tmp_path):
    from backtester.data.store import DataStore

    templates.save_template("Two", some_indicators(2))
    tab = ChartTab(DataStore(tmp_path / "library"))
    tab.refresh_templates()
    assert tab.template_combo.findText("Two") > 0

    emitted = []
    tab.indicators_changed.connect(emitted.append)
    tab.template_combo.setCurrentText("Two")

    assert len(tab.indicators) == 2
    assert emitted and len(emitted[0]) == 2


def test_chart_tab_ignores_the_placeholder(qapp, template_dir, tmp_path):
    from backtester.data.store import DataStore

    tab = ChartTab(DataStore(tmp_path / "library"))
    tab.set_indicators(some_indicators(1))
    tab.template_combo.setCurrentText(NO_TEMPLATE)
    assert len(tab.indicators) == 1          # selecting "(none)" changes nothing
