import { getTutors } from "../api/client";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatPrice, formatRating, formatTutorSubjects } from "../utils/format";
import page from "./Page.module.css";

export default function Tutors() {
  const { language, t } = useLanguage();
  const tutors = useApi(getTutors);

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
              to={`/tutors/${tutor.id}`}
              title={tutor.name}
              fields={[
                { label: t("fields.teaches"), value: formatTutorSubjects(tutor.subjects, language, t) },
                { label: t("fields.languages"), value: formatLanguages(tutor.languages, t) },
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
