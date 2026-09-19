import { useEffect, useState } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function Boutique() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/products/`)
      .then((res) => res.json())
      .then((data) => setProducts(Array.isArray(data) ? data : data.results || []))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 720, margin: '0 auto', padding: '3rem 1.5rem' }}>
      <h1>La marketplace du savoir</h1>
      <p style={{ color: '#666' }}>Cours, ebooks, datasets, prestations — 70 % des revenus reviennent au créateur.</p>
      {loading && <p>Chargement…</p>}
      {!loading && products.length === 0 && <p>Aucun article publié pour le moment.</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {products.map((p) => (
          <li key={p.id} style={{ border: '1px solid #eee', borderRadius: 8, padding: '1rem', marginBottom: '0.75rem' }}>
            <strong>{p.title}</strong>
            <div style={{ fontSize: '0.85rem', color: '#888' }}>
              {p.type} · {(p.price / 100).toLocaleString()} {p.currency}
            </div>
            <p style={{ color: '#444' }}>{p.description}</p>
          </li>
        ))}
      </ul>
    </main>
  )
}
