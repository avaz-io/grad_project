import type { FreeSlot } from "../api/types";
import { useLanguage } from "../context/LanguageContext";
import { formatPrice, formatTimeRange } from "../utils/format";
import styles from "./SlotList.module.css";

// The free time slots of a tutor or mentor.
// Booking is not built yet, so every "Book" button is disabled.
export default function SlotList({ slots }: { slots: FreeSlot[] }) {
  const { language, t } = useLanguage();

  if (slots.length === 0) {
    return <p className={styles.empty}>{t("booking.noSlots")}</p>;
  }

  return (
    <ul className={styles.list}>
      {slots.map((slot) => (
        <li key={slot.id} className={styles.slot}>
          <span className={styles.time}>{formatTimeRange(slot.starts_at, slot.ends_at, language)}</span>
          <span className={styles.price}>{formatPrice(slot.price, t)}</span>
          <button type="button" className={styles.book} disabled title={t("common.comingSoon")}>
            {t("booking.book")}
          </button>
        </li>
      ))}
    </ul>
  );
}
