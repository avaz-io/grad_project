import styles from "./InfoList.module.css";

// One labelled piece of information, e.g. { label: "Subject", value: "English" }.
export type Field = {
  label: string;
  value: string;
};

// The "Subject: English / Level: B2 / ..." table at the top of a detail page.
export default function InfoList({ fields }: { fields: Field[] }) {
  return (
    <dl className={styles.list}>
      {fields.map((field) => (
        <div key={field.label} className={styles.row}>
          <dt>{field.label}</dt>
          <dd>{field.value}</dd>
        </div>
      ))}
    </dl>
  );
}
