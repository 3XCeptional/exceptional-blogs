import { useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { articles } from "../content";
import { ArticleCard } from "../components/ArticleCard";

const CATEGORIES: { value: string; label: string }[] = [
  { value: "all", label: "All" },
  { value: "ai-security", label: "AI & LLM Security" },
  { value: "career", label: "Career & Job Market" },
  { value: "tech", label: "Tech Deep Dives" },
];

export default function Home() {
  const [active, setActive] = useState("all");
  const carouselRef = useRef<HTMLDivElement>(null);

  const filtered = useMemo(
    () => (active === "all" ? articles : articles.filter((a) => a.category === active)),
    [active],
  );

  const scroll = (dir: number) => {
    carouselRef.current?.scrollBy({ left: dir * 320, behavior: "smooth" });
  };

  return (
    <div className="wrap wide">
      <header className="site-header">
        <div className="brand-row">
          <Link className="brand" to="/" viewTransition>
            Exceptional<span>Blogs</span>
          </Link>
          <span className="tagline">
            Research-backed articles on AI security, careers, and technology.
          </span>
        </div>
        <nav className="cats">
          {CATEGORIES.map((c) => (
            <button
              key={c.value}
              className={`cat-pill${active === c.value ? " active" : ""}`}
              onClick={() => setActive(c.value)}
            >
              {c.label}
            </button>
          ))}
        </nav>
      </header>

      <section className="featured">
        <h2 className="section-title">Recent articles</h2>
        <div className="carousel-row">
          <div className="carousel-nav">
            <button aria-label="Previous" onClick={() => scroll(-1)}>
              &#8249;
            </button>
            <button aria-label="Next" onClick={() => scroll(1)}>
              &#8250;
            </button>
          </div>
          <div className="carousel" ref={carouselRef}>
            {articles.map((a, i) => (
              <ArticleCard key={a.slug} article={a} index={i} />
            ))}
          </div>
        </div>
      </section>

      <section className="all">
        <h2 className="section-title">All articles</h2>
        {filtered.length > 0 ? (
          <div className="grid">
            {filtered.map((a, i) => (
              <ArticleCard key={a.slug} article={a} index={i} />
            ))}
          </div>
        ) : (
          <p className="empty-cat">No articles in this category yet.</p>
        )}
      </section>

      <footer className="site">
        Exceptional Blogs. Articles are researched with delegated AI agents and independently
        source-checked before publishing. &middot;{" "}
        <a
          className="support-link"
          href="https://www.buymeacoffee.com/3xceptional"
          target="_blank"
          rel="noopener"
        >
          Support this project
        </a>
      </footer>
    </div>
  );
}
