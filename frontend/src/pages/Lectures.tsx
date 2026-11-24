import { getLectures } from "../api/client";
import type { Lecture } from "../api/types";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatDateTime, subjectName } from "../utils/format";
import page from "./Page.module.css";

export default function Lectures() {
  const { language, t } = useLanguage();
  const lectures = useApi(getLectures);

  // Only add the lines we have data for (subject, start time and speaker can be empty).
  function details(lecture: Lecture): string[] {
    const lines: string[] = [];
    if (lecture.subject) lines.push(subjectName(lecture.subject, language));
    lines.push(t(`languageNames.${lecture.language}`));
    if (lecture.starts_at) {
      lines.push(t("lectures.startsAt", { date: formatDateTime(lecture.starts_at, language) }));
    }
    if (lecture.speaker_name) lines.push(t("common.speaker", { name: lecture.speaker_name }));
    return lines;
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
              title={lecture.title}
              tag={t(`lectures.${lecture.lecture_type}`)}
              details={details(lecture)}
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
