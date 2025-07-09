// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import Backend from "i18next-http-backend";

const LOCAL_STORAGE_KEY = "hardpy-language";

const initializeI18n = async () => {
  await i18n
    .use(Backend)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
      fallbackLng: "en",
      debug: false,
      interpolation: {
        escapeValue: false,
      },
      detection: {
        order: ["localStorage", "navigator"],
        caches: ["localStorage"],
        lookupLocalStorage: LOCAL_STORAGE_KEY,
      },
      backend: {
        loadPath: "/locales/{{lng}}/translation.json",
      },
    });

  try {
    const res = await fetch("/api/language");
    const data = await res.json();
    const langFromConfig = data.language ?? "en";

    const langFromLocalStorage = localStorage.getItem(LOCAL_STORAGE_KEY);

    if (!langFromLocalStorage) {
      await i18n.changeLanguage(langFromConfig);
      localStorage.setItem(LOCAL_STORAGE_KEY, langFromConfig);
    }
  } catch (e) {
    console.warn("Could not fetch backend language config, using fallback.");
  }

  console.log("i18n initialized with:", i18n.language);
};

initializeI18n();

export default i18n;
