import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="wrap">
      <header className="hero">
        <span className="kicker">404</span>
        <h1>Page not found</h1>
        <p className="dek">
          That article does not exist, or the link is out of date. <Link to="/">Back to the homepage.</Link>
        </p>
      </header>
    </div>
  );
}
