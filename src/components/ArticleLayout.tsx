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
        <Link to="/">&larr; Exceptional Blogs</Link>
      </p>
      <header className="hero">
        <span className="kicker">{frontmatter.kicker}</span>
        <h1>{frontmatter.title}</h1>
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
    </div>
  );
}
