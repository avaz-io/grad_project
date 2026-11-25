import { ReactNode } from "react";

import { useLanguage } from "../context/LanguageContext";
import styles from "./DataState.module.css";

type DataStateProps = {
  loading: boolean;
  error: boolean;
  notFound?: boolean; // the server said 404, so trying again will not help
  empty?: boolean;
  onRetry: () => void;
  children: ReactNode;
};

// Shows "Loading...", an error (with a retry button), "not found" or "Nothing found."
// Only when the data is ready does it show its children.
export default function DataState({
  loading,
  error,
  notFound = false,
  empty = false,
  onRetry,
  children,
}: DataStateProps) {
  const { t } = useLanguage();

  if (loading) {
    return (
      <p className={styles.message} role="status">
        {t("common.loading")}
      </p>
    );
  }

  if (notFound) {
    return <p className={styles.message}>{t("common.notFound")}</p>;
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
