<svelte:head>
  <title>Sobre Nós - Molduras Novo Tempo</title>
</svelte:head>

<section class="about-page">
  <div class="container">
    <h1 class="section-title">Sobre Nós</h1>

    <div class="about-content">
      <div class="about-image">
        <img src="https://placehold.co/600x400/1a1a1a/F5B800?text=Molduras+Novo+Tempo" alt="Molduras Novo Tempo" />
      </div>
      <div class="about-text">
        <h2>Molduras Novo Tempo</h2>
        <p>
          Há mais de <strong>20 anos no mercado</strong>, a Molduras Novo Tempo é referência na fabricação e venda de placas decorativas, molduras e quadros de alta qualidade.
        </p>
        <p>
          Atendemos lojistas em todo o Brasil, oferecendo produtos com acabamento premium e design exclusivo. Nossa missão é transformar ambientes através da arte e decoração acessível.
        </p>
        <p>
          Trabalhamos com uma ampla variedade de estilos — do clássico ao moderno, do minimalista ao rústico — sempre buscando inovar e trazer as tendências mais atuais do mercado de decoração.
        </p>

        <div class="stats">
          <div class="stat">
            <span class="stat-number">20+</span>
            <span class="stat-label">Anos de experiência</span>
          </div>
          <div class="stat">
            <span class="stat-number">1000+</span>
            <span class="stat-label">Clientes satisfeitos</span>
          </div>
          <div class="stat">
            <span class="stat-number">5000+</span>
            <span class="stat-label">Produtos entregues</span>
          </div>
        </div>
      </div>
    </div>

    <div class="values">
      <div class="value-card">
        <h3>Missão</h3>
        <p>Transformar ambientes com arte e decoração de qualidade, tornando cada espaço único e especial.</p>
      </div>
      <div class="value-card">
        <h3>Visão</h3>
        <p>Ser a principal referência em molduras e quadros decorativos no Brasil, reconhecida pela qualidade e inovação.</p>
      </div>
      <div class="value-card">
        <h3>Valores</h3>
        <p>Qualidade, compromisso com o cliente, inovação constante e respeito ao meio ambiente.</p>
      </div>
    </div>
  </div>
</section>

<style>
  .about-page {
    padding: 3rem 0;
  }

  .about-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
    margin-bottom: 4rem;
  }

  .about-image img {
    width: 100%;
    border-radius: var(--radius-lg);
  }

  .about-text h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--primary-dark);
  }

  .about-text p {
    color: var(--gray-600);
    line-height: 1.8;
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }

  .stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.5rem;
  }

  .stat {
    text-align: center;
  }

  .stat-number {
    display: block;
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary);
  }

  .stat-label {
    font-size: 0.8rem;
    color: var(--gray-500);
  }

  .values {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .value-card {
    padding: 2rem;
    background: var(--gray-50);
    border-radius: var(--radius-lg);
    border-left: 4px solid var(--primary);
  }

  .value-card h3 {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
    color: var(--black);
  }

  .value-card p {
    font-size: 0.9rem;
    color: var(--gray-600);
    line-height: 1.6;
  }

  @media (max-width: 768px) {
    .about-content {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    .values {
      grid-template-columns: 1fr;
    }
    .stats {
      flex-wrap: wrap;
      justify-content: center;
    }
  }
</style>
