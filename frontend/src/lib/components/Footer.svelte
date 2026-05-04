<footer class="footer">
  <div class="footer-main">
    <div class="container footer-grid">
      <div class="footer-col">
        <div class="footer-logo">
          <div class="logo-icon"><span>NT</span></div>
          <div>
            <strong>MOLDURAS NOVO TEMPO</strong>
            <small>molduras & quadros</small>
          </div>
        </div>
        <p class="footer-desc">
          Somos fabricantes de placas decorativas, molduras e quadros. Há mais de 20 anos no mercado atendendo lojistas em todo o Brasil.
        </p>
      </div>

      <div class="footer-col">
        <h4>Links Rápidos</h4>
        <a href="/">Início</a>
        <a href="/sobre">Sobre nós</a>
        <a href="/produtos">Produtos</a>
        <a href="/contato">Contato</a>
        <a href="/comentarios">Comentários</a>
      </div>

      <div class="footer-col">
        <h4>Categorias</h4>
        <a href="/produtos?category_id=1">Quadros Decorativos</a>
        <a href="/produtos?category_id=2">Molduras</a>
        <a href="/produtos?category_id=3">Placas Decorativas</a>
        <a href="/produtos?category_id=4">Quadros Personalizados</a>
        <a href="/produtos?category_id=5">Kits de Quadros</a>
      </div>

      <div class="footer-col">
        <h4>Contato</h4>
        <p>contato@moldurasnovotempo.com.br</p>
        <p>(11) 99999-9999</p>
        <div class="social-links">
          <a href="https://instagram.com/moldurasnovotempo" target="_blank" rel="noopener" aria-label="Instagram">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <p>&copy; {new Date().getFullYear()} Molduras Novo Tempo. Todos os direitos reservados.</p>
    </div>
  </div>
</footer>

<style>
  .footer {
    margin-top: 4rem;
  }

  .footer-main {
    background: var(--black);
    color: var(--white);
    padding: 3rem 0;
  }

  .footer-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
  }

  .footer-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .footer-logo .logo-icon {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .footer-logo .logo-icon span {
    font-weight: 800;
    color: var(--black);
    font-size: 1.1rem;
  }

  .footer-logo strong {
    font-size: 0.9rem;
    display: block;
    letter-spacing: 0.5px;
  }

  .footer-logo small {
    font-size: 0.65rem;
    color: var(--primary);
  }

  .footer-desc {
    font-size: 0.85rem;
    color: var(--gray-400);
    line-height: 1.7;
  }

  .footer-col h4 {
    font-size: 0.9rem;
    margin-bottom: 1rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .footer-col a {
    display: block;
    font-size: 0.85rem;
    color: var(--gray-400);
    padding: 0.25rem 0;
    transition: color 0.2s;
  }

  .footer-col a:hover {
    color: var(--primary);
  }

  .footer-col p {
    font-size: 0.85rem;
    color: var(--gray-400);
    margin-bottom: 0.25rem;
  }

  .social-links {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
  }

  .social-links a {
    color: var(--gray-400);
    transition: color 0.2s;
  }

  .social-links a:hover {
    color: var(--primary);
  }

  .footer-bottom {
    background: #111;
    padding: 1rem 0;
    text-align: center;
  }

  .footer-bottom p {
    font-size: 0.8rem;
    color: var(--gray-500);
  }

  @media (max-width: 768px) {
    .footer-grid {
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .footer-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
