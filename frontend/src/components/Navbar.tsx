import { useState } from "react";
import { Link, NavLink } from "react-router-dom";

import { Language, useLanguage } from "../context/LanguageContext";
import styles from "./Navbar.module.css";

const SECTION_LINKS = [
  { to: "/courses", key: "nav.courses" },
  { to: "/tutors", key: "nav.tutors" },
  { to: "/mentors", key: "nav.mentors" },
  { to: "/lectures", key: "nav.lectures" },
];

const LANGUAGES: Language[] = ["en", "uz"];

// NavLink tells us if its page is open, so we can highlight it.
function linkClass({ isActive }: { isActive: boolean }) {
  return isActive ? `${styles.link} ${styles.active}` : styles.link;
}

export default function Navbar() {
  const { language, setLanguage, t } = useLanguage();
  // On small screens the links are hidden behind a "Menu" button.
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);

  return (
    <header className={styles.header}>
      <nav className={styles.inner}>
        <Link to="/" className={styles.logo} onClick={closeMenu}>
          {t("appName")}
        </Link>

        <button
          type="button"
          className={styles.menuButton}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰ {t("nav.menu")}
        </button>

        <div className={menuOpen ? `${styles.menu} ${styles.open}` : styles.menu}>
          <div className={styles.links}>
            {SECTION_LINKS.map((link) => (
              <NavLink key={link.to} to={link.to} className={linkClass} onClick={closeMenu}>
                {t(link.key)}
              </NavLink>
            ))}
          </div>

          <div className={styles.actions}>
            <NavLink to="/login" className={linkClass} onClick={closeMenu}>
              {t("nav.login")}
            </NavLink>
            <NavLink to="/register" className={styles.registerButton} onClick={closeMenu}>
              {t("nav.register")}
            </NavLink>

            <div className={styles.languageSwitch} role="group" aria-label={t("nav.language")}>
              {LANGUAGES.map((code) => (
                <button
                  key={code}
                  type="button"
                  className={code === language ? styles.languageActive : styles.languageButton}
                  aria-pressed={code === language}
                  onClick={() => setLanguage(code)}
                >
                  {code.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
}
