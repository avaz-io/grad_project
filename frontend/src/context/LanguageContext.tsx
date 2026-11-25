import { createContext, ReactNode, useContext, useEffect, useState } from "react";

import en from "../i18n/en.json";
import uzJson from "../i18n/uz.json";

export type Language = "en" | "uz";
type Translations = typeof en;

// Giving uz.json the same type as en.json makes the build fail
// if a key exists in English but is missing in Uzbek.
const uz: Translations = uzJson;
const translations: Record<Language, Translations> = { en, uz };

const STORAGE_KEY = "mentoria.language";

export type TranslateParams = Record<string, string | number>;
export type Translate = (key: string, params?: TranslateParams) => string;

type LanguageContextValue = {
  language: Language;
  setLanguage: (language: Language) => void;
  // t("nav.courses") returns the text in the current language.
  // t("common.lessons", { count: 4 }) also fills in "{count}".
  t: Translate;
};

const LanguageContext = createContext<LanguageContextValue | null>(null);

// Follows a dotted key like "nav.courses" through the nested JSON object.
function lookup(dictionary: Translations, key: string): string | undefined {
  let value: unknown = dictionary;
  for (const part of key.split(".")) {
    if (typeof value !== "object" || value === null) {
      return undefined;
    }
    value = (value as Record<string, unknown>)[part];
  }
  return typeof value === "string" ? value : undefined;
}

function savedLanguage(): Language {
  return localStorage.getItem(STORAGE_KEY) === "uz" ? "uz" : "en";
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(savedLanguage);

  // Remember the choice and tell the browser which language the page is in.
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, language);
    document.documentElement.lang = language;
  }, [language]);

  function t(key: string, params: TranslateParams = {}): string {
    // A missing key shows the key itself, so the mistake is easy to spot.
    let text = lookup(translations[language], key) ?? key;
    for (const [name, value] of Object.entries(params)) {
      text = text.split(`{${name}}`).join(String(value));
    }
    return text;
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextValue {
  const context = useContext(LanguageContext);
  if (context === null) {
    throw new Error("useLanguage must be used inside <LanguageProvider>");
  }
  return context;
}
