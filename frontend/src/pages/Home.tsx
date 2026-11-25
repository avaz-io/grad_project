import { Link } from "react-router-dom";

import { useLanguage } from "../context/LanguageContext";
import styles from "./Home.module.css";
import page from "./Page.module.css";

// The four parts of Mentoria. Title and text come from the translation files.
const SECTIONS = [
  { to: "/courses", title: "nav.courses", text: "home.coursesText" },
  { to: "/tutors", title: "nav.tutors", text: "home.tutorsText" },
  { to: "/mentors", title: "nav.mentors", text: "home.mentorsText" },
  { to: "/lectures", title: "nav.lectures", text: "home.lecturesText" },
];

export default function Home() {
  const { t } = useLanguage();

  return (
    <>
      <section className={styles.hero}>
        <h1>{t("home.title")}</h1>
        <p>{t("home.tagline")}</p>
        <div className={styles.actions}>
          <Link to="/courses" className={page.button}>
            {t("home.ctaCourses")}
          </Link>
          <Link to="/tutors" className={page.buttonOutline}>
            {t("home.ctaTutors")}
          </Link>
        </div>
      </section>

      <section>
        <h2>{t("home.sectionsTitle")}</h2>
        <div className={styles.sections}>
          {SECTIONS.map((section) => (
            <Link key={section.to} to={section.to} className={styles.sectionCard}>
              <h3>{t(section.title)}</h3>
              <p>{t(section.text)}</p>
              <span className={styles.open}>{t("home.open")}</span>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
