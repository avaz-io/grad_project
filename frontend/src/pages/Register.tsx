import { Link } from "react-router-dom";

import { useLanguage } from "../context/LanguageContext";
import page from "./Page.module.css";

// Placeholder: the real form will call the registration API (Iteration 1, Week 14).
export default function Register() {
  const { t } = useLanguage();

  return (
    <div className={page.centerBox}>
      <h1>{t("auth.registerTitle")}</h1>
      <p>{t("auth.comingSoon")}</p>
      <Link to="/login">{t("auth.toLogin")}</Link>
    </div>
  );
}
