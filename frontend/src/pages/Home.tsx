import { useEffect, useState } from "react";

import { getHealth } from "../api/client";
import en from "../i18n/en.json";

export default function Home() {
  const [apiStatus, setApiStatus] = useState("checking...");

  // Calls the backend once to prove frontend and backend are connected.
  useEffect(() => {
    getHealth()
      .then((data) => setApiStatus(data.status))
      .catch(() => setApiStatus("unreachable"));
  }, []);

  return (
    <main className="page">
      <h1>{en.appName}</h1>
      <p>{en.tagline}</p>
      <p>
        {en.apiStatus}: {apiStatus}
      </p>
    </main>
  );
}
