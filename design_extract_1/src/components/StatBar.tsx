interface StatBarProps {
  label: string;
  value: number;
  max?: number;
  color?: string;
}

export default function StatBar({ label, value, max = 100, color = '#00FF88' }: StatBarProps) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className="flex items-center gap-3 py-1">
      <span className="font-mono text-[10px] tracking-widest text-muted-foreground uppercase w-28 shrink-0">
        {label}
      </span>
      <div className="flex-1 h-2 bg-muted rounded-sm overflow-hidden relative">
        <div
          className="h-full transition-all duration-700"
          style={{ width: `${pct}%`, background: color, boxShadow: `0 0 6px ${color}` }}
        />
      </div>
    </div>
  );
}
