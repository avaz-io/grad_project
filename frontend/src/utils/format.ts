import type { SubjectShort } from "../api/types";
import type { Language, Translate } from "../context/LanguageContext";

// "15.00" -> "$15", "0.00" -> "Free". Prices are in US dollars (payments run in test mode).
export function formatPrice(price: string, t: Translate): string {
  const amount = Number(price);
  return amount === 0 ? t("common.free") : `$${amount}`;
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

// ["uz", "en"] -> "Languages: Uzbek, English"
export function formatLanguages(codes: string[], t: Translate): string {
  const names = codes.map((code) => t(`languageNames.${code}`));
  return t("common.languages", { list: names.join(", ") });
}

// Date and time of a live lecture, written in the interface language.
export function formatDateTime(iso: string, language: Language): string {
  const locale = language === "uz" ? "uz-UZ" : "en-GB";
  return new Date(iso).toLocaleString(locale, { dateStyle: "medium", timeStyle: "short" });
}
