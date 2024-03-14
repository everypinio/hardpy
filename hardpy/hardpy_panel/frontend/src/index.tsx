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
    .then(data => `${data.connection_str}/statestore`);
}

getSyncURL()
  .then(syncURL => {
    const db = new PouchDB(syncURL);
    const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);

    root.render(
      <StrictMode>
        <Provider pouchdb={db}>
          <App />
        </Provider>
      </StrictMode>
    );
  })
  .catch(error => {
    console.error(error);
  });


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
