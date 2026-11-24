import { useState } from "react";

import { getCourses, getSubjects } from "../api/client";
import { LEVELS } from "../api/types";
import { useApi } from "../api/useApi";
import Card from "../components/Card";
import DataState from "../components/DataState";
import { useLanguage } from "../context/LanguageContext";
import { formatPrice, subjectName } from "../utils/format";
import page from "./Page.module.css";

export default function Courses() {
  const { language, t } = useLanguage();
  const [subject, setSubject] = useState(""); // "" = all subjects
  const [level, setLevel] = useState(""); // "" = all levels

  // Subjects fill the filter drop-down. Courses load again when a filter changes.
  const subjects = useApi(getSubjects);
  const courses = useApi(() => getCourses({ subject, level }), [subject, level]);

  return (
    <>
      <div className={page.header}>
        <h1>{t("courses.title")}</h1>
        <p>{t("courses.subtitle")}</p>
      </div>

      <div className={page.filters}>
        <label className={page.filter}>
          {t("courses.subject")}
          <select value={subject} onChange={(event) => setSubject(event.target.value)}>
            <option value="">{t("common.all")}</option>
            {subjects.data?.map((item) => (
              <option key={item.slug} value={item.slug}>
                {subjectName(item, language)}
              </option>
            ))}
          </select>
        </label>

        <label className={page.filter}>
          {t("courses.level")}
          <select value={level} onChange={(event) => setLevel(event.target.value)}>
            <option value="">{t("common.all")}</option>
            {LEVELS.map((value) => (
              <option key={value} value={value}>
                {t(`levels.${value}`)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <DataState
        loading={courses.loading}
        error={courses.error}
        empty={courses.data?.length === 0}
        onRetry={courses.retry}
      >
        <div className={page.grid}>
          {courses.data?.map((course) => (
            <Card
              key={course.id}
              title={course.title}
              tag={t(`levels.${course.level}`)}
              details={[
                subjectName(course.subject, language),
                t(`languageNames.${course.language}`),
                t("common.educator", { name: course.educator_name }),
              ]}
              footerLeft={formatPrice(course.price, t)}
              footerRight={t("common.lessons", { count: course.lesson_count })}
            />
          ))}
        </div>
      </DataState>
    </>
  );
}
