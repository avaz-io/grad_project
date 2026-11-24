import styles from "./Card.module.css";

type CardProps = {
  title: string;
  tag?: string; // small label in the corner, e.g. "Live" or "B2"
  details: string[]; // one line of text each
  footerLeft: string; // usually the price
  footerRight?: string; // usually the rating or lesson count
};

// One item in a list page: a course, tutor, mentor or lecture.
export default function Card({ title, tag, details, footerLeft, footerRight }: CardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.top}>
        <h3 className={styles.title}>{title}</h3>
        {tag && <span className={styles.tag}>{tag}</span>}
      </div>

      <ul className={styles.details}>
        {details.map((line, index) => (
          <li key={index}>{line}</li>
        ))}
      </ul>

      <div className={styles.footer}>
        <span className={styles.price}>{footerLeft}</span>
        {footerRight && <span className={styles.muted}>{footerRight}</span>}
      </div>
    </article>
  );
}
