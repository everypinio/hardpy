// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import Backend from "i18next-http-backend";

const initializeI18n = async () => {
  try {
    const res = await fetch("/api/hardpy_config");
    const data = await res.json();
    const langFromConfig = data.frontend?.language ?? "en";

    await i18n
      .use(Backend)
      .use(initReactI18next)
      .init({
        lng: langFromConfig,
        fallbackLng: "en",
        debug: false,
        interpolation: {
          escapeValue: false,
        },
        backend: {
          loadPath: "/locales/{{lng}}/translation.json",
        },
      });

    console.log("i18n initialized with:", i18n.language);
  } catch (e) {
    console.error("Error initializing i18n:", e);
    // Provide a fallback value or take some other action to recover from the error
    await i18n
      .use(Backend)
      .use(initReactI18next)
      .init({
        lng: "en",
        fallbackLng: "en",
        debug: false,
        interpolation: {
          escapeValue: false,
        },
        backend: {
          loadPath: "/locales/{{lng}}/translation.json",
        },
      });
    console.log("i18n initialized with:", i18n.language);
  }
};

initializeI18n();

export default i18n;
