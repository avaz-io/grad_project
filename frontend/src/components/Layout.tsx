import { Outlet } from "react-router-dom";

import Footer from "./Footer";
import styles from "./Layout.module.css";
import Navbar from "./Navbar";

// The frame around every page. <Outlet /> is where the current page is shown.
export default function Layout() {
  return (
    <div className={styles.layout}>
      <Navbar />
      <main className={styles.main}>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
