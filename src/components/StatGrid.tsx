import type { ReactNode } from "react";

export function StatGrid({ children }: { children: ReactNode }) {
  return <div className="stat-strip">{children}</div>;
}

export function Stat({ num, children }: { num: string; children: ReactNode }) {
  return (
    <div className="stat-item">
      <span className="figure-num">{num}</span>
      <span className="figure-label">{children}</span>
    </div>
  );
}
