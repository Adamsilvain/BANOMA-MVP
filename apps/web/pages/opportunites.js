import { useEffect, useState } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function Opportunites() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/opportunities/`)
      .then((res) => res.json())
      .then((data) => setItems(Array.isArray(data) ? data : data.results || []))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 720, margin: '0 auto', padding: '3rem 1.5rem' }}>
      <h1>Opportunités</h1>
      {loading && <p>Chargement…</p>}
      {!loading && items.length === 0 && <p>Aucune opportunité publiée pour le moment.</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {items.map((o) => (
          <li key={o.id} style={{ border: '1px solid #eee', borderRadius: 8, padding: '1rem', marginBottom: '0.75rem' }}>
            <strong>{o.title}</strong>
            <div style={{ fontSize: '0.85rem', color: '#888' }}>
              {o.type} {o.remote ? '· À distance' : o.location ? `· ${o.location}` : ''}
            </div>
            <p style={{ color: '#444' }}>{o.description}</p>
          </li>
        ))}
      </ul>
    </main>
  )
}
