import { mapPins } from "@/lib/data";
import { riskClass } from "@/lib/risk";

export function KenyaRiskMap({ compact = false }: { compact?: boolean }) {
  return (
    <div className={compact ? "map-shell compact" : "map-shell"}>
      <svg
        className="kenya-map"
        viewBox="0 0 100 100"
        role="img"
        aria-label="Stylized Kenya risk heatmap with county signal pins"
      >
        <path
          d="M45 5 L67 9 L80 22 L89 42 L83 63 L91 76 L78 91 L60 96 L44 89 L32 93 L20 79 L13 62 L18 44 L10 31 L25 21 L31 9 Z"
          className="map-base"
        />
        <path
          d="M31 9 L39 30 L30 48 L18 44 L10 31 L25 21 Z"
          className="map-zone guarded-zone"
        />
        <path
          d="M39 30 L58 33 L62 55 L48 66 L30 48 Z"
          className="map-zone elevated-zone"
        />
        <path
          d="M58 33 L80 22 L89 42 L83 63 L62 55 Z"
          className="map-zone guarded-zone"
        />
        <path
          d="M48 66 L62 55 L83 63 L91 76 L78 91 L60 96 L44 89 Z"
          className="map-zone low-zone"
        />
        <path
          d="M30 48 L48 66 L44 89 L32 93 L20 79 L13 62 Z"
          className="map-zone elevated-zone"
        />
        {mapPins.map((pin) => (
          <g key={pin.county} className={`map-pin ${riskClass(pin.level)}`}>
            <circle cx={pin.x} cy={pin.y} r={compact ? "2.8" : "3.5"} />
            {!compact ? (
              <text x={pin.x + 4} y={pin.y + 1.5}>
                {pin.county}
              </text>
            ) : null}
          </g>
        ))}
      </svg>
    </div>
  );
}
