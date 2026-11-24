import { ReactNode } from "react";

import { useLanguage } from "../context/LanguageContext";
import styles from "./DataState.module.css";

type DataStateProps = {
  loading: boolean;
  error: boolean;
  empty: boolean;
  onRetry: () => void;
  children: ReactNode;
};

// Shows "Loading...", an error with a retry button, or "Nothing found."
// Only when the data is ready does it show its children (the list of cards).
export default function DataState({ loading, error, empty, onRetry, children }: DataStateProps) {
  const { t } = useLanguage();

  if (loading) {
    return (
      <p className={styles.message} role="status">
        {t("common.loading")}
      </p>
    );
  }

  if (error) {
    return (
      <div className={styles.error} role="alert">
        <p>{t("common.error")}</p>
        <button type="button" className={styles.retry} onClick={onRetry}>
          {t("common.retry")}
        </button>
      </div>
    );
  }

  if (empty) {
    return <p className={styles.message}>{t("common.empty")}</p>;
  }

  return <>{children}</>;
}
