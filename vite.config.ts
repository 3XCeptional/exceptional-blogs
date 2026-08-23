import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import mdx from "@mdx-js/rollup";
import remarkGfm from "remark-gfm";

// https://vite.dev/config/
// Articles export `frontmatter` as a plain JS object at the top of the .mdx
// file (MDX supports export statements natively), so no frontmatter remark
// plugin is needed here.
export default defineConfig({
  base: "/exceptional-blogs/",
  plugins: [
    {
      enforce: "pre",
      ...mdx({
        // Required for <MDXProvider> context to actually reach compiled
        // MDX output; without this, custom tags like <StatGrid> resolve
        // to undefined and React throws on mount (blank page, no log).
        providerImportSource: "@mdx-js/react",
        // GFM adds table syntax support; without it, markdown tables
        // render as literal pipe-delimited text inside a <p>.
        remarkPlugins: [remarkGfm],
      }),
    },
    react({ include: /\.(jsx|tsx|mdx)$/ }),
  ],
});
