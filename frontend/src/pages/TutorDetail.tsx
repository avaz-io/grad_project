import { Link, useParams } from "react-router-dom";

import { getTutor } from "../api/client";
import { useApi } from "../api/useApi";
import DataState from "../components/DataState";
import InfoList from "../components/InfoList";
import SlotList from "../components/SlotList";
import { useLanguage } from "../context/LanguageContext";
import { formatLanguages, formatPrice, formatRating, formatTutorSubjects } from "../utils/format";
import styles from "./Detail.module.css";

// /tutors/:id: tutor profile and the free time slots that can be booked.
export default function TutorDetail() {
  const { id = "" } = useParams();
  const { language, t } = useLanguage();
  const tutor = useApi(() => getTutor(id), [id]);

  return (
    <>
      <Link to="/tutors" className={styles.back}>
        {t("common.back")}
      </Link>

      <DataState
        loading={tutor.loading}
        error={tutor.error}
        notFound={tutor.notFound}
        onRetry={tutor.retry}
      >
        {tutor.data && (
          <>
            <section className={styles.panel}>
              <div className={styles.titleRow}>
                <h1>{tutor.data.name}</h1>
              </div>
              <InfoList
                fields={[
                  {
                    label: t("fields.teaches"),
                    value: formatTutorSubjects(tutor.data.subjects, language, t),
                  },
                  { label: t("fields.languages"), value: formatLanguages(tutor.data.languages, t) },
                  {
                    label: t("fields.rating"),
                    value: formatRating(tutor.data.rating_avg, tutor.data.rating_count, t),
                  },
                  {
                    label: t("fields.hourlyRate"),
                    value: t("common.pricePerHour", { price: formatPrice(tutor.data.hourly_rate, t) }),
                  },
                ]}
              />
            </section>

            {tutor.data.bio && (
              <section className={styles.panel}>
                <h2>{t("booking.about")}</h2>
                <p className={styles.text}>{tutor.data.bio}</p>
              </section>
            )}

            <section className={styles.panel}>
              <h2>{t("booking.freeSlots")}</h2>
              <SlotList slots={tutor.data.free_slots} />
            </section>
          </>
        )}
      </DataState>
    </>
  );
}
