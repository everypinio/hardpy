// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

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
import { SuiteList, TestRunI } from "./hardpy_test_view/SuiteList";
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
  const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
  const [use_debug_info, setUseDebugInfo] = React.useState(false);

  const [lastRunStatus, setLastRunStatus] = React.useState("");
  const [lastProgress, setProgress] = React.useState(0);
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);

  const [language, setLanguage] = React.useState(
    localStorage.getItem('hardpy-language') || 'en'
  );

  const changeLanguage = (lang: string) => {
    setLanguage(lang);
    localStorage.setItem('hardpy-language', lang);
  };

  const translations = {
    en: {
      title: "HardPy Operator Panel",
      lastRun: "Last run:",
      soundOn: "Turn on the sound",
      soundOff: "Turn off the sound",
      debugOn: "Turn on the debug mode",
      debugOff: "Turn off the debug mode",
      language: "Language",
      connection: "Establishing a connection... 🧐🔎",
      dbError: "Database connection error. 🙅🏽‍♀️🚫",
      noEntries: "No entries in the database 🙅🏽‍♀️🚫"
    },
    ru: {
      title: "Панель оператора HardPy",
      lastRun: "Последний запуск:",
      soundOn: "Включить звук",
      soundOff: "Выключить звук",
      debugOn: "Включить режим отладки",
      debugOff: "Выключить режим отладки",
      language: "Язык",
      connection: "Установка соединения... 🧐🔎",
      dbError: "Ошибка подключения к базе данных. 🙅🏽‍♀️🚫",
      noEntries: "Нет записей в базе данных 🙅🏽‍♀️🚫"
    },
    zh: {
      title: "HardPy 操作面板",
      lastRun: "最后一次运行:",
      soundOn: "开启声音",
      soundOff: "关闭声音",
      debugOn: "开启调试模式",
      debugOff: "关闭调试模式",
      language: "语言",
      connection: "正在建立连接... 🧐🔎",
      dbError: "数据库连接错误. 🙅🏽‍♀️🚫",
      noEntries: "数据库中没有条目 🙅🏽‍♀️🚫"
    },
    ja: {
      title: "HardPy オペレーターパネル",
      lastRun: "最後の実行:",
      soundOn: "音をオンにする",
      soundOff: "音をオフにする",
      debugOn: "デバッグモードをオンにする",
      debugOff: "デバッグモードをオフにする",
      language: "言語",
      connection: "接続を確立しています... 🧐🔎",
      dbError: "データベース接続エラー. 🙅🏽‍♀️🚫",
      noEntries: "データベースにエントリがありません 🙅🏽‍♀️🚫"
    },
    es: {
      title: "Panel de operador HardPy",
      lastRun: "Última ejecución:",
      soundOn: "Activar sonido",
      soundOff: "Desactivar sonido",
      debugOn: "Activar modo de depuración",
      debugOff: "Desactivar modo de depuración",
      language: "Idioma",
      connection: "Estableciendo conexión... 🧐🔎",
      dbError: "Error de conexión a la base de datos. 🙅🏽‍♀️🚫",
      noEntries: "No hay entradas en la base de datos 🙅🏽‍♀️🚫"
    },
    de: {
      title: "HardPy Bedienfeld",
      lastRun: "Letzter Lauf:",
      soundOn: "Ton einschalten",
      soundOff: "Ton ausschalten",
      debugOn: "Debug-Modus einschalten",
      debugOff: "Debug-Modus ausschalten",
      language: "Sprache",
      connection: "Verbindung wird hergestellt... 🧐🔎",
      dbError: "Datenbankverbindungsfehler. 🙅🏽‍♀️🚫",
      noEntries: "Keine Einträge in der Datenbank 🙅🏽‍♀️🚫"
    },
    fr: {
      title: "Panneau opérateur HardPy",
      lastRun: "Dernière exécution:",
      soundOn: "Activer le son",
      soundOff: "Désactiver le son",
      debugOn: "Activer le mode débogage",
      debugOff: "Désactiver le mode débogage",
      language: "Langue",
      connection: "Établissement de la connexion... 🧐🔎",
      dbError: "Erreur de connexion à la base de données. 🙅🏽‍♀️🚫",
      noEntries: "Aucune entrée dans la base de données 🙅🏽‍♀️🚫"
    }
  };

  type TranslationKey = 
    | 'title' 
    | 'lastRun' 
    | 'soundOn' 
    | 'soundOff' 
    | 'debugOn' 
    | 'debugOff' 
    | 'language' 
    | 'connection' 
    | 'dbError' 
    | 'noEntries';

  const t = (key: TranslationKey) => (translations as any)[language][key] || translations.en[key];

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
          <H2>{t('connection')}</H2>
        </Card>
      );
    }

    if (state === "error") {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t('dbError')}</H2>
          {error && <p>{error.message}</p>}
        </Card>
      );
    }

    if (rows.length === 0) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t('noEntries')}</H2>
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
          text={use_end_test_sound ? t('soundOff') : t('soundOn')}
          icon={use_end_test_sound ? "volume-up" : "volume-off"}
          id="use_end_test_sound"
          onClick={() => setUseEndTestSound(!use_end_test_sound)}
        />
        <MenuItem
          shouldDismissPopover={false}
          text={use_debug_info ? t('debugOff') : t('debugOn')}
          icon={"bug"}
          id="use_debug_info"
          onClick={() => setUseDebugInfo(!use_debug_info)}
        />
        <Divider />
        <MenuItem text={t('language')} icon="translate">
          <MenuItem text="English" onClick={() => changeLanguage('en')} />
          <MenuItem text="Русский" onClick={() => changeLanguage('ru')} />
          <MenuItem text="中文" onClick={() => changeLanguage('zh')} />
          <MenuItem text="日本語" onClick={() => changeLanguage('ja')} />
          <MenuItem text="Español" onClick={() => changeLanguage('es')} />
          <MenuItem text="Deutsch" onClick={() => changeLanguage('de')} />
          <MenuItem text="Français" onClick={() => changeLanguage('fr')} />
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
                  <b>{ultrawide ? t('title') : "HardPy"}</b>
                </div>
              )}
          </Navbar.Heading>

          {wide && <Navbar.Divider />}

          <Navbar.Heading id={"last-exec-heading"}>
            <div>{t('lastRun')}</div>
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
