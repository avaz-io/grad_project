import { getMentors } from "../api/client";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatRating, formatSessionPrice } from "../utils/format";
import page from "./Page.module.css";

export default function Mentors() {
  const { t } = useLanguage();
  const mentors = useApi(getMentors);

  return (
    <>
      <div className={page.header}>
        <h1>{t("mentors.title")}</h1>
        <p>{t("mentors.subtitle")}</p>
      </div>

      <DataState
        loading={mentors.loading}
        error={mentors.error}
        empty={mentors.data?.length === 0}
        onRetry={mentors.retry}
      >
        <div className={page.grid}>
          {mentors.data?.map((mentor) => (
            <Card
              key={mentor.id}
              to={`/mentors/${mentor.id}`}
              title={mentor.name}
              fields={[
                { label: t("fields.topics"), value: mentor.topics },
                { label: t("fields.languages"), value: formatLanguages(mentor.languages, t) },
              ]}
              footerLeft={formatSessionPrice(mentor.default_price, t)}
              footerRight={formatRating(mentor.rating_avg, mentor.rating_count, t)}
            />
          ))}
        </div>
      </DataState>
    </>
  );
}
