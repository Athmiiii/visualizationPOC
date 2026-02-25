/**
 * CleaningReport — Displays a human-readable summary of the changes
 * the data_cleaner service made to the uploaded CSV.
 *
 * Props:
 *   report {object} — cleaning_report dict from the backend.
 */
function CleaningReport({ report }) {
    const items = []

    // Duplicate rows removed
    if (report.duplicates_removed > 0) {
        items.push(`Removed ${report.duplicates_removed} duplicate row(s)`)
    }

    // Null values filled
    if (report.nulls_filled && Object.keys(report.nulls_filled).length > 0) {
        for (const [col, info] of Object.entries(report.nulls_filled)) {
            items.push(
                `Filled ${info.count} null(s) in "${col}" using ${info.strategy} (${info.value})`
            )
        }
    }

    // Type conversions
    if (report.type_conversions?.length > 0) {
        for (const tc of report.type_conversions) {
            items.push(`Converted "${tc.column}" from ${tc.from} → ${tc.to}`)
        }
    }

    // Casing normalised
    if (report.casing_normalised?.length > 0) {
        items.push(
            `Normalised text casing in: ${report.casing_normalised.join(', ')}`
        )
    }

    return (
        <div className="card">
            <h2>🧹 Cleaning Report</h2>
            {items.length === 0 ? (
                <p className="no-changes">✅ No issues found — data looks clean!</p>
            ) : (
                <div className="report-grid">
                    {items.map((item, i) => (
                        <div className="report-item" key={i}>
                            <div className="report-dot" />
                            <span>{item}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default CleaningReport
