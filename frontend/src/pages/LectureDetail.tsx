import { Link, useParams } from "react-router-dom";

import { getLecture } from "../api/client";
import type { Lecture } from "../api/types";
import { useApi } from "../api/useApi";
import DataState from "../components/DataState";
import InfoList, { type Field } from "../components/InfoList";
import { useLanguage } from "../context/LanguageContext";
import { formatDateTime, subjectName } from "../utils/format";
import styles from "./Detail.module.css";

// /lectures/:id: a free lecture. Live lectures also show their start date.
export default function LectureDetail() {
  const { id = "" } = useParams();
  const { language, t } = useLanguage();
  const lecture = useApi(() => getLecture(id), [id]);

  function fields(item: Lecture): Field[] {
    const result: Field[] = [
      { label: t("fields.type"), value: t(`lectures.${item.lecture_type}`) },
      { label: t("fields.subject"), value: subjectName(item.subject, language) },
      { label: t("fields.language"), value: t(`languageNames.${item.language}`) },
    ];
    if (item.starts_at) {
      result.push({ label: t("fields.startsAt"), value: formatDateTime(item.starts_at, language) });
    }
    if (item.duration_minutes) {
      result.push({ label: t("fields.duration"), value: t("common.minutes", { count: item.duration_minutes }) });
    }
    if (item.speaker_name) {
      result.push({ label: t("fields.speaker"), value: item.speaker_name });
    }
    return result;
  }

  return (
    <>
      <Link to="/lectures" className={styles.back}>
        {t("common.back")}
      </Link>

      <DataState
        loading={lecture.loading}
        error={lecture.error}
        notFound={lecture.notFound}
        onRetry={lecture.retry}
      >
        {lecture.data && (
          <>
            <section className={styles.panel}>
              <div className={styles.titleRow}>
                <h1>{lecture.data.title}</h1>
                <span className={styles.tag}>{t(`lectures.${lecture.data.lecture_type}`)}</span>
              </div>
              <InfoList fields={fields(lecture.data)} />
            </section>

            {lecture.data.description && (
              <section className={styles.panel}>
                <h2>{t("lectures.about")}</h2>
                <p className={styles.text}>{lecture.data.description}</p>
              </section>
            )}
          </>
        )}
      </DataState>
    </>
  );
}
