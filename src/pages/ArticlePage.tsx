import { useParams } from "react-router-dom";
import { MDXProvider } from "@mdx-js/react";
import { getArticleModule } from "../content";
import ArticleLayout from "../components/ArticleLayout";
import { mdxComponents } from "../mdx-components";
import NotFound from "./NotFound";

export default function ArticlePage() {
  const { slug: rawSlug } = useParams<{ slug: string }>();
  const slug = rawSlug?.replace(/\.html$/, "");
  const mod = slug ? getArticleModule(slug) : undefined;

  if (!mod) return <NotFound />;

  const Body = mod.default;

  return (
    <ArticleLayout frontmatter={mod.frontmatter}>
      <MDXProvider components={mdxComponents}>
        <Body />
      </MDXProvider>
    </ArticleLayout>
  );
}
