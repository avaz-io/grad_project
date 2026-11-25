import { Link } from "react-router-dom";

import styles from "./Card.module.css";
import type { Field } from "./InfoList";

type CardProps = {
  to: string; // the detail page this card opens
  title: string;
  tag?: string; // small label in the corner, e.g. "Live"
  fields: Field[]; // shown as "Subject: English", one per line
  footerLeft: string; // usually the price
  footerRight?: string; // usually the rating or lesson count
};

// One item in a list page: a course, tutor, mentor or lecture.
// The whole card is a link to the item's detail page.
export default function Card({ to, title, tag, fields, footerLeft, footerRight }: CardProps) {
  return (
    <Link to={to} className={styles.card}>
      <div className={styles.top}>
        <h3 className={styles.title}>{title}</h3>
        {tag && <span className={styles.tag}>{tag}</span>}
      </div>

      <ul className={styles.fields}>
        {fields.map((field) => (
          <li key={field.label}>
            <span className={styles.label}>{field.label}:</span> {field.value}
          </li>
        ))}
      </ul>

      <div className={styles.footer}>
        <span className={styles.price}>{footerLeft}</span>
        {footerRight && <span className={styles.muted}>{footerRight}</span>}
      </div>
    </Link>
  );
}
