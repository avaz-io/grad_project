import { Link } from "react-router-dom";

import { useLanguage } from "../context/LanguageContext";
import page from "./Page.module.css";

// Shown for any address that does not match a route in App.tsx.
export default function NotFound() {
  const { t } = useLanguage();

  return (
    <div className={page.centerBox}>
      <h1>404 · {t("notFound.title")}</h1>
      <p>{t("notFound.text")}</p>
      <Link to="/" className={page.button}>
        {t("notFound.back")}
      </Link>
    </div>
  );
}
