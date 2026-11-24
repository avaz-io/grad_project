import { Link, useParams } from "react-router-dom";

import { getCourse } from "../api/client";
import { useApi } from "../api/useApi";
import DataState from "../components/DataState";
import InfoList from "../components/InfoList";
import { useLanguage } from "../context/LanguageContext";
import { formatPrice, subjectName } from "../utils/format";
import styles from "./Detail.module.css";

// /courses/:id: course information and its lesson outline (titles only).
export default function CourseDetail() {
  const { id = "" } = useParams();
  const { language, t } = useLanguage();
  const course = useApi(() => getCourse(id), [id]);

  return (
    <>
      <Link to="/courses" className={styles.back}>
        {t("common.back")}
      </Link>

      <DataState
        loading={course.loading}
        error={course.error}
        notFound={course.notFound}
        onRetry={course.retry}
      >
        {course.data && (
          <>
            <section className={styles.panel}>
              <div className={styles.titleRow}>
                <h1>{course.data.title}</h1>
              </div>
              <InfoList
                fields={[
                  { label: t("fields.subject"), value: subjectName(course.data.subject, language) },
                  { label: t("fields.level"), value: t(`levels.${course.data.level}`) },
                  {
                    label: t("fields.teachingLanguage"),
                    value: t(`languageNames.${course.data.language}`),
                  },
                  { label: t("fields.educator"), value: course.data.educator_name },
                  { label: t("fields.price"), value: formatPrice(course.data.price, t) },
                ]}
              />
              <div className={styles.actions}>
                <button type="button" className={styles.actionButton} disabled>
                  {t("courses.enrol")}
                </button>
                <span className={styles.note}>{t("common.comingSoon")}</span>
              </div>
            </section>

            {course.data.description && (
              <section className={styles.panel}>
                <h2>{t("courses.about")}</h2>
                <p className={styles.text}>{course.data.description}</p>
              </section>
            )}

            <section className={styles.panel}>
              <h2>{t("courses.lessonsTitle")}</h2>
              <ol className={styles.lessons}>
                {course.data.lessons.map((lesson) => (
                  <li key={lesson.id}>{lesson.title}</li>
                ))}
              </ol>
            </section>
          </>
        )}
      </DataState>
    </>
  );
}
