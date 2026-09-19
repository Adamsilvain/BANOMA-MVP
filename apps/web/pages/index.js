export default function Home() {
  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 720, margin: '0 auto', padding: '3rem 1.5rem' }}>
      <h1>BANOMA</h1>
      <p style={{ fontSize: '1.15rem', color: '#444' }}>
        La plateforme qui connecte les talents scientifiques et techniques africains aux opportunités mondiales.
      </p>
      <ul>
        <li>Valoriser les compétences intellectuelles et techniques</li>
        <li>Offrir une vitrine interactive aux experts</li>
        <li>Encourager la monétisation des savoir-faire</li>
      </ul>
      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
        <a href="/talents" style={{ padding: '0.6rem 1.2rem', background: '#111', color: '#fff', borderRadius: 6, textDecoration: 'none' }}>
          Découvrir les talents
        </a>
        <a href="/opportunites" style={{ padding: '0.6rem 1.2rem', border: '1px solid #111', borderRadius: 6, textDecoration: 'none', color: '#111' }}>
          Voir les opportunités
        </a>
      </div>
    </main>
  )
}
