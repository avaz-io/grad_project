import { getTutors } from "../api/client";
import type { TutorSubject } from "../api/types";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatPrice, formatRating, subjectName } from "../utils/format";
import page from "./Page.module.css";

export default function Tutors() {
  const { language, t } = useLanguage();
  const tutors = useApi(getTutors);

  // "English (A1 – B2)": the subject and the range of levels the tutor teaches.
  const describeSubject = (subject: TutorSubject) =>
    `${subjectName(subject, language)} (${t(`levels.${subject.min_level}`)} – ${t(
      `levels.${subject.max_level}`
    )})`;

  return (
    <>
      <div className={page.header}>
        <h1>{t("tutors.title")}</h1>
        <p>{t("tutors.subtitle")}</p>
      </div>

      <DataState
        loading={tutors.loading}
        error={tutors.error}
        empty={tutors.data?.length === 0}
        onRetry={tutors.retry}
      >
        <div className={page.grid}>
          {tutors.data?.map((tutor) => (
            <Card
              key={tutor.id}
              title={tutor.name}
              details={[
                ...tutor.subjects.map(describeSubject),
                formatLanguages(tutor.languages, t),
              ]}
              footerLeft={t("common.pricePerHour", { price: formatPrice(tutor.hourly_rate, t) })}
              footerRight={formatRating(tutor.rating_avg, tutor.rating_count, t)}
            />
          ))}
        </div>
      </DataState>
    </>
  );
}
