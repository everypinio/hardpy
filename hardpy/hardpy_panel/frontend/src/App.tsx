// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";

import {
  Button,
  Navbar,
  Alignment,
  Classes,
  Colors,
  Menu,
  MenuItem,
  H2,
  Popover,
  Card,
  Divider,
} from "@blueprintjs/core";

import StartStopButton from "./button/StartStop";
import { TestRunI } from "./hardpy_test_view/SuiteList";
import SuiteList from "./hardpy_test_view/SuiteList";
import ProgressView from "./progress/ProgressView";
import TestStatus from "./hardpy_test_view/TestStatus";
import ReloadAlert from "./restart_alert/RestartAlert";
import PlaySound from "./hardpy_test_view/PlaySound";

import { useAllDocs } from "use-pouchdb";

import "./App.css";

const WINDOW_WIDTH_THRESHOLDS = {
  ULTRAWIDE: 490,
  WIDE: 400,
};

/**
 * Main component of the GUI.
 * @returns {JSX.Element} The main application component.
 */
function App(): JSX.Element {
  const { t, i18n } = useTranslation();
  const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
  const [use_debug_info, setUseDebugInfo] = React.useState(false);

  const [lastRunStatus, setLastRunStatus] = React.useState("");
  const [lastProgress, setProgress] = React.useState(0);
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('hardpy-language', lang);
  };

  /**
   * Custom hook to determine if the window width is greater than a specified size.
   * @param {number} size - The width threshold to compare against.
   * @returns {boolean} True if the window width is greater than the specified size, otherwise false.
   */
  const useWindowWide = (size: number): boolean => {
    const [width, setWidth] = React.useState(0);

    React.useEffect(() => {
      function handleResize() {
        setWidth(window.innerWidth);
      }

      window.addEventListener("resize", handleResize);

      handleResize();

      return () => {
        window.removeEventListener("resize", handleResize);
      };
    }, [setWidth]);

    return width > size;
  };

  const ultrawide = useWindowWide(WINDOW_WIDTH_THRESHOLDS.ULTRAWIDE);
  const wide = useWindowWide(WINDOW_WIDTH_THRESHOLDS.WIDE);

  /**
   * Custom hook to render data from the database.
   * @returns {JSX.Element} The rendered database content or a loading/error message.
   */
  const useRenderDb = (): JSX.Element => {
    const { rows, state, loading, error } = useAllDocs({
      include_docs: true,
    });

    React.useEffect(() => {
      if (state === "error") {
        setIsAuthenticated(false);
      } else if (isAuthenticated === false) {
        setIsAuthenticated(true);
      }
    }, [state]);

    if (loading && rows.length === 0) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t('app.connection')}</H2>
        </Card>
      );
    }

    if (state === "error") {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t('app.dbError')}</H2>
          {error && <p>{error.message}</p>}
        </Card>
      );
    }

    if (rows.length === 0) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t('app.noEntries')}</H2>
        </Card>
      );
    }


    /* Assume it is only one */
    const db_row = rows[0].doc as TestRunI;
    const status = db_row.status;
    if (status && status != lastRunStatus) {
      setLastRunStatus(status);
    }

    const progress = db_row.progress;
    if (progress && progress != lastProgress) {
      setProgress(progress);
    }

    return (
      <div style={{ marginTop: "40px" }}>
        {rows.map((row) => (
          <div key={row.id} style={{ display: "flex", flexDirection: "row" }}>
            {(ultrawide || !use_debug_info) && (
              <Card
                style={{
                  flexDirection: "column",
                  padding: "20px",
                  flexGrow: 1,
                  flexShrink: 1,
                  marginTop: "20px",
                  marginBottom: "20px",
                }}
              >
                <SuiteList
                  db_state={row.doc as TestRunI}
                  defaultClose={!ultrawide}
                ></SuiteList>
              </Card>
            )}
            {use_debug_info && (
              <Card
                style={{
                  flexDirection: "column",
                  padding: "20px",
                  marginTop: "20px",
                  marginBottom: "20px",
                }}
              >
                <pre>{JSON.stringify(row.doc, null, 2)}</pre>
              </Card>
            )}
          </div>
        ))}
      </div>
    );
  };

  /**
   * Renders the settings menu.
   * @returns {JSX.Element} The settings menu component.
   */
  const renderSettingsMenu = (): JSX.Element => {
    return (
      <Menu>
        <MenuItem
          shouldDismissPopover={false}
          text={use_end_test_sound ? t('app.soundOff') : t('app.soundOn')}
          icon={use_end_test_sound ? "volume-up" : "volume-off"}
          id="use_end_test_sound"
          onClick={() => setUseEndTestSound(!use_end_test_sound)}
        />
        <MenuItem
          shouldDismissPopover={false}
          text={use_debug_info ? t('app.debugOff') : t('app.debugOn')}
          icon={"bug"}
          id="use_debug_info"
          onClick={() => setUseDebugInfo(!use_debug_info)}
        />
        <Divider />
        <MenuItem text={t('app.language')} icon="translate">
          <MenuItem text="English" onClick={() => changeLanguage('en')} />
          <MenuItem text="中文" onClick={() => changeLanguage('ch')} />
          <MenuItem text="日本語" onClick={() => changeLanguage('ja')} />
          <MenuItem text="Español" onClick={() => changeLanguage('sp')} />
          <MenuItem text="Deutsch" onClick={() => changeLanguage('ge')} />
          <MenuItem text="Français" onClick={() => changeLanguage('fr')} />
          <MenuItem text="Русский" onClick={() => changeLanguage('ru')} />
        </MenuItem>
      </Menu>
    );
  };

  return (
    <div className="App" style={{ minWidth: "310px", margin: "auto" }}>
      {/* Popout elements */}
      <ReloadAlert reload_timeout_s={3} />
      {/* <Notification /> */}

      {/* Header */}
      <Navbar
        fixedToTop={true}
        style={{ background: Colors.LIGHT_GRAY4, margin: "auto" }}
      >
        <Navbar.Group align={Alignment.LEFT}>
          <Navbar.Heading id={"main-heading"}>
            <div className={"logo-smol"}></div>
              {wide && (
                <div>
                  <b>{ultrawide ? t('app.title') : "HardPy"}</b>
                </div>
              )}
          </Navbar.Heading>

          {wide && <Navbar.Divider />}

          <Navbar.Heading id={"last-exec-heading"}>
            <div>{t('app.lastRun')}</div>
          </Navbar.Heading>
          <div id={"glob-test-status"}>
            <TestStatus status={lastRunStatus} />
            {use_end_test_sound && (
              <PlaySound key="sound" status={lastRunStatus} />
            )}
          </div>

          <Navbar.Divider />
        </Navbar.Group>

        <Navbar.Group align={Alignment.RIGHT}>
          <Popover content={renderSettingsMenu()}>
            <Button className="bp3-minimal" icon="cog" />
          </Popover>
        </Navbar.Group>
      </Navbar>

      {/* Tests panel */}
      <div className={Classes.DRAWER_BODY} style={{ marginBottom: "60px" }}>
        {useRenderDb()}
      </div>

      {/* Footer */}

      <div
        className={Classes.DRAWER_FOOTER}
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "row",
          position: "fixed",
          bottom: 0,
          background: Colors.LIGHT_GRAY5,
          margin: "auto",
        }}
      >
        <div
          style={{
            flexDirection: "column",
            flexGrow: 1,
            flexShrink: 1,
            marginTop: "auto",
            marginBottom: "auto",
            padding: "20px",
          }}
        >
          <ProgressView percentage={lastProgress} status={lastRunStatus} />
        </div>
        <div style={{ flexDirection: "column" }}>
          <StartStopButton
            testing_status={lastRunStatus}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
