import type { ComponentType } from "react";
import type { Frontmatter } from "../components/ArticleLayout";

export interface ArticleFrontmatter extends Frontmatter {
  excerpt: string;
  category: string;
  categoryLabel: string;
}

export interface ArticleMeta {
  slug: string;
  path: string;
  title: string;
  excerpt: string;
  image: string;
  category: string;
  categoryLabel: string;
  date: string;
}

type MdxModule = {
  default: ComponentType;
  frontmatter: ArticleFrontmatter;
};

const modules = import.meta.glob("./articles/*.mdx", { eager: true }) as Record<
  string,
  MdxModule
>;

function slugFromPath(path: string): string {
  return path.replace("./articles/", "").replace(/\.mdx$/, "");
}

export const articles: ArticleMeta[] = Object.entries(modules)
  .map(([path, mod]) => {
    const slug = slugFromPath(path);
    return {
      slug,
      path: `/${slug}.html`,
      title: mod.frontmatter.title,
      excerpt: mod.frontmatter.excerpt,
      image: mod.frontmatter.image,
      category: mod.frontmatter.category,
      categoryLabel: mod.frontmatter.categoryLabel,
      date: mod.frontmatter.date,
    };
  })
  .sort((a, b) => b.date.localeCompare(a.date));

export function getArticleModule(slug: string): MdxModule | undefined {
  return modules[`./articles/${slug}.mdx`];
}
