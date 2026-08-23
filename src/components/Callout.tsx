import type { ReactNode } from "react";

export function Callout({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="callout">
      <span className="label">{label}</span>
      {children}
    </div>
  );
}

export function Warn({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="warn">
      <span className="label">{label}</span>
      {children}
    </div>
  );
}
