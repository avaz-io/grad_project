import { Link, useParams } from "react-router-dom";

import { getMentor } from "../api/client";
import { useApi } from "../api/useApi";
import DataState from "../components/DataState";
import InfoList from "../components/InfoList";
import SlotList from "../components/SlotList";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatRating, formatSessionPrice } from "../utils/format";
import styles from "./Detail.module.css";

// /mentors/:id: mentor profile and the free time slots that can be booked.
export default function MentorDetail() {
  const { id = "" } = useParams();
  const { t } = useLanguage();
  const mentor = useApi(() => getMentor(id), [id]);

  return (
    <>
      <Link to="/mentors" className={styles.back}>
        {t("common.back")}
      </Link>

      <DataState
        loading={mentor.loading}
        error={mentor.error}
        notFound={mentor.notFound}
        onRetry={mentor.retry}
      >
        {mentor.data && (
          <>
            <section className={styles.panel}>
              <div className={styles.titleRow}>
                <h1>{mentor.data.name}</h1>
              </div>
              <InfoList
                fields={[
                  { label: t("fields.topics"), value: mentor.data.topics },
                  { label: t("fields.languages"), value: formatLanguages(mentor.data.languages, t) },
                  {
                    label: t("fields.rating"),
                    value: formatRating(mentor.data.rating_avg, mentor.data.rating_count, t),
                  },
                  {
                    label: t("fields.sessionPrice"),
                    value: formatSessionPrice(mentor.data.default_price, t),
                  },
                ]}
              />
            </section>

            {mentor.data.bio && (
              <section className={styles.panel}>
                <h2>{t("booking.about")}</h2>
                <p className={styles.text}>{mentor.data.bio}</p>
              </section>
            )}

            <section className={styles.panel}>
              <h2>{t("booking.freeSlots")}</h2>
              <SlotList slots={mentor.data.free_slots} />
            </section>
          </>
        )}
      </DataState>
    </>
  );
}
