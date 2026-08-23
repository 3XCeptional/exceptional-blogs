import type { ReactNode } from "react";

export interface Source {
  label: string;
  url?: string;
}

/**
 * Renders the mandatory Sources footer. Every source must resolve to a real,
 * verified URL; omit `url` only for the rare case documented in the disclaimer.
 */
export function Sources({ items }: { items: Source[] }) {
  return (
    <footer className="sources">
      <h2>Sources</h2>
      <ol>
        {items.map((s, i) => (
          <li key={i}>
            {s.url ? (
              <a href={s.url} target="_blank" rel="noopener">
                {s.label}
              </a>
            ) : (
              s.label
            )}
          </li>
        ))}
      </ol>
    </footer>
  );
}

export function Disclaimer({ children }: { children: ReactNode }) {
  return <p className="disclaimer">{children}</p>;
}
