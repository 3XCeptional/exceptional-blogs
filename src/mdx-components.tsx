import type { MDXComponents } from "mdx/types";
import { Callout, Warn } from "./components/Callout";
import { StatGrid, Stat } from "./components/StatGrid";
import { Sources, Disclaimer } from "./components/Sources";

/**
 * Components made available inside every .mdx article without an explicit
 * import. Keep this list small and stable: it is the template's public API.
 */
export const mdxComponents: MDXComponents = {
  Callout,
  Warn,
  StatGrid,
  Stat,
  Sources,
  Disclaimer,
};
