// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { StrictMode } from 'react';
import ReactDOM from "react-dom/client";

import PouchDB from 'pouchdb-browser'
import { Provider } from 'use-pouchdb'

import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

function getSyncURL() {
  return fetch("/api/couch")
    .then(response => response.json())
    .then(data => `${data.connection_str}/statestore`)
    .catch(error => {
      console.error(error);
      undefined
    });
}

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);

const syncURL = await getSyncURL();
if (syncURL !== undefined) {
  const db = new PouchDB(syncURL);

  root.render(
    <StrictMode>
      <Provider pouchdb={db}>
        <App />
      </Provider>
    </StrictMode>
  );
} else {
  root.render(
    <>
        <h1>No PouchDB sync URL</h1>
        <p>Getting the URL from a backend was failed</p>
    </>
  );
}


if (process.env.NODE_ENV !== 'development') {
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  console.log = function () { };
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  console.debug = function () { };
}


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
