<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/state';
  import { api } from '$lib/api';
  import { buildWhatsAppUrl } from '$lib/whatsapp';

  let product: any = $state(null);
  let loading = $state(true);
  let message = $state('');
  let activeImage = $state(0);

  onMount(async () => {
    try {
      const id = Number(page.params.id);
      product = await api.getProduct(id);
      activeImage = 0;
    } catch {
      message = 'Produto não encontrado';
    }
    loading = false;
  });

  const whatsappUrl = $derived(product ? buildWhatsAppUrl(product.name) : buildWhatsAppUrl());
</script>

<svelte:head>
  <title>{product?.name || 'Produto'} - Molduras Novo Tempo</title>
</svelte:head>

<section class="product-page">
  <div class="container">
    {#if loading}
      <p class="loading">Carregando...</p>
    {:else if !product}
      <p class="error">{message || 'Produto não encontrado'}</p>
      <a href="/produtos" class="btn btn-outline">Voltar ao catálogo</a>
    {:else}
      <nav class="breadcrumb">
        <a href="/">Início</a> /
        <a href="/produtos">Produtos</a> /
        {#if product.category}
          <a href={`/produtos?category_id=${product.category.id}`}>{product.category.name}</a> /
        {/if}
        <span>{product.name}</span>
      </nav>

      <div class="product-layout">
        <div class="product-image">
          {#if product.images?.length}
            <img src={product.images[activeImage].url} alt="{product.name} - imagem {activeImage + 1}" />
            {#if product.images.length > 1}
              <div class="image-thumbs">
                {#each product.images as img, i}
                  <button
                    class="thumb-btn"
                    class:active={activeImage === i}
                    onclick={() => activeImage = i}
                    aria-label="Ver imagem {i + 1}"
                  >
                    <img src={img.url} alt="{product.name} {i + 1}" />
                  </button>
                {/each}
              </div>
            {/if}
          {:else if product.image_url}
            <img src={product.image_url} alt={product.name} />
          {:else}
            <div class="no-image">Sem imagem</div>
          {/if}
        </div>

        <div class="product-info">
          {#if product.category}
            <span class="product-category">{product.category.name}</span>
          {/if}
          <h1 class="product-name">{product.name}</h1>

          <div class="product-description">
            <h3>Descrição</h3>
            <p>{product.description}</p>
          </div>

          <div class="product-actions">
            <a
              href={whatsappUrl}
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary add-to-cart"
            >
              Tenho interesse neste produto
            </a>
          </div>

          {#if message}
            <p class="message">{message}</p>
          {/if}

          <div class="product-features">
            <div class="feature">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2">
                <rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
              </svg>
              <span>Frete para todo Brasil</span>
            </div>
            <div class="feature">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>Compra Segura</span>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</section>

<style>
  .product-page {
    padding: 2rem 0 4rem;
  }

  .breadcrumb {
    font-size: 0.85rem;
    color: var(--gray-500);
    margin-bottom: 2rem;
  }

  .breadcrumb a {
    color: var(--gray-500);
    transition: color 0.2s;
  }

  .breadcrumb a:hover {
    color: var(--primary-dark);
  }

  .breadcrumb span {
    color: var(--black);
    font-weight: 500;
  }

  .product-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: start;
  }

  .product-image {
    background: var(--gray-100);
    border-radius: var(--radius-lg);
    overflow: hidden;
  }

  .product-image > img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
  }

  .no-image {
    width: 100%;
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--gray-500);
  }

  .image-thumbs {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    overflow-x: auto;
    background: var(--gray-100);
  }

  .thumb-btn {
    flex-shrink: 0;
    width: 64px;
    height: 64px;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid transparent;
    cursor: pointer;
    padding: 0;
    transition: border-color 0.15s;
    opacity: 0.7;
  }

  .thumb-btn img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .thumb-btn:hover, .thumb-btn.active {
    border-color: var(--primary);
    opacity: 1;
  }

  .product-category {
    display: inline-block;
    background: var(--primary);
    color: var(--black);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }

  .product-name {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    line-height: 1.3;
  }

  .product-description {
    margin-bottom: 1.5rem;
  }

  .product-description h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }

  .product-description p {
    color: var(--gray-600);
    font-size: 0.9rem;
    line-height: 1.7;
  }

  .product-actions {
    display: flex;
    margin-bottom: 1rem;
  }

  .add-to-cart {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 0.9rem 2rem;
    font-size: 1rem;
    background: var(--green-whatsapp);
    border-color: var(--green-whatsapp);
    color: var(--white);
  }

  .add-to-cart:hover {
    filter: brightness(0.95);
  }

  .message {
    padding: 0.5rem;
    border-radius: var(--radius);
    font-size: 0.85rem;
    color: var(--danger);
    margin-bottom: 1rem;
  }

  .product-features {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-200);
  }

  .feature {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.85rem;
    color: var(--gray-600);
  }

  .loading, .error {
    text-align: center;
    padding: 3rem;
    color: var(--gray-500);
  }

  @media (max-width: 768px) {
    .product-layout {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
  }
</style>
