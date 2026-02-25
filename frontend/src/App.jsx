import { useState } from 'react'
import UploadCSV from './components/UploadCSV.jsx'
import CleaningReport from './components/CleaningReport.jsx'
import ChartDisplay from './components/ChartDisplay.jsx'

/**
 * App — Root component.
 *
 * Manages the top-level application state (cleaningReport, chartImage,
 * chartDecision) and composes the three main child components.
 */
function App() {
    const [cleaningReport, setCleaningReport] = useState(null)
    const [chartImage, setChartImage] = useState(null)
    const [chartDecision, setChartDecision] = useState(null)

    /**
     * handleResult — called by UploadCSV with the backend response payload.
     * @param {{ chart_image: string, cleaning_report: object, chart_decision: object }} result
     */
    function handleResult(result) {
        setCleaningReport(result.cleaning_report)
        setChartImage(result.chart_image)
        setChartDecision(result.chart_decision)
    }

    return (
        <div className="app">
            <header className="app-header">
                <h1>AI Data Visualizer</h1>
                <p>Upload a CSV — let AI clean your data and pick the perfect chart.</p>
            </header>

            <UploadCSV onResult={handleResult} />

            {cleaningReport && <CleaningReport report={cleaningReport} />}

            {chartDecision && (
                <div className="card">
                    <h2>📊 Chart Recommendation</h2>
                    <div className="decision-grid">
                        {[
                            ['Chart Type', chartDecision.chart_type],
                            ['X Axis', chartDecision.x_axis],
                            ['Y Axis', chartDecision.y_axis],
                            ['Group By', chartDecision.group_by ?? '—'],
                        ].map(([label, value]) => (
                            <div className="decision-chip" key={label}>
                                <div className="chip-label">{label}</div>
                                <div className="chip-value">{String(value)}</div>
                            </div>
                        ))}
                    </div>
                    {chartDecision.reason && (
                        <p style={{ marginTop: 14, color: 'var(--muted)', fontSize: '0.88rem' }}>
                            💡 {chartDecision.reason}
                        </p>
                    )}
                </div>
            )}

            {chartImage && <ChartDisplay imageBase64={chartImage} />}
        </div>
    )
}

export default App
