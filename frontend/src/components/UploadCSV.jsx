import { useState, useRef } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/upload-csv'

/**
 * UploadCSV — Lets the user pick a .csv file and submit it to the backend.
 *
 * Props:
 *   onResult(result) — callback invoked with the full backend JSON response
 *                      after a successful upload.
 */
function UploadCSV({ onResult }) {
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const inputRef = useRef(null)

    /** handleFileChange — stores the chosen file in state. */
    function handleFileChange(e) {
        setError(null)
        setFile(e.target.files[0] ?? null)
    }

    /** handleSubmit — POSTs the CSV to the FastAPI backend as multipart/form-data. */
    async function handleSubmit(e) {
        e.preventDefault()
        if (!file) return

        setLoading(true)
        setError(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const { data } = await axios.post(API_URL, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            })
            onResult(data)
        } catch (err) {
            const msg =
                err?.response?.data?.detail ??
                err?.message ??
                'An unexpected error occurred.'
            setError(msg)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="card">
            <h2>📂 Upload CSV</h2>
            <form onSubmit={handleSubmit}>
                <div className="upload-zone" onClick={() => inputRef.current?.click()}>
                    <label>
                        <svg width="40" height="40" fill="none" stroke="currentColor" strokeWidth="1.5"
                            viewBox="0 0 24 24" style={{ color: 'var(--accent)' }}>
                            <path strokeLinecap="round" strokeLinejoin="round"
                                d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                        </svg>
                        <span>{file ? '' : 'Click to choose a .csv file'}</span>
                        {file && <span className="file-chosen">✅ {file.name}</span>}
                    </label>
                    <input
                        ref={inputRef}
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        id="csv-file-input"
                    />
                </div>

                {error && <div className="error-banner">⚠️ {error}</div>}

                <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={!file || loading}
                    id="upload-submit-btn"
                >
                    {loading ? (
                        <>
                            <span className="spinner" />
                            Analysing…
                        </>
                    ) : (
                        'Visualize with AI ✨'
                    )}
                </button>
            </form>
        </div>
    )
}

export default UploadCSV
