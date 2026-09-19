import { useEffect, useState } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function Talents() {
  const [talents, setTalents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/talents/`)
      .then((res) => res.json())
      .then((data) => setTalents(Array.isArray(data) ? data : data.results || []))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 720, margin: '0 auto', padding: '3rem 1.5rem' }}>
      <h1>Talents</h1>
      {loading && <p>Chargement…</p>}
      {!loading && talents.length === 0 && <p>Aucun talent pour le moment.</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {talents.map((t) => (
          <li key={t.id} style={{ border: '1px solid #eee', borderRadius: 8, padding: '1rem', marginBottom: '0.75rem' }}>
            <strong>{t.user}</strong>
            {t.skills && <div style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#888' }}>{t.skills}</div>}
          </li>
        ))}
      </ul>
    </main>
  )
}
