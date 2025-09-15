// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { useTranslation } from "react-i18next";

import PouchDB from "pouchdb-browser";
import { Provider } from "use-pouchdb";

import "normalize.css";
import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";
import "./i18n";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

function ErrorMessage() {
  const { t } = useTranslation();

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>{t("error.dbConnectionTitle")}</h1>
      <p>{t("error.dbConnectionMessage")}</p>
    </div>
  );
}

/**
 * Fetches the synchronization URL for PouchDB from the backend API.
 *
 * @returns {Promise<string | undefined>} A promise that resolves to the sync URL as a string if successful,
 * or undefined if an error occurs.
 * @throws {Error} If the fetch request fails or the response cannot be parsed.
 */
async function getSyncURL(): Promise<string | undefined> {
  try {
    const response = await fetch("/api/couch");
    const data = await response.json();
    return `${data.connection_str}/statestore`;
  } catch (error) {
    console.error(error);
    return undefined;
  }
}

/**
 * Gets the syncronization document ID from the backend API.
 * @returns {Promise<string>} A promise that resolves to the sync document ID as a string.
 */
async function getDatabaseDocumentId(): Promise<string> {
  try {
    const response = await fetch("/api/database_document_id");
    const data = await response.json();
    return data.document_id;
  } catch (error) {
    console.error(error);
    return "current";
  }
}

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

const syncURL = await getSyncURL();
if (syncURL !== undefined) {
  const db = new PouchDB(syncURL);

  const syncDocumentId = await getDatabaseDocumentId();

  /**
   * Renders the main application wrapped in a PouchDB Provider and React StrictMode.
   *
   * @param {PouchDB.Database} db - The PouchDB database instance to be provided to the application.
   */
  root.render(
    <StrictMode>
      <Provider pouchdb={db}>
        <App syncDocumentId={syncDocumentId} />
      </Provider>
    </StrictMode>
  );
} else {
  /**
   * Renders an error message if the PouchDB sync URL could not be retrieved.
   */
  root.render(
    <StrictMode>
      <ErrorMessage />
    </StrictMode>
  );
}

if (process.env.NODE_ENV !== "development") {
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  console.log = function () {};
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  console.debug = function () {};
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
