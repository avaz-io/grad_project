import type { SubjectShort, TutorSubject } from "../api/types";
import type { Language, Translate } from "../context/LanguageContext";

// "15.00" -> "$15", "12.50" -> "$12.5", "0.00" -> "Free". All prices are in US dollars.
export function formatPrice(price: string, t: Translate): string {
  const amount = Number(price);
  return amount === 0 ? t("common.free") : `$${amount}`;
}

// Mentor sessions: "Free", or "$10 / session".
export function formatSessionPrice(price: string, t: Translate): string {
  return Number(price) === 0
    ? t("common.free")
    : t("common.pricePerSession", { price: formatPrice(price, t) });
}

// "★ 4.5 (12 reviews)", or "No reviews yet" when nobody has rated.
export function formatRating(ratingAvg: string, ratingCount: number, t: Translate): string {
  if (ratingCount === 0) {
    return t("common.noReviews");
  }
  return t("common.rating", { rating: Number(ratingAvg).toFixed(1), count: ratingCount });
}

export function subjectName(subject: SubjectShort, language: Language): string {
  return language === "uz" ? subject.name_uz : subject.name_en;
}

// ["uz", "en"] -> "Uzbek, English"
export function formatLanguages(codes: string[], t: Translate): string {
  return codes.map((code) => t(`languageNames.${code}`)).join(", ");
}

// [{English, a1, b2}] -> "English (A1 – B2)": what a tutor teaches and for which levels.
export function formatTutorSubjects(subjects: TutorSubject[], language: Language, t: Translate): string {
  return subjects
    .map((s) => `${subjectName(s, language)} (${t(`levels.${s.min_level}`)} – ${t(`levels.${s.max_level}`)})`)
    .join(", ");
}

function localeOf(language: Language): string {
  return language === "uz" ? "uz-UZ" : "en-GB";
}

// "25 Nov 2026, 10:00", written in the interface language.
export function formatDateTime(iso: string, language: Language): string {
  return new Date(iso).toLocaleString(localeOf(language), { dateStyle: "medium", timeStyle: "short" });
}

// "25 Nov 2026, 10:00 – 11:00" for a booking slot.
export function formatTimeRange(startIso: string, endIso: string, language: Language): string {
  const end = new Date(endIso).toLocaleTimeString(localeOf(language), { timeStyle: "short" });
  return `${formatDateTime(startIso, language)} – ${end}`;
}
