/**
 * ChartDisplay — Renders the base64-encoded chart image returned by the backend.
 *
 * Props:
 *   imageBase64 {string} — Base64 PNG string (no data-URI prefix).
 */
function ChartDisplay({ imageBase64 }) {
    return (
        <div className="card">
            <h2>📈 Generated Chart</h2>
            <img
                className="chart-img"
                src={`data:image/png;base64,${imageBase64}`}
                alt="AI-generated data visualization chart"
            />
        </div>
    )
}

export default ChartDisplay
