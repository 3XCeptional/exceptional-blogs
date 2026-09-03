import type { ReactNode } from "react";
import { Link } from "react-router-dom";

export interface Frontmatter {
  title: string;
  dek: string;
  date: string;
  readTime: string;
  kicker: string;
  image: string;
  imageAlt: string;
  imageCaption: string;
  attackStyle?: string;
}

export default function ArticleLayout({
  frontmatter,
  children,
}: {
  frontmatter: Frontmatter;
  children: ReactNode;
}) {
  return (
    <div className="wrap">
      <p style={{ paddingTop: 24 }}>
        <Link to="/" viewTransition>
          &larr; Exceptional Blogs
        </Link>
      </p>
      <header className="hero">
        <h1>{frontmatter.title}</h1>
        {frontmatter.attackStyle && <span className="attack-tag">{frontmatter.attackStyle}</span>}
        <p className="dek">{frontmatter.dek}</p>
        <p className="meta">
          Published {frontmatter.date} &middot; Research compiled with delegated AI agents and
          independent source verification &middot; {frontmatter.readTime}
        </p>
      </header>

      <figure>
        <img
          src={`${import.meta.env.BASE_URL}${frontmatter.image}`}
          alt={frontmatter.imageAlt}
          loading="lazy"
        />
        <figcaption>{frontmatter.imageCaption}</figcaption>
      </figure>

      <div className="article-body">{children}</div>

      <footer className="site">
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
