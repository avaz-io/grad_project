import { Link } from "react-router-dom";

import { useLanguage } from "../context/LanguageContext";
import page from "./Page.module.css";

// Placeholder: the real form will call the JWT login API (Iteration 1, Week 14).
export default function Login() {
  const { t } = useLanguage();

  return (
    <div className={page.centerBox}>
      <h1>{t("auth.loginTitle")}</h1>
      <p>{t("auth.comingSoon")}</p>
      <Link to="/register">{t("auth.toRegister")}</Link>
    </div>
  );
}
