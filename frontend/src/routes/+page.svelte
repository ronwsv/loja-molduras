<script lang="ts">
  import HeroBanner from '$lib/components/HeroBanner.svelte';
  import ProductGrid from '$lib/components/ProductGrid.svelte';

  let { data } = $props();
</script>

<svelte:head>
  <title>Molduras Novo Tempo - Quadros e Molduras</title>
</svelte:head>

<HeroBanner />

<!-- Categories Section -->
<section class="section categories-section">
  <div class="container">
    <h2 class="section-title">Nossas Categorias</h2>
    <div class="categories-grid">
      {#each data.categories as cat}
        <a href={`/produtos?category_id=${cat.id}`} class="category-card">
          <img src={cat.image_url} alt={cat.name} />
          <div class="category-overlay">
            <h3>{cat.name}</h3>
          </div>
        </a>
      {/each}
    </div>
  </div>
</section>

<!-- Featured Products -->
<section class="section featured-section">
  <div class="container">
    <h2 class="section-title">Produtos em Destaque</h2>
    {#if data.featuredProducts.length > 0}
      <ProductGrid products={data.featuredProducts} />
    {:else}
      <p class="empty-text">Nenhum produto em destaque no momento.</p>
    {/if}
    <div class="center-action">
      <a href="/produtos" class="btn btn-outline">Ver todos os produtos</a>
    </div>
  </div>
</section>

<!-- Info Banners -->
<section class="section info-section">
  <div class="container info-grid">
    <div class="info-card">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="1.5">
        <rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
      </svg>
      <h3>Frete para todo Brasil</h3>
      <p>Enviamos para todo o país com segurança</p>
    </div>
    <div class="info-card">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="1.5">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
      <h3>Compra Segura</h3>
      <p>Seus dados protegidos em todas as etapas</p>
    </div>
    <div class="info-card">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="1.5">
        <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <h3>Qualidade Garantida</h3>
      <p>Mais de 20 anos de experiência no mercado</p>
    </div>
    <div class="info-card">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="1.5">
        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
      </svg>
      <h3>Atendimento Dedicado</h3>
      <p>Suporte via WhatsApp e telefone</p>
    </div>
  </div>
</section>

<style>
  .section {
    padding: 3rem 0;
  }

  .categories-section {
    background: var(--gray-50);
  }

  .categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }

  .category-card {
    position: relative;
    aspect-ratio: 4/3;
    border-radius: var(--radius-lg);
    overflow: hidden;
  }

  .category-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s;
  }

  .category-card:hover img {
    transform: scale(1.1);
  }

  .category-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(26,26,26,0.9) 0%, transparent 60%);
    display: flex;
    align-items: flex-end;
    padding: 1rem;
  }

  .category-overlay h3 {
    color: var(--white);
    font-size: 0.95rem;
    font-weight: 600;
  }

  .center-action {
    text-align: center;
    margin-top: 2rem;
  }

  .empty-text {
    text-align: center;
    color: var(--gray-400);
    padding: 2rem;
  }

  .info-section {
    background: var(--gray-50);
  }

  .info-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }

  .info-card {
    text-align: center;
    padding: 2rem 1rem;
  }

  .info-card h3 {
    margin: 1rem 0 0.25rem;
    font-size: 0.95rem;
  }

  .info-card p {
    font-size: 0.8rem;
    color: var(--gray-500);
  }

  @media (max-width: 768px) {
    .info-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 480px) {
    .info-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
