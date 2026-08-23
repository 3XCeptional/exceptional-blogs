import type { ReactNode } from "react";

function InfoIcon() {
  return (
    <svg
      className="icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d="M9 18h6" />
      <path d="M10 21h4" />
      <path d="M12 3a6 6 0 0 0-3.5 10.9c.6.45 1 1.2 1 2.1h5c0-.9.4-1.65 1-2.1A6 6 0 0 0 12 3Z" />
    </svg>
  );
}

function WarnIcon() {
  return (
    <svg
      className="icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d="M12 4 3 20h18L12 4Z" />
      <line x1="12" y1="10" x2="12" y2="15" />
      <circle cx="12" cy="18" r="0.6" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function Callout({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="callout">
      <span className="label">
        <InfoIcon />
        {label}
      </span>
      {children}
    </div>
  );
}

export function Warn({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="warn">
      <span className="label">
        <WarnIcon />
        {label}
      </span>
      {children}
    </div>
  );
}
