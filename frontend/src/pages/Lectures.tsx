import { getLectures } from "../api/client";
import type { Lecture } from "../api/types";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import type { Field } from "../components/InfoList";
import { useLanguage } from "../context/LanguageContext";
import { formatDateTime, subjectName } from "../utils/format";
import page from "./Page.module.css";

export default function Lectures() {
  const { language, t } = useLanguage();
  const lectures = useApi(getLectures);

  // Start time and speaker are only shown when the lecture has them.
  function fields(lecture: Lecture): Field[] {
    const result: Field[] = [
      { label: t("fields.subject"), value: subjectName(lecture.subject, language) },
      { label: t("fields.language"), value: t(`languageNames.${lecture.language}`) },
    ];
    if (lecture.starts_at) {
      result.push({ label: t("fields.startsAt"), value: formatDateTime(lecture.starts_at, language) });
    }
    if (lecture.speaker_name) {
      result.push({ label: t("fields.speaker"), value: lecture.speaker_name });
    }
    return result;
  }

  return (
    <>
      <div className={page.header}>
        <h1>{t("lectures.title")}</h1>
        <p>{t("lectures.subtitle")}</p>
      </div>

      <DataState
        loading={lectures.loading}
        error={lectures.error}
        empty={lectures.data?.length === 0}
        onRetry={lectures.retry}
      >
        <div className={page.grid}>
          {lectures.data?.map((lecture) => (
            <Card
              key={lecture.id}
              to={`/lectures/${lecture.id}`}
              title={lecture.title}
              tag={t(`lectures.${lecture.lecture_type}`)}
              fields={fields(lecture)}
              footerLeft={t("common.free")}
              footerRight={
                lecture.duration_minutes
                  ? t("common.minutes", { count: lecture.duration_minutes })
                  : undefined
              }
            />
          ))}
        </div>
      </DataState>
    </>
  );
}
