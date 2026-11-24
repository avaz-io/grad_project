import { useLanguage } from "../context/LanguageContext";
import styles from "./Footer.module.css";

export default function Footer() {
  const { t } = useLanguage();
  const year = new Date().getFullYear();

  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <p>
          <strong>
            © {year} {t("appName")}
          </strong>{" "}
          · {t("footer.about")}
        </p>
        <p className={styles.muted}>{t("footer.project")}</p>
      </div>
    </footer>
  );
}
