import { getMentors } from "../api/client";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatPrice, formatRating } from "../utils/format";
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
          {mentors.data?.map((mentor) => {
            // A free session just says "Free", a paid one says "$10 / session".
            const price = formatPrice(mentor.default_price, t);
            const isFree = Number(mentor.default_price) === 0;
            return (
              <Card
                key={mentor.id}
                title={mentor.name}
                details={[mentor.topics, formatLanguages(mentor.languages, t)]}
                footerLeft={isFree ? price : t("common.pricePerSession", { price })}
                footerRight={formatRating(mentor.rating_avg, mentor.rating_count, t)}
              />
            );
          })}
        </div>
      </DataState>
    </>
  );
}
