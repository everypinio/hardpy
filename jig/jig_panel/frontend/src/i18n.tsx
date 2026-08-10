// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import Backend from "i18next-http-backend";

const FALLBACK_LANGUAGE = "en";

const readLanguage = async (): Promise<string> => {
  try {
    const res = await fetch("/api/jig_config");
    const data = await res.json();
    return data.frontend?.language ?? FALLBACK_LANGUAGE;
  } catch (e) {
    console.error("Error reading the panel language:", e);
    return FALLBACK_LANGUAGE;
  }
};

const initializeI18n = async () => {
  await i18n
    .use(Backend)
    .use(initReactI18next)
    .init({
      lng: await readLanguage(),
      fallbackLng: FALLBACK_LANGUAGE,
      debug: false,
      interpolation: {
        escapeValue: false,
      },
      backend: {
        loadPath: "/locales/{{lng}}/translation.json",
        // Translations must be revalidated against the server: a browser
        // serving them from its cache renders the keys of a newer panel build.
        requestOptions: { cache: "no-cache" },
      },
    });

  console.log("i18n initialized with:", i18n.language);
};

initializeI18n();

export default i18n;
