import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import mdx from "@mdx-js/rollup";

// https://vite.dev/config/
// Articles export `frontmatter` as a plain JS object at the top of the .mdx
// file (MDX supports export statements natively), so no frontmatter remark
// plugin is needed here.
export default defineConfig({
  base: "/exceptional-blogs/",
  plugins: [
    { enforce: "pre", ...mdx() },
    react({ include: /\.(jsx|tsx|mdx)$/ }),
  ],
});
