import type { ReactNode } from "react";

export function StatGrid({ children }: { children: ReactNode }) {
  return <div className="card-grid">{children}</div>;
}

export function Stat({ num, children }: { num: string; children: ReactNode }) {
  return (
    <div className="stat-card">
      <span className="figure-num">{num}</span>
      <span className="figure-label">{children}</span>
    </div>
  );
}
