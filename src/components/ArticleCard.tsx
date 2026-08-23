import { Link } from "react-router-dom";
import type { ArticleMeta } from "../content";

export function ArticleCard({ article, index = 0 }: { article: ArticleMeta; index?: number }) {
  const displayDate = new Date(`${article.date}T00:00:00`).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <Link
      className="carousel-card reveal"
      to={article.path}
      viewTransition
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <img
        className="thumb"
        src={`${import.meta.env.BASE_URL}${article.image}`}
        alt=""
        loading="lazy"
      />
      <div className="body">
        <span className="card-cat">{article.categoryLabel}</span>
        <div className="card-title">{article.title}</div>
        <p className="card-excerpt">{article.excerpt}</p>
        <span className="card-meta">{displayDate}</span>
      </div>
    </Link>
  );
}
